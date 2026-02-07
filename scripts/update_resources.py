import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

def fetch_arxiv_papers():
    # Search for papers from DeepMind authors or with DeepMind affiliation in the last 30 days
    # Note: ArXiv API search is limited, using a broad query for demonstration
    base_url = 'http://export.arxiv.org/api/query?'
    # Query for "DeepMind" in abstract or title, sorted by submittedDate
    query = 'search_query=all:DeepMind&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending'
    response = requests.get(base_url + query)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        papers = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip().replace('\n', ' ')
            link = entry.find('{http://www.w3.org/2005/Atom}id').text
            published = entry.find('{http://www.w3.org/2005/Atom}published').text[:10]
            papers.append(f"*   **[{published}]** [{title}]({link})")
        return papers
    return []

def fetch_github_repos():
    # Fetch recently updated repos from google-deepmind organization
    url = "https://api.github.com/orgs/google-deepmind/repos?sort=updated&direction=desc&per_page=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        repo_list = []
        for repo in repos:
            name = repo['name']
            link = repo['html_url']
            desc = repo.get('description', 'No description')
            updated = repo['updated_at'][:10]
            repo_list.append(f"*   **[{updated}]** [{name}]({link}): {desc}")
        return repo_list
    return []

def update_readme():
    papers = fetch_arxiv_papers()
    repos = fetch_github_repos()
    
    if not papers and not repos:
        print("No new content found.")
        return

    update_content = f"\n\n## Latest Updates ({datetime.now().strftime('%Y-%m-%d')})\n"
    
    if papers:
        update_content += "\n### Recent ArXiv Papers (DeepMind)\n" + "\n".join(papers)
    
    if repos:
        update_content += "\n### Recently Updated GitHub Repos\n" + "\n".join(repos)
        
    with open("README.md", "a") as f:
        f.write(update_content)
    
    print("README.md updated.")

if __name__ == "__main__":
    update_readme()
