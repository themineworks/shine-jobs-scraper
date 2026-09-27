#!/usr/bin/env python3
"""Times Group India job board, 22 fields, monitor mode. Python, Node.js and cURL clients for the Shine.com Jobs Scraper on Apify, pay per result.

Command-line client for the themineworks/shine-jobs-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/shine-jobs-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/shine-jobs-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--search-keywords", help="Comma-separated. One or more job-search keywords, for example 'python developer', 'data scientist'")
    ap.add_argument("--location", help="City name, for example 'Bangalore', 'Mumbai', 'Pune'")
    ap.add_argument("--experience-level", help="Years of experience band, as offered by Shine's own filter")
    ap.add_argument("--salary-range", help="Annual CTC band, as offered by Shine's own filter")
    ap.add_argument("--employment-type", help="Employment type, as offered by Shine's own filter")
    ap.add_argument("--shift-type", help="Full-time or part-time, as offered by Shine's own filter")
    ap.add_argument("--sort-by", help="Relevance (Shine's default ranking) or Freshness (newest postings first, useful with…")
    ap.add_argument("--max-jobs", type=int, help="Maximum number of jobs to scrape across all keywords")
    ap.add_argument("--include-job-description", action=argparse.BooleanOptionalAction, help="If true, include the full job description text")
    ap.add_argument("--monitor-mode", action=argparse.BooleanOptionalAction, help="Run on a schedule and deliver ONLY results not seen in a previous run")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.search_keywords: run_input["searchKeywords"] = [s.strip() for s in a.search_keywords.split(",") if s.strip()]
    if a.location is not None: run_input["location"] = a.location
    if a.experience_level is not None: run_input["experienceLevel"] = a.experience_level
    if a.salary_range is not None: run_input["salaryRange"] = a.salary_range
    if a.employment_type is not None: run_input["employmentType"] = a.employment_type
    if a.shift_type is not None: run_input["shiftType"] = a.shift_type
    if a.sort_by is not None: run_input["sortBy"] = a.sort_by
    if a.max_jobs is not None: run_input["maxJobs"] = a.max_jobs
    if a.include_job_description is not None: run_input["includeJobDescription"] = a.include_job_description
    if a.monitor_mode is not None: run_input["monitorMode"] = a.monitor_mode

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
