import os
import requests

GITHUB_USERNAME = "pratyushwinorlearn"  # Replace with your exact GitHub handle
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "corpus"))

os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_readmes():
    print(f"Fetching public repositories for '{GITHUB_USERNAME}'...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    resp = requests.get(url)

    if resp.status_code != 200:
        print(f"Error fetching repos: {resp.json().get('message', 'Unknown error')}")
        return

    repos = resp.json()
    print(f"Found {len(repos)} repositories. Downloading READMEs...\n")

    downloaded = 0
    for repo in repos:
        name = repo["name"]
        branch = repo.get("default_branch", "main")
        readme_url = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{name}/{branch}/README.md"

        readme_resp = requests.get(readme_url)
        if readme_resp.status_code == 200 and readme_resp.text.strip():
            file_path = os.path.join(OUTPUT_DIR, f"{name}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {name}\n\n{readme_resp.text}")
            print(f"  [✓] Saved {name}.md")
            downloaded += 1
        else:
            print(f"  [x] Skipped {name} (No README)")

    print(f"\nCompleted! {downloaded} project documents saved to '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    fetch_readmes()