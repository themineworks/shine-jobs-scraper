# Shine.com Jobs Scraper: Salary, Experience & Skills API

Scrape live Shine.com (Times Group) job listings across IT, BPO, banking, retail, and manufacturing: title, company, salary in lakhs, experience band, location, employment type, and full description. Filters mirror the live site exactly. No login, no browser.

**Run it on Apify:** [apify.com/themineworks/shine-jobs-scraper](https://apify.com/themineworks/shine-jobs-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/shine-jobs-scraper](https://themineworks.com/actors/shine-jobs-scraper/)

**Price:** From $1.50 per 1,000 jobs on Apify's higher plans ($2.50 on the free plan). Failed and empty results are never charged.

## What it returns

* Filter by keyword, location, experience band, salary, and shift
* Salary returned as numeric min/max lakhs, not display text
* Skills returned as Shine's own structured tag array
* Monitor mode + freshness sort for a daily new-jobs feed
* No login, no browser, no anti-bot challenge found

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/shine-jobs-scraper").call(run_input={
    "searchKeywords": [
        "python developer"
    ],
    "location": "Bangalore",
    "experienceLevel": "3to5",
    "salaryRange": "6to8"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/shine-jobs-scraper').call({
    "searchKeywords": [
        "python developer"
    ],
    "location": "Bangalore",
    "experienceLevel": "3to5",
    "salaryRange": "6to8"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~shine-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchKeywords": ["python developer"], "location": "Bangalore", "experienceLevel": "3to5", "salaryRange": "6to8"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 shine_jobs_scraper.py --token YOUR_APIFY_TOKEN --search-keywords "python developer" --location "Bangalore" --experience-level "3to5" --salary-range "6to8"
node shine_jobs_scraper.mjs --token YOUR_APIFY_TOKEN --search-keywords "python developer" --location "Bangalore" --experience-level "3to5" --salary-range "6to8"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `searchKeywords` (required) | array |  | One or more job-search keywords, for example 'python developer', 'data scientist' |
| `location` | string |  | City name, for example 'Bangalore', 'Mumbai', 'Pune' |
| `experienceLevel` | string | `""` | Years of experience band, as offered by Shine's own filter |
| `salaryRange` | string | `""` | Annual CTC band, as offered by Shine's own filter |
| `employmentType` | string | `""` | Employment type, as offered by Shine's own filter |
| `shiftType` | string | `""` | Full-time or part-time, as offered by Shine's own filter |
| `sortBy` | string | `"relevance"` | Relevance (Shine's default ranking) or Freshness (newest postings first, useful with Monitor mode) |
| `maxJobs` | integer | `5` | Maximum number of jobs to scrape across all keywords |
| `includeJobDescription` | boolean | `false` | If true, include the full job description text |
| `monitorMode` | boolean | `false` | Run on a schedule and deliver ONLY results not seen in a previous run |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `job_id` | string | Shine.com internal job ID |
| `title` | string | Job title |
| `company` | string | Company name (or recruiting consultancy name) |
| `locations` | array | Job location(s) |
| `location` | string | Job location(s) as a comma-separated string |
| `experience_min_years` | number | Minimum years of experience required |
| `experience_max_years` | number | Maximum years of experience required |
| `experience_text` | string | Raw experience text from Shine (for example '3 to 7 Yrs') |
| `salary_text` | string | Raw salary string from Shine (for example 'Rs 4.0, 6 Lakh/Yr' or '[Salary Hidden]') |
| `salary_min_lakhs` | number | Minimum salary in INR lakhs per annum |
| `salary_max_lakhs` | number | Maximum salary in INR lakhs per annum |
| `employment_type` | string | Employment type: regular, contractual, internship, work-from-home |
| `shift_type` | string | full-time or part-time |
| `skills` | array | Keywords / skills tagged on the job |
| `description` | string | Job description text, HTML stripped (truncated to 500 chars unless includeJobDescription=true) |
| `apply_url` | string | URL to the Shine.com job detail / apply page |
| `recruiter_name` | string | Recruiter / hiring firm display name, when shown |
| `posted_date` | string | ISO timestamp when the job was posted on Shine |
| `posted_days_ago` | number | Approximate number of days since the job was posted |
| `expiry_date` | string | ISO timestamp when the listing expires on Shine |
| `early_applicant` | boolean | True if Shine flags this as an early-applicant opportunity |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/shine-jobs-scraper
```

## FAQ

### Is this scraping HTML?

No. It calls the same public JSON endpoint (/api/v2/search/simple/) Shine's own web app calls. No browser, a few seconds per keyword.

### Do I need a proxy?

No. The endpoint was verified reachable with no user-agent, cookies, or proxy at all.

### Why is salary_text sometimes "[Salary Hidden]"?

Many recruiters choose not to publish a number. This actor reports that faithfully rather than inventing a figure.

### Can I get only the newest postings?

Yes. Set sortBy to freshness, and turn on monitorMode to charge only for genuinely new listings on repeat runs.

### What does it cost?

Pay per event: one job-scraped event per delivered record, charged only after validation. Failed and empty results are never charged.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Hirist Jobs Scraper](https://themineworks.com/actors/hirist-jobs-scraper/): India IT jobs across 147 locations, 19 fields
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
