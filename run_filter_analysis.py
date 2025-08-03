#!/usr/bin/env python3

from search_engine import CandidateSearchEngine
from query_configs import QueryConfigurations
import json
import time

def run_comprehensive_filter_analysis():
    print("Starting Comprehensive Filter Analysis")
    print("=" * 60)

    engine = CandidateSearchEngine()
    configs = QueryConfigurations().get_all_configs()

    print(f"Analyzing {len(configs)} job configurations:")
    for config_name, config_data in configs.items():
        print(f"  - {config_name}: {config_data['name']}")

    print("\nRunning searches with detailed filter logging...")

    all_results = {}
    for i, (config_name, config_data) in enumerate(configs.items(), 1):
        print(f"\n[{i}/{len(configs)}] Processing {config_data['name']}...")

        try:
            start_time = time.time()
            results = engine.search_by_config(config_name, top_k=10)
            duration = time.time() - start_time

            all_results[config_name] = {
                "config_name": config_name,
                "job_title": config_data['name'],
                "results_count": len(results),
                "search_duration": duration,
                "status": "success"
            }

            print(f"  Found {len(results)} candidates in {duration:.2f}s")

        except Exception as e:
            print(f"  Error: {e}")
            all_results[config_name] = {
                "config_name": config_name,
                "job_title": config_data['name'],
                "status": "error",
                "error": str(e)
            }

        time.sleep(0.5)

    print("\nGenerating filter analysis...")

    filter_report = engine.generate_filter_report("comprehensive_filter_analysis.json")
    filter_stats = engine.filter_logger.get_filter_stats()

    summary_report = {
        "analysis_metadata": {
            "total_job_configs": len(configs),
            "successful_searches": len([r for r in all_results.values() if r.get("status") == "success"]),
            "failed_searches": len([r for r in all_results.values() if r.get("status") == "error"]),
            "analysis_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "individual_job_results": all_results,
        "filter_performance_summary": filter_stats
    }

    with open("comprehensive_search_summary.json", "w") as f:
        json.dump(summary_report, f, indent=2, default=str)

    print("\nReports Generated:")
    print("  - detailed_filter_logs.json")
    print("  - comprehensive_filter_analysis.json")
    print("  - comprehensive_search_summary.json")

    if filter_stats:
        overall = filter_stats["overall_stats"]
        print("\nSummary:")
        print(f"  Total candidates processed: {overall['total_candidates_processed']:,}")
        print(f"  Candidates passed filters:  {overall['total_candidates_passed']:,}")
        print(f"  Total filter failures:      {overall['total_filter_failures']:,}")
        print(f"  Overall filter rate:        {overall['overall_filter_rate']:.1%}")

        if "failure_breakdown" in filter_stats:
            failure_breakdown = filter_stats["failure_breakdown"]
            sorted_failures = sorted(failure_breakdown.items(), key=lambda x: x[1], reverse=True)
            print("\nTop Filter Issues:")
            for i, (filter_name, count) in enumerate(sorted_failures[:5], 1):
                print(f"  {i}. {filter_name}: {count:,} failures")

    print("\nFilter analysis complete.")
    return summary_report

if __name__ == "__main__":
    run_comprehensive_filter_analysis()
