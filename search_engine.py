import re
import openai
import turbopuffer as tpuf
import voyageai
import json
import logging
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional

from config import *
from utils import TextProcessor, normalize_score
from query_configs import QueryConfigurations
from logging_config import setup_logger
from filter_logger import FilterLogger

setup_logger()
logger = logging.getLogger(__name__)

class CandidateSearchEngine:
    def __init__(self):
        try:
            tpuf.api_base_url = f"https://{TURBOPUFFER_REGION}.turbopuffer.com/v1"
            self.ns = tpuf.Namespace(TPUF_NAMESPACE_NAME, api_key=TURBOPUFFER_API_KEY)
            self.text_processor = TextProcessor()
            self.query_configs = QueryConfigurations()
            self.filter_logger = FilterLogger("detailed_filter_logs.json")
            self.filter_logger.load_from_file()
            logger.info("TurboPuffer client and processors initialized.")
        except Exception as e:
            logger.critical(f"Failed to initialize TurboPuffer: {e}", exc_info=True)

        try:
            self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.openai_client = None

        try:
            self.voyage_client = voyageai.Client(api_key=VOYAGE_API_KEY)
            logger.info("Voyage AI client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Voyage AI client: {e}")
            self.voyage_client = None

    def search_by_config(self, config_name: str, top_k: int = 10) -> List[str]:
        configs = self.query_configs.get_all_configs()
        config = configs.get(config_name)

        if not config:
            logger.error(f"Configuration '{config_name}' not found.")
            return []

        return self.search(query=config['query'], job_config=config, top_k=top_k)

    def expand_query_with_openai(self, original_query: str, job_context: Dict) -> str:
        if not self.openai_client:
            logger.warning("OpenAI client not available. Skipping query expansion.")
            return original_query

        job_title = job_context.get('name', 'Professional')
        prompt = f"""
        You are an expert recruiter. Expand this job search query to include relevant synonyms, alternative terms, and industry-specific keywords for a candidate search.
        Original Query: "{original_query}"
        Job Title: {job_title}
        Focus on terms likely to appear in professional profiles like on LinkedIn.
        Return only the expanded search query as a single string, with no explanations. Use boolean operators like OR and parentheses for grouping.
        Example output: ("tax attorney" OR "tax lawyer") AND ("IRS audit" OR "tax controversy")
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4.1-nano-2025-04-14",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.2
            )
            expanded_query = response.choices[0].message.content.strip()
            logger.info(f"Query expanded: '{original_query}' -> '{expanded_query}'")
            return expanded_query
        except Exception as e:
            logger.error(f"OpenAI query expansion failed: {e}")
            return original_query

    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        if not self.voyage_client:
            logger.warning("Voyage AI client not available, skipping vector search.")
            return None
        try:
            result = self.voyage_client.embed(texts=[query], model="voyage-3", input_type="query")
            logger.debug(f"Generated embedding for query using voyage-3.")
            return result.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {e}", exc_info=True)
            return None

    def vector_search(self, query_vector: List[float], top_k: int = 100) -> List[Dict]:
        try:
            response = self.ns.query(
                vector=query_vector,
                top_k=top_k,
                include_attributes=["name", "rerank_summary", "years_experience", "keywords", "full_text"],
                distance_metric="cosine_distance"
            )
            return [
                {
                    **row.attributes,
                    'id': row.id,
                    'vector_similarity': 1.0 - row.dist
                }
                for row in response
            ]
        except Exception as e:
            logger.error(f"Vector search error: {e}", exc_info=True)
            return []

    def enhanced_hybrid_search(self, query: str, job_config: Dict, top_k: int = 200) -> List[Dict]:
        expanded_query = self.expand_query_with_openai(query, job_config)
        query_vector = self.generate_query_embedding(expanded_query)
        if not query_vector:
            return []

        vector_results = self.vector_search(query_vector, top_k=top_k)
        for res in vector_results:
            res['rrf_score'] = res.get('vector_similarity', 0)
        return vector_results

    def apply_hard_filters(self, candidates: List[Dict], hard_criteria: Dict) -> List[Dict]:
        if not hard_criteria:
            return candidates

        filtered_candidates = []
        logger.info(f"Applying hard filters to {len(candidates)} candidates")

        for c in candidates:
            passes_all = True

            min_years = hard_criteria.get('min_years_experience')
            max_years = hard_criteria.get('max_years_experience')
            actual_years = c.get('years_experience', 0)

            if min_years is not None and actual_years < min_years:
                passes_all = False
            if max_years is not None and actual_years > max_years:
                passes_all = False

            if not passes_all:
                continue

            edu_reqs = hard_criteria.get('required_education', {})
            if edu_reqs:
                passes_edu = True
                for degree, required in edu_reqs.items():
                    if degree == "any_of":
                        if not any(c.get(d, False) for d in required):
                            passes_edu = False
                            break
                    elif required and not c.get(degree, False):
                        passes_edu = False
                        break

                if not passes_edu:
                    passes_all = False

            if not passes_all:
                continue

            required_keywords = hard_criteria.get('required_keywords', [])
            if required_keywords:
                text_to_search = (c.get('full_text', '') + ' ' + c.get('rerank_summary', '')).lower()
                if not all(kw.lower() in text_to_search for kw in required_keywords):
                    passes_all = False

            if not passes_all:
                continue

            if passes_all:
                filtered_candidates.append(c)

        logger.info(f"Hard filters: {len(candidates)} -> {len(filtered_candidates)} candidates passed")
        return filtered_candidates

    def calculate_soft_score(self, candidate: Dict, soft_criteria: Dict) -> float:
        if not soft_criteria:
            return 0.0
        score = 0.0
        text_blob = (candidate.get("full_text", "") + " " + candidate.get("rerank_summary", "")).lower()

        for factor, weight in soft_criteria.get("weight_factors", {}).items():
            if any(kw.lower() in text_blob for kw in soft_criteria.get(f"{factor}_keywords", [])):
                score += weight

        if any(kw.lower() in text_blob for kw in soft_criteria.get("preferred_keywords", [])):
            score += 1.0

        if candidate.get("years_experience", 0) >= soft_criteria.get("preferred_experience", 99):
            score += 2.0

        return score

    def search(self, query: str, job_config: Dict, top_k: int = 10) -> List[str]:
        job_name = job_config.get('name', 'N/A')
        logger.info(f"Running search for: {job_name}")

        candidates_raw = self.enhanced_hybrid_search(query, job_config, top_k=250)
        if not candidates_raw:
            logger.warning("No initial candidates found from vector search.")
            return []
        logger.info(f"Found {len(candidates_raw)} initial candidates.")

        processed_candidates = [self.text_processor.parse_candidate_comprehensive(c) for c in candidates_raw]
        logger.info(f"Enriched all candidates with structured data.")

        self.filter_logger.start_session(job_name, query, len(processed_candidates))
        filtered_candidates = self.apply_hard_filters(processed_candidates, job_config.get('hard_criteria', {}))
        self.filter_logger.end_session(len(filtered_candidates))

        if not filtered_candidates:
            logger.warning("No candidates remained after hard filtering.")
            return []
        logger.info(f"{len(filtered_candidates)} candidates remain after hard filters.")

        for c in filtered_candidates:
            soft_score = self.calculate_soft_score(c, job_config.get('soft_criteria', {}))
            initial_score = c.get('rrf_score', 0)
            c['final_score'] = (initial_score * 0.4) + (soft_score * 0.6)
        logger.info(f"Calculated final scores for all candidates.")

        scores = [c['final_score'] for c in filtered_candidates]
        min_s, max_s = min(scores), max(scores)
        for c in filtered_candidates:
            c['normalized_score'] = normalize_score(c['final_score'], min_s, max_s)
        filtered_candidates.sort(key=lambda x: x.get('normalized_score', 0), reverse=True)

        result_ids = [c['id'] for c in filtered_candidates[:top_k]]
        logger.info(f"Returning top {len(result_ids)} candidate IDs.")
        logger.debug("Top 3 candidates with scores:")
        for c in filtered_candidates[:3]:
            logger.debug(f"ID: {c['id']}, Name: {c.get('name', 'N/A')}, Score: {c.get('normalized_score', 0):.3f}")

        return result_ids

    def generate_filter_report(self, save_to_file: str = "filter_analysis_report.json"):
        stats = self.filter_logger.get_filter_stats()

        if not stats:
            logger.warning("No filter statistics available")
            return {}

        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_sessions_analyzed": len(self.filter_logger.all_sessions)
            },
            "executive_summary": stats["overall_stats"],
            "detailed_breakdown": {
                "filter_failure_analysis": stats["failure_breakdown"],
                "job_config_performance": stats["job_performance"]
            },
            "recommendations": []
        }

        for job_name, job_stats in stats["job_performance"].items():
            filter_rate = job_stats["filter_rate"]
            if filter_rate > 0.8:
                report["recommendations"].append({
                    "job_config": job_name,
                    "issue": "High filter rate",
                    "filter_rate": filter_rate,
                    "recommendation": "Consider relaxing hard criteria - too many candidates being filtered"
                })
            elif filter_rate < 0.1:
                report["recommendations"].append({
                    "job_config": job_name,
                    "issue": "Low filter rate",
                    "filter_rate": filter_rate,
                    "recommendation": "Consider tightening hard criteria - filters may be too permissive"
                })

        try:
            with open(save_to_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Filter analysis report saved to {save_to_file}")
        except Exception as e:
            logger.error(f"Error saving filter report: {e}")

        return report
