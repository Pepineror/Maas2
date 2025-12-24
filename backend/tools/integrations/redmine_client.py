from typing import List, Optional, Union, Dict, Any, Type, TypeVar
import requests
import os
from urllib.parse import urljoin
from time import sleep

from backend.core.config import settings
from backend.core.logging import logger
from backend.schemas.redmine import (
    RedmineProject, RedmineIssue, RedmineUser, RedmineTracker, RedmineStatus, RedmineWikiPage
)

T = TypeVar("T")

class RedmineHttpError(Exception):
    """Raised when Redmine API returns a 4xx or 5xx error."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Redmine API Error {status_code}: {message}")

class RedmineInvalidResponse(Exception):
    """Raised when response parsing fails."""
    pass

class RedmineClient:
    """
    Robust Client for the Redmine REST API.
    Handles authentication, pagination, and error handling.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initializes the Redmine Client.
        """
        self.base_url = base_url or settings.REDMINE_BASE_URL
        self.api_key = api_key or settings.REDMINE_API_KEY
        
        if not self.base_url or not self.api_key:
            logger.warning("RedmineClient initialized without BASE_URL or API_KEY.")

        self.session = requests.Session()
        self.session.headers.update({
            "X-Redmine-API-Key": self.api_key or "",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, retry_count: int = 0) -> Dict[str, Any]:
        """
        Internal method to enforce HTTP handling and retries.
        """
        if not self.base_url:
             raise ValueError("Redmine base URL not configured.")
             
        url = urljoin(self.base_url, endpoint)
        if not endpoint.endswith(".json"):
            url = f"{url}.json" if "?" not in url else url.replace("?", ".json?")

        try:
            response = self.session.request(method, url, params=params, timeout=10)
            
            if 500 <= response.status_code < 600 and retry_count < 2:
                sleep(0.5 * (retry_count + 1))
                return self._request(method, endpoint, params, retry_count + 1)
            
            if response.status_code >= 400:
                raise RedmineHttpError(response.status_code, response.text)
                
            return response.json()
            
        except requests.exceptions.Timeout:
             if retry_count < 2:
                sleep(0.5)
                return self._request(method, endpoint, params, retry_count + 1)
             raise RedmineHttpError(408, "Request Timeout")
        except requests.exceptions.RequestException as e:
            raise RedmineHttpError(500, str(e))
        except ValueError:
             raise RedmineInvalidResponse("Failed to parse JSON response")

    def _paginate(self, endpoint: str, key: str, schema: Type[T], params: Optional[Dict] = None) -> List[T]:
        """Generic pagination handler."""
        limit = 100
        offset = 0
        all_items = []
        params = params or {}
        
        while True:
            current_params = params.copy()
            current_params.update({"limit": limit, "offset": offset})
            
            data = self._request("GET", endpoint, params=current_params)
            
            items_data = data.get(key, [])
            if not items_data:
                break
                
            for item in items_data:
                try:
                    all_items.append(schema(**item))
                except Exception as e:
                    logger.warning(f"Failed to parse {key} item {item.get('id')}: {e}")
            
            if len(items_data) < limit:
                break
                
            offset += limit
            
        return all_items

    def list_projects(self) -> List[RedmineProject]:
        """List all accessible projects."""
        return self._paginate("projects", "projects", RedmineProject)

    def get_project(self, project_id: Union[int, str]) -> RedmineProject:
        """Get details of a specific project."""
        data = self._request("GET", f"projects/{project_id}")
        return RedmineProject(**data["project"])

    def list_issues(self, project_id: Union[int, str], include: Optional[List[str]] = None) -> List[RedmineIssue]:
        """List issues for a project."""
        params = {"project_id": project_id}
        if include:
            params["include"] = ",".join(include)
        return self._paginate("issues", "issues", RedmineIssue, params=params)

    def get_issue(self, issue_id: Union[int, str]) -> RedmineIssue:
        """Get details of a specific issue."""
        data = self._request("GET", f"issues/{issue_id}")
        return RedmineIssue(**data["issue"])

    def get_wiki_page(self, project_id: Union[int, str], title: str) -> RedmineWikiPage:
        """Get a specific wiki page for a project."""
        data = self._request("GET", f"projects/{project_id}/wiki/{title}")
        return RedmineWikiPage(**data["wiki_page"])

    def list_wiki_pages(self, project_id: Union[int, str]) -> List[RedmineWikiPage]:
        """List all wiki pages for a project."""
        data = self._request("GET", f"projects/{project_id}/wiki/index")
        return [RedmineWikiPage(**p) for p in data.get("wiki_pages", [])]
