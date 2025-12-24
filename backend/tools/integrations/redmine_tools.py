from agno.tools import Toolkit
from backend.tools.integrations.redmine_client import RedmineClient
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class RedmineTools(Toolkit):
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__(name="redmine_tools")
        self.client = RedmineClient(base_url, api_key)
        self.register(self.get_project_context)

    def get_project_context(self, project_identifier: str) -> str:
        """
        Fetches a comprehensive project context from Redmine, including:
        - Project details
        - Recent/Open issues
        - Wiki pages (summaries)
        """
        try:
            project = self.client.get_project(project_identifier)
            issues = self.client.list_issues(project_id=project.id, include=["status", "tracker"])
            wiki_pages = self.client.list_wiki_pages(project.id)

            summary = f"--- REDMINE PROJECT CONTEXT: {project.name} ---\n"
            summary += f"Identifier: {project.identifier}\n"
            summary += f"Description: {project.description or 'No description available.'}\n"
            
            summary += f"\n[ISSUES] Total Open: {len(issues)}\n"
            for issue in issues[:5]:
                 summary += f"- {issue.id}: {issue.subject} ({issue.status.name})\n"

            summary += f"\n[WIKI] Total Pages: {len(wiki_pages)}\n"
            for page in wiki_pages[:5]:
                summary += f"- Page: {page.title} (Updated: {page.updated_on})\n"
                # Optionally fetch content of the main 'Wiki' page if it exists
                if page.title == "Wiki":
                    main_page = self.client.get_wiki_page(project.id, "Wiki")
                    summary += f"  Content Snippet: {main_page.text[:300]}...\n"

            return summary

        except Exception as e:
            logger.error(f"RedmineTools error for {project_identifier}: {e}")
            return f"Error retrieving Redmine context: {str(e)}"
