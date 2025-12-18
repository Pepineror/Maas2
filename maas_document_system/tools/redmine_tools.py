from agno.tools import Toolkit
from maas_document_system.tools.redmine_client import RedmineClient
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
        Fetches a summary of the project context from Redmine, including project details and open issues.
        Use this to understand the status and requirements of the project.

        Args:
            project_identifier: The string ID/slug of the project in Redmine.

        Returns:
            A string summary of the project and its open issues.
        """
        try:
            # We need to find the project ID from the identifier first (or assume we can fetch by identifier if API supports it)
            # Redmine API get_project usually accepts numeric ID or string identifier.
            project = self.client.get_project(project_identifier)
            
            # List some open issues for context
            issues = self.client.list_issues(project_id=project.id, include=["status", "tracker"])
            
            summary = f"Project: {project.name} (ID: {project.id})\n"
            summary += f"Description: {project.description or 'No description'}\n"
            summary += f"Status: {project.status}\n"
            summary += f"\nOpen Issues ({len(issues)} found):\n"
            
            for issue in issues[:10]: # Limit to 10 for context window
                 summary += f"- [{issue.tracker.name}] #{issue.id} {issue.subject} ({issue.status.name})\n"
                 if issue.description:
                     summary += f"  Description: {issue.description[:200]}...\n"

            return summary

        except Exception as e:
            logger.error(f"Failed to fetch project context for {project_identifier}: {e}")
            return f"Error fetching project data: {str(e)}"
