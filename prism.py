
import os
import requests
import re

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")

def get_pr_details():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def validate_pr_title(title):
    if not re.match(r"^(feat|fix|chore|docs|test): ", title):
        raise ValueError(f"❌ Invalid PR title: {title}")

def main():
    pr = get_pr_details()
    validate_pr_title(pr["title"])
    print("✅ PR title check passed!")

if __name__ == "__main__":
    main()
    print(f"GITHUB_REPO: {REPO}")
    print(f"PR_NUMBER: {PR_NUMBER}")
    print(f"TOKEN is set: {bool(GITHUB_TOKEN)}")
