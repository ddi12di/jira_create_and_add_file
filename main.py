import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv('JIRA_URL')
PROJECT_KEY = os.getenv('PROJECT_KEY')
TOKEN = os.getenv('TOKEN')

summary_jira = 'Title'
description_jira = 'Descriptions'
priority = 'High'  # High and Low
issue_type = 'Incident'  # Incident and Service Request Complaint
country = 'India'
components_1 = ['Web']
labels = ['In', 'kredito24.in', 'Complaint']


attachments = 'file.txt'

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

header_att = {
    'X-Atlassian-Token': 'no-check',
    "Authorization": f"Bearer {TOKEN}"
}


def jira_create(summary_jira: str, description_jira: str, priority: str, PROJECT_KEY: str, issue_type: str,
                components: list, labels: list, country: str, attachments):
    issue_data = {
        "fields": {
            "summary": summary_jira,
            "description": description_jira,
            "priority": {"name": f'{priority}'},
            "project": {"key": f"{PROJECT_KEY}"},
            "issuetype": {"name": f"{issue_type}"},
            'components': [{'name': component} for component in components],
            "labels": labels,
            "customfield_12901": {'value': country},
        }
    }

    response = requests.post(
        f"{JIRA_URL}/rest/api/2/issue",
        headers=headers,
        data=json.dumps(issue_data)
    )
    res = response.json()
    if response.status_code == 201:  # Добавить проверку файлов!!!!!

        issue_id = response.json()['key']
        print(issue_id)
        with open(attachments, 'rb') as file:
            files = {'file': (attachments, file)}
            attach_file_response = requests.post(
                f'{JIRA_URL}/rest/api/2/issue/{issue_id}/attachments',
                headers=header_att,
                files=files
            )
        print(attach_file_response.status_code)
        if attach_file_response.status_code == 200:
            print()
            print('Задача создана и файл прикреплен успешно!')
        else:
            print('Ошибка прикрепления файла:', attach_file_response.text)

    if response.status_code == 201:
        print(res)
        return res

    else:
        print(res)
        return res


jira_create(summary_jira=summary_jira, description_jira=description_jira, priority=priority, PROJECT_KEY=PROJECT_KEY,
            issue_type=issue_type, components=components_1, labels=labels, attachments=attachments, country=country)
