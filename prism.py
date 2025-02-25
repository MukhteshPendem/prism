import os
import requests
import re
import openai

# Environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("GITHUB_EVENT_PULL_REQUEST_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Valid prefixes for PR titles
VALID_PREFIXES = [
    "feat", "fix", "chore", "docs", "test", "refactor", "style", "perf", "ci", "build", "revert"
]

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def get_pr_details():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def validate_pr_title(title):
    if not re.match(rf"^({'|'.join(VALID_PREFIXES)}): ", title):
        raise ValueError(f"❌ Invalid PR title: {title}")

def generate_suggested_titles(failed_title):
    prompt = f"Suggest 3 alternate Pull Request titles for the following invalid title: {failed_title}. Make sure the title follows naming conventions such as a valid prefix (e.g., feat, fix, chore)."

    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt, 
        max_tokens=50,
        n=3,  # Get 3 title suggestions
        stop=None
    )

    suggestions = [choice['text'].strip() for choice in response['choices']]
    return suggestions

def main():
    pr = get_pr_details()
    pr_title = pr["title"]
    
    try:
        # Validate the PR title
        validate_pr_title(pr_title)
        print("✅ PR title check passed!")
    
    except ValueError as e:
        print(e)
        print("🔄 Generating title suggestions...")
        
        # If validation fails, generate title suggestions
        suggestions = generate_suggested_titles(pr_title)
        
        # Create a comment with the suggestions
        create_pr_comment(f"Your PR title is invalid. Here are some suggestions:\n" + "\n".join(suggestions))

def create_pr_comment(comment):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("✅ Comment with title suggestions added to PR!")

if __name__ == "__main__":
    main()
    print(f"GITHUB_REPO: {REPO}")
    print(f"PR_NUMBER: {PR_NUMBER}")
    print(f"TOKEN is set: {bool(GITHUB_TOKEN)}")
