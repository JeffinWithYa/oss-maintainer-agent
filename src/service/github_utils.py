import base64
from datetime import datetime
import os
from typing import Optional

from github import Github
from github.Repository import Repository

def save_research_report(content: str, topic: str, repo_name: str = "JeffinWithYa/oss-maintainer-agent") -> str:
    """
    Save a research report to GitHub and return the URL.
    
    Args:
        content: The markdown content of the report
        topic: The research topic
        repo_name: The GitHub repository name
    
    Returns:
        str: URL to the saved report
    """
    # Initialize GitHub client with token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is required")
    
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # Create a sanitized filename from the topic
    sanitized_topic = "".join(c if c.isalnum() else "_" for c in topic.lower())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/{sanitized_topic}_{timestamp}.md"
    
    # Add report metadata
    full_content = f"""---
topic: {topic}
date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

{content}
"""
    
    try:
        # Create or update the file in the repository
        repo.create_file(
            path=filename,
            message=f"Research report: {topic}",
            content=full_content,
            branch="main"
        )
        
        # Return the URL to the file
        return f"https://github.com/{repo_name}/blob/main/{filename}"
    
    except Exception as e:
        raise RuntimeError(f"Failed to save report to GitHub: {str(e)}") 