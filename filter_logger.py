import json
import os
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class FilterFailure:
    """Structure for tracking filter failures"""
    candidate_id: str
    candidate_name: str
    filter_type: str
    filter_name: str
    reason: str
    expected_value: Any
    actual_value: Any
    timestamp: str


@dataclass
class FilterSession:
    """Structure for tracking a complete filter session"""
    job_config_name: str
    query: str
    total_candidates: int
    candidates_after_filtering: int
    filter_failures: List[FilterFailure]
    timestamp: str


class FilterLogger:
    """Logger for tracking hard filter failures and search statistics"""
    
    def __init__(self, log_file: str = "filter_logs.json"):
        self.log_file = log_file
        self.current_session = None
        self.all_sessions = []
        
    def start_session(self, job_config_name: str, query: str, total_candidates: int):
        """Start a new filter session"""
        self.current_session = FilterSession(
            job_config_name=job_config_name,
            query=query,
            total_candidates=total_candidates,
            candidates_after_filtering=0,
            filter_failures=[],
            timestamp=datetime.now().isoformat()
        )
    
    def log_filter_failure(self, candidate: Dict, filter_type: str, filter_name: str, 
                          reason: str, expected_value: Any, actual_value: Any):
        """Log a specific filter failure for a candidate"""
        if not self.current_session:
            return
            
        failure = FilterFailure(
            candidate_id=candidate.get('id', 'unknown'),
            candidate_name=candidate.get('name', 'Unknown'),
            filter_type=filter_type,
            filter_name=filter_name,
            reason=reason,
            expected_value=expected_value,
            actual_value=actual_value,
            timestamp=datetime.now().isoformat()
        )
        
        self.current_session.filter_failures.append(failure)
    
    def end_session(self, candidates_after_filtering: int):
        """End the current filter session and save results"""
        if not self.current_session:
            return
            
        self.current_session.candidates_after_filtering = candidates_after_filtering
        self.all_sessions.append(self.current_session)
        self.save_to_file()
        self.current_session = None
    
    def save_to_file(self):
        """Save all sessions to JSON file"""
        try:
            # Convert dataclasses to dictionaries
            sessions_data = [asdict(session) for session in self.all_sessions]
            
            # Create the log structure
            log_data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "total_sessions": len(sessions_data),
                    "log_version": "1.0"
                },
                "sessions": sessions_data
            }
            
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Error saving filter logs: {e}")
    
    def get_filter_stats(self) -> Dict:
        """Get comprehensive statistics about filter performance"""
        if not self.all_sessions:
            return {}
            
        total_candidates = sum(session.total_candidates for session in self.all_sessions)
        total_filtered = sum(session.candidates_after_filtering for session in self.all_sessions)
        total_failures = sum(len(session.filter_failures) for session in self.all_sessions)
        
        # Failure breakdown by filter type
        failure_breakdown = {}
        for session in self.all_sessions:
            for failure in session.filter_failures:
                filter_key = f"{failure.filter_type}.{failure.filter_name}"
                if filter_key not in failure_breakdown:
                    failure_breakdown[filter_key] = 0
                failure_breakdown[filter_key] += 1
        
        # Job config performance
        job_performance = {}
        for session in self.all_sessions:
            job_name = session.job_config_name
            if job_name not in job_performance:
                job_performance[job_name] = {
                    'total_candidates': 0,
                    'filtered_candidates': 0,
                    'failure_count': 0,
                    'filter_rate': 0
                }
            
            job_performance[job_name]['total_candidates'] += session.total_candidates
            job_performance[job_name]['filtered_candidates'] += session.candidates_after_filtering
            job_performance[job_name]['failure_count'] += len(session.filter_failures)
        
        # Calculate filter rates
        for job_name in job_performance:
            total = job_performance[job_name]['total_candidates']
            filtered = job_performance[job_name]['filtered_candidates']
            if total > 0:
                job_performance[job_name]['filter_rate'] = (total - filtered) / total
        
        return {
            "overall_stats": {
                "total_candidates_processed": total_candidates,
                "total_candidates_passed": total_filtered,
                "total_filter_failures": total_failures,
                "overall_filter_rate": (total_candidates - total_filtered) / total_candidates if total_candidates > 0 else 0
            },
            "failure_breakdown": failure_breakdown,
            "job_performance": job_performance
        }
    
    def load_from_file(self):
        """Load existing log data from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    
                # Convert back to dataclasses
                self.all_sessions = []
                for session_data in data.get('sessions', []):
                    failures = [FilterFailure(**failure) for failure in session_data.get('filter_failures', [])]
                    session_data['filter_failures'] = failures
                    self.all_sessions.append(FilterSession(**session_data))
                    
            except Exception as e:
                print(f"Error loading filter logs: {e}")
                self.all_sessions = []