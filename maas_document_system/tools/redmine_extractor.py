from typing import List, Optional, Union, Dict, Any
from maas_document_system.tools.redmine_client import RedmineClient
from maas_document_system.schemas.redmine import (
    RedmineProject, RedmineIssue, RedmineUser, RedmineTracker, RedmineStatus
)

# Configuration provided in the prompt
REDMINE_BASE_URL = "http://cidiia.uce.edu.do"
# Ideally this should be an env var, but for this specific task requirement we set it as default
REDMINE_API_KEY = "43124da14909bca4587aca7cb9cc97ad2bcd7996"

class RedmineExtractor:
    """
    Extractor specific for the requested Redmine instance.
    Wraps RedmineClient with specific configuration and simplified interface.
    """
    def __init__(self, base_url: str = REDMINE_BASE_URL, api_key: str = REDMINE_API_KEY):
        self.client = RedmineClient(base_url=base_url, api_key=api_key)

    def list_projects(self) -> List[RedmineProject]:
        return self.client.list_projects()

    def list_issues(self, project_id: Optional[Union[int, str]] = None) -> List[RedmineIssue]:
        """
        List issues. If project_id is provided, filter by it.
        Otherwise lists all visible issues (might be very large, client handles pagination).
        """
        if project_id:
            return self.client.list_issues(project_id)
        # If the underlying client doesn't support list_issues without project_id, we might need to adjust.
        # Looking at RedmineClient.list_issues, it takes project_id as required arg.
        # But Redmine API allows global issue listing.
        # We'll stick to project generic listing if needed or just expose what client has.
        # Let's inspect RedmineClient.list_issues in thought before committing.
        # It has `def list_issues(self, project_id: Union[int, str], ...)` so it requires project_id.
        # We will assume for now we always want project issues or we need to update RedmineClient.
        # For this extractor, let's keep it safe.
        raise NotImplementedError("Listing global issues not supported yet in standard client, provide project_id")

    def get_issue_details(self, issue_id: Union[int, str]) -> RedmineIssue:
        return self.client.get_issue(issue_id)

    def list_users(self) -> List[RedmineUser]:
        return self.client.list_users()

    def list_trackers(self) -> List[RedmineTracker]:
        return self.client.list_trackers()

    def list_statuses(self) -> List[RedmineStatus]:
        return self.client.list_statuses()
