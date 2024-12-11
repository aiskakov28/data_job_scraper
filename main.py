import re
import requests
import pandas as pd
from datetime import datetime
from data_cleaner import clean_company_url, extract_company_name


def scrape_jobs():
    jobs = []
    quick_info = []
    url = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/README.md"

    try:
        response = requests.get(url, verify=False)
        content = response.text
        rows = content.split('\n')

        for row in rows:
            if '|' in row and ('data' in row.lower() or 'analyst' in row.lower() or 'scientist' in row.lower()):
                columns = row.split('|')
                if len(columns) >= 4:
                    company = columns[1].strip()
                    role = columns[2].strip()
                    location = columns[3].strip()
                    link = columns[4].strip() if len(columns) > 4 else ''

                    if any(keyword in role.lower() for keyword in ['data', 'analyst', 'scientist']):
                        clean_company = extract_company_name(company)
                        cleaned_url = clean_company_url(link) if link else ""

                        application_url = ""
                        if "Apply" in link:
                            urls = re.findall(r'https?://[^\s<>"\']+', link)
                            if urls:
                                application_url = urls[0]
                                application_url = re.sub(r'\?(utm_source|ref|gh_jid).*', '', application_url)

                        jobs.append({
                            'title': str(role.strip()),
                            'company': clean_company,
                            'location': str(location.strip()),
                            'url': cleaned_url,
                            'application_url': application_url,
                            'date_posted': str(datetime.now().strftime('%Y-%m-%d'))
                        })

                        quick_info.append({
                            'internship': str(role),
                            'company': clean_company,
                            'location': str(location)
                        })

                        print(f"Found job: {role} at {clean_company}")

    except Exception as e:
        print(f"Error processing jobs: {str(e)}")

    if jobs:
        df_full = pd.DataFrame(jobs)
        filename_full = f'data_positions_full_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
        df_full.to_csv(filename_full, index=False)

        df_quick = pd.DataFrame(quick_info)
        filename_quick = f'data_positions_summary_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
        df_quick.to_csv(filename_quick, index=False)

        print(f"\nSaved {len(jobs)} jobs to {filename_full}")
        print(f"Saved summary information to {filename_quick}")
    else:
        print("\nNo jobs found")


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    scrape_jobs()