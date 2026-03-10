import json
import os

issue_data= open('issueData.json')
json_data = json.load(issue_data)
linked_issues = json_data["fields"]["issuelinks"]
linked_ids = []
for issue in linked_issues:
    linked_ids.append(f'_{issue["id"]}_')
filter_string = f"{' or '.join(linked_ids)}"
print(filter_string)
