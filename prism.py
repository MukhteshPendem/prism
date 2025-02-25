import os
import requests
import re
from openai import OpenAI

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


VALID_PREFIXES = [
    "feat", "fix", "chore", "docs", "test", "refactor", "style", "perf", "ci", "build", "revert"
]


def get_pr_details():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def validate_pr_title(title):
    if not re.match(rf"^({'|'.join(VALID_PREFIXES)}): ", title):
        raise ValueError(f"❌ Invalid PR title: {title}")


def generate_suggested_titles(title):
    prompt = f"The PR title '{title}' doesn't follow conventional commit standards. Suggest three alternative, properly formatted titles."

    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  
    )

    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": f"{prompt}",
        }
    ],
    model="gpt-4o",
)

    suggestions = chat_completion['choices'][0]['message']['content']
    return suggestions


def main():
    try:
        pr = get_pr_details()
        validate_pr_title(pr["title"])
        print("✅ PR title check passed!")
    except ValueError as e:
        print(e)
        suggestions = generate_suggested_titles(pr["title"])
        print("💡 Suggested PR titles:\n" + suggestions)


if __name__ == "__main__":
    main()
    print(f"GITHUB_REPO: {REPO}")
    print(f"PR_NUMBER: {PR_NUMBER}")
    print(f"TOKEN is set: {bool(GITHUB_TOKEN)}")
