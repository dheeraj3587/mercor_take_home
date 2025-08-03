import requests
import json
import time
from typing import Dict, List
from config import *
from search_engine import CandidateSearchEngine
from query_configs import QueryConfigurations
from utils import logger

class SearchEvaluator:
    def __init__(self):
        self.search_engine = CandidateSearchEngine()
        self.query_configs = QueryConfigurations()
        self.evaluate_url = "https://mercor-dev--search-eng-interview.modal.run/evaluate"

    def test_single_query(self, config_path: str, candidate_ids: List[str]) -> Dict:
        if len(candidate_ids) == 0:
            logger.error(f"No candidates found for {config_path}")
            return {"error": "No candidates provided"}

        if len(candidate_ids) > FINAL_CANDIDATES:
            candidate_ids = candidate_ids[:FINAL_CANDIDATES]

        payload = {
            "config_path": config_path,
            "object_ids": candidate_ids
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": EMAIL
        }

        try:
            logger.info(f"Testing {config_path} with {len(candidate_ids)} candidates...")
            response = requests.post(self.evaluate_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                avg_score = result.get('average_final_score', 'N/A')
                logger.info(f"{config_path}: Average score = {avg_score}")

                if 'average_soft_scores' in result:
                    logger.info("  Soft scores:")
                    for score_info in result['average_soft_scores']:
                        criteria = score_info.get('criteria_name', 'Unknown')
                        score = score_info.get('average_score', 'N/A')
                        logger.info(f"    {criteria}: {score}")

                if 'average_hard_scores' in result:
                    logger.info("  Hard scores:")
                    for score_info in result['average_hard_scores']:
                        criteria = score_info.get('criteria_name', 'Unknown')
                        pass_rate = score_info.get('pass_rate', 'N/A')
                        logger.info(f"    {criteria}: {pass_rate} pass rate")

                return result
            else:
                logger.error(f"{config_path}: HTTP {response.status_code} - {response.text}")
                return {"error": f"HTTP {response.status_code}", "message": response.text}

        except requests.exceptions.Timeout:
            logger.error(f"{config_path}: Request timeout")
            return {"error": "timeout"}
        except Exception as e:
            logger.error(f"{config_path}: {str(e)}")
            return {"error": str(e)}

    def test_specific_queries(self, query_list: List[str] = None) -> Dict[str, Dict]:
        all_configs = self.query_configs.get_all_configs()

        if query_list is None:
            query_list = [
                "tax_lawyer.yml",
                "bankers.yml", 
                "doctors_md.yml",
                "junior_corporate_lawyer.yml"
            ]

        results = {}
        logger.info(f"Testing {len(query_list)} specific queries...")

        for config_name in query_list:
            if config_name not in all_configs:
                logger.error(f"Configuration '{config_name}' not found")
                continue

            config_data = all_configs[config_name]
            logger.info(f"{'='*40}")
            logger.info(f"Testing: {config_data['name']} ({config_name})")
            logger.info(f"{'='*40}")

            try:
                candidate_ids = self.search_engine.search_by_config(config_name, top_k=FINAL_CANDIDATES)

                if not candidate_ids:
                    logger.error(f"No candidates found for {config_name}")
                    results[config_name] = {"error": "No candidates found"}
                    continue

                eval_result = self.test_single_query(config_name, candidate_ids)

                results[config_name] = {
                    "config_data": config_data,
                    "candidate_ids": candidate_ids,
                    "evaluation": eval_result,
                    "timestamp": time.time()
                }

                time.sleep(1)

            except Exception as e:
                logger.error(f"Error testing {config_name}: {e}")
                results[config_name] = {"error": str(e)}

        return results

    def test_all_queries(self) -> Dict[str, Dict]:
        all_configs = self.query_configs.get_all_configs()
        query_list = list(all_configs.keys())

        logger.info(f"Testing all {len(query_list)} queries...")
        return self.test_specific_queries(query_list)

    def save_test_results(self, results: Dict[str, Dict], filename: str = "test_results.json"):
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Test results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving test results: {e}")

    def print_test_summary(self, results: Dict[str, Dict]):
        print(f"\n{'='*60}")
        print("EVALUATION TEST SUMMARY")
        print(f"{'='*60}")

        successful_tests = 0
        total_score = 0.0

        print(f"{'Query Type':<25} {'Score':<10} {'Status':<15}")
        print("-" * 60)

        for config_name, result in results.items():
            if "evaluation" in result and "average_final_score" in result["evaluation"]:
                score = result["evaluation"]["average_final_score"]
                total_score += score
                successful_tests += 1
                status = "Success"
                score_str = f"{score:.3f}"
            else:
                status = "Failed"
                score_str = "N/A"

            query_name = config_name.replace('.yml', '')
            print(f"{query_name:<25} {score_str:<10} {status:<15}")

        print("-" * 60)

        if successful_tests > 0:
            average_score = total_score / successful_tests
            print(f"{'AVERAGE':<25} {average_score:.3f}      ({successful_tests}/{len(results)} successful)")
        else:
            print("No successful tests")

        print(f"{'='*60}")


if __name__ == "__main__":
    evaluator = SearchEvaluator()

    print("SEARCH ENGINE TESTING")
    print("Development evaluation in progress")
    print(f"Email: {EMAIL}")
    print(f"Namespace: {TPUF_NAMESPACE_NAME}")

    print("\nWhat would you like to test?")
    print("1. Test a few key queries")
    print("2. Test all queries")
    print("3. Test specific queries")

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        results = evaluator.test_specific_queries()
    elif choice == "2":
        results = evaluator.test_all_queries()
    elif choice == "3":
        queries = input("Enter query names (comma-separated, e.g., tax_lawyer.yml,bankers.yml): ").strip()
        query_list = [q.strip() for q in queries.split(",") if q.strip()]
        results = evaluator.test_specific_queries(query_list)
    else:
        print("Invalid choice")
        exit()

    evaluator.save_test_results(results)
    evaluator.print_test_summary(results)

    print("\nTest results saved to 'test_results.json'")
