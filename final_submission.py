import requests
import json
import time
from typing import Dict, List
from config import *
from search_engine import CandidateSearchEngine
from query_configs import QueryConfigurations
from utils import logger

class FinalSubmission:
    """Handles the final candidate submission to the grading endpoint"""

    def __init__(self):
        self.search_engine = CandidateSearchEngine()
        self.query_configs = QueryConfigurations()
        self.grade_url = "https://mercor-dev--search-eng-interview.modal.run/grade"

    def generate_all_candidates(self) -> Dict[str, List[str]]:
        """Generate candidate lists for all job types"""
        all_configs = self.query_configs.get_all_configs()
        submission_data = {}

        logger.info(f"Generating candidates for {len(all_configs)} different job roles...")

        for config_name, config_data in all_configs.items():
            logger.info(f"Processing: {config_data['name']} ({config_name})")

            try:
                candidate_ids = self.search_engine.search_by_config(config_name, top_k=FINAL_CANDIDATES)

                if len(candidate_ids) < FINAL_CANDIDATES:
                    logger.warning(f"{config_name}: Only found {len(candidate_ids)} candidates (need: {FINAL_CANDIDATES})")

                submission_data[config_name] = candidate_ids[:FINAL_CANDIDATES]
                logger.info(f"{config_name}: Successfully prepared {len(candidate_ids)} candidates")

            except Exception as e:
                logger.error(f"Error processing {config_name}: {e}")
                continue

        return submission_data

    def validate_final_submission(self, candidate_data: Dict[str, List[str]]) -> bool:
        """Check if submission meets all requirements before sending"""
        all_configs = self.query_configs.get_all_configs()
        missing_configs = set(all_configs.keys()) - set(candidate_data.keys())
        
        if missing_configs:
            logger.warning(f"Missing configurations: {missing_configs}")

        for config_name, candidates in candidate_data.items():
            if len(candidates) < FINAL_CANDIDATES:
                logger.warning(f"{config_name}: Has {len(candidates)} candidates (need: {FINAL_CANDIDATES})")
            
            # Check each candidate ID is valid
            for i, candidate_id in enumerate(candidates):
                if not candidate_id or not isinstance(candidate_id, str) or len(candidate_id) < 10:
                    logger.error(f"{config_name} candidate {i+1} has invalid ID: '{candidate_id}'")
                    return False

        logger.info("Submission validation passed")
        return True

    def submit_for_final_grading(self, candidate_data: Dict[str, List[str]]) -> Dict:
        """Submit candidate data to the grading endpoint"""
        payload = {
            "config_candidates": candidate_data
        }
        headers = {
            "Content-Type": "application/json", 
            "Authorization": EMAIL
        }

        try:
            logger.info("Sending submission for final grading...")
            logger.info(f"Job roles: {len(candidate_data)}")
            logger.info(f"Total candidates: {sum(len(candidates) for candidates in candidate_data.values())}")

            response = requests.post(self.grade_url, headers=headers, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Final submission successful!")
                return result
            else:
                logger.error(f"❌ Submission failed: HTTP {response.status_code}")
                logger.error(f"Response: {response.text}")
                return {"error": f"HTTP {response.status_code}", "message": response.text}

        except requests.exceptions.Timeout:
            logger.error("❌ Submission timed out")
            return {"error": "timeout"}
        except Exception as e:
            logger.error(f"❌ Submission error: {str(e)}")
            return {"error": str(e)}

    def save_final_submission(self, candidate_data: Dict[str, List[str]], filename: str = "final_submission_backup.json"):
        """Save submission data as backup before sending"""
        submission_backup = {
            "submitter_info": {
                "name": FULL_NAME,
                "email": EMAIL,
                "namespace": TPUF_NAMESPACE_NAME,
                "submission_time": time.time()
            },
            "submission_data": {
                "config_candidates": candidate_data
            },
            "metadata": {
                "total_query_types": len(candidate_data),
                "expected_candidates_per_query": FINAL_CANDIDATES,
                "actual_candidates_per_query": {cfg: len(cands) for cfg, cands in candidate_data.items()},
                "total_candidates_submitted": sum(len(candidates) for candidates in candidate_data.values())
            }
        }

        try:
            with open(filename, 'w') as f:
                json.dump(submission_backup, f, indent=2)
            logger.info(f"Submission backup saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving backup: {e}")

    def run_final_submission(self):
        print("\n" + "="*60)
        print("FINAL SUBMISSION FOR GRADING")
        print("="*60)
        print(f"Name: {FULL_NAME}")
        print(f"Email: {EMAIL}")
        print(f"Namespace: {TPUF_NAMESPACE_NAME}")
        print("\nNote: Ensure you have tested your search engine with evaluator.py")
        print("="*60)

        # Single confirmation
        confirm = input("\nProceed with final submission? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Submission cancelled.")
            return None

        print("\nInitiating final submission process...")

        # Step 1: Generate candidates
        logger.info("Generating candidates for all query types...")
        candidate_data = self.generate_all_candidates()

        if not candidate_data:
            logger.error("No candidates generated. Aborting submission.")
            return None

        # Step 2: Validate submission
        logger.info("Validating submission data...")
        if not self.validate_final_submission(candidate_data):
            logger.error("Validation failed. Aborting submission.")
            return None

        # Step 3: Save backup
        logger.info("Creating submission backup...")
        self.save_final_submission(candidate_data)

        # Step 4: Submit
        print(f"\nSubmission Summary:")
        print(f"- Query types: {len(candidate_data)}")
        print(f"- Total candidates: {sum(len(candidates) for candidates in candidate_data.values())}")
        
        logger.info("Submitting to grading service...")
        result = self.submit_for_final_grading(candidate_data)

        # Handle results
        if "error" not in result:
            print("\n" + "="*60)
            print("SUBMISSION SUCCESSFUL")
            print("="*60)
            
            with open("final_grading_result.json", "w") as f:
                json.dump(result, f, indent=2)
            print("Results saved to 'final_grading_result.json'")
            
        else:
            print("\n" + "="*60)
            print("SUBMISSION FAILED")
            print("="*60)
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"Details: {result.get('message', 'No additional details')}")
            
            with open("submission_error.json", "w") as f:
                json.dump(result, f, indent=2)
            print("Error details saved to 'submission_error.json'")

        return result

if __name__ == "__main__":
    submission = FinalSubmission()
    print("Final Submission System")
    print("Uses /grade endpoint for official submission")
    print("(Different from evaluator.py which uses /evaluate for testing)")
    
    result = submission.run_final_submission()