# Binfx_report_generator

## About
Set a scheduler to run on the first of every month to:
- generate plots (helpdesk):
    - Workload trend
    - Month Workload
    - Opened vs closed tickets this month
    - Current (open) Tickets by status
    - Time to first respond - met vs breached
    - Time to resolve - met vs breached

- Produce reports
    - Includes plots and brief descriptions
    - To include number of data processed (?)

## Commands
In the **root** folder of project:
1. Run plots .py to generate plots

    `python3 code/plots.py -m data/2101 -a data/all_data -d 'Jan 2021'`

2. Run doc_report.py to generate report

    `python3 code/doc_report.py -p data/2101`

## Data

Data required is pulled from reports section in helpdesk. The snapshot
current (open) ticket file (suffix EMEE) is pulled from search issue. Data required:
- Created requests per day for the month
- Requested completed per day for the month
- Breached SLAs time to respond
- Breached SLAs time to resolve
- Current (open) tickets (save as EMEE_ddmmyy)
- Created requests per month for all time (save in seperate folder called all_data)

## Structure

```bash
├── Binfx_Service_Reports
    ├── data
    │   ├── Created_requests_per_day_for_the _month.tsv
    │   ├── Requested_completed_per_day_for_the_month
    │   ├── Breached_SLAs_time_to_respond.tsv
    │   ├── Breached_SLAs_time_to_resolve.tsv
    │   └── EMEE_ddmmyy.tsv
    ├── all_data
    │   └── Created_requests_per_month_for_all_time.tsv
    ├── template
    │   └── Report_template.docx
    └── code
        ├── doc_report.py
        ├── plots.py
        └── README.md
```