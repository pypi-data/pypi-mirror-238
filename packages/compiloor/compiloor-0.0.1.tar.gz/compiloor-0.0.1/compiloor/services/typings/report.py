from typing import Dict

REPORT_VARIABLES = [
    '[[protocol_name_bold]]',
    '[[protocol_repository_bold]]',
    '[[protocol_commit_bold]]', 
    '[[protocol_date_bold]]',
    '[[type_bold]]',
    '[[protocol_sloc_bold]]',
]

INFORMATION_TABLE_VARIABLES: Dict[str, str] = {
    '[[protocol_protocol_name_bold]]': 'Protocol Name',
    '[[protocol_repository_bold]]': 'Repository',
    '[[protocol_commit_bold]]': 'Commit', 
    '[[protocol_date_bold]]': 'Date',
    '[[protocol_type_bold]]': 'Protocol Type',
    '[[protocol_sloc_bold]]': 'SLOC'
}

REPORT_SECTION_HEADINGS = [
    "1. About", "2. Disclaimer",
    "3. Introduction", "4. Risk Classification",
    "4.1. Impact", "4.2. Likelihood",
    "4.3. Action required for severity levels",
    "5. Executive Summary", "6. Findings"
]

PROTOCOL_INFORMATION_TABLE_COLUMNS = ["Protocol Name", "Repository", "Commit", "Date", "Protocol Type", "SLOC"]

SEVERITY_CLASSIFICATION_TABLE_ROWS = [
    ["Likelihood: High", "Critical", "High", "Medium"],
    ["Likelihood: Medium", "High", "Medium", "Low"],
    ["Likelihood: Low", "Medium", "Low", "Low"],
]
SEVERITY_CLASSIFICATION_TABLE_COLUMNS = ["Severity", "Impact: High", "Impact: Medium", "Impact: Low"]

FINDING_COUNT_TABLE_COLUMNS = ["Severity", "Amount"]