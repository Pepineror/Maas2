from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RedmineProject(BaseModel):
    """Represents a Redmine Project."""
    id: int = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    identifier: str = Field(..., description="Project identifier (slug)")
    description: Optional[str] = Field(None, description="Project description")
    created_on: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_on: Optional[datetime] = Field(None, description="Last update timestamp")
    status: int = Field(1, description="Project status")

class RedmineUser(BaseModel):
    """Represents a Redmine User."""
    id: int = Field(..., description="User ID")
    login: str = Field(..., description="User login")
    firstname: str = Field(..., description="First name")
    lastname: str = Field(..., description="Last name")
    mail: Optional[str] = Field(None, description="Email address")
    last_login_on: Optional[datetime] = Field(None, description="Last login timestamp")

class RedmineTracker(BaseModel):
    """Represents a Redmine Tracker (e.g., Bug, Feature)."""
    id: int = Field(..., description="Tracker ID")
    name: str = Field(..., description="Tracker name")

class RedmineStatus(BaseModel):
    """Represents an Issue Status."""
    id: int = Field(..., description="Status ID")
    name: str = Field(..., description="Status name")
    is_closed: bool = Field(False, description="Whether this status means the issue is closed")

class RedminePriority(BaseModel):
    """Represents an Issue Priority."""
    id: int = Field(..., description="Priority ID")
    name: str = Field(..., description="Priority name")

class RedmineIssue(BaseModel):
    """Represents a Redmine Issue."""
    id: int = Field(..., description="Issue ID")
    project: RedmineProject = Field(..., description="Project this issue belongs to")
    tracker: RedmineTracker = Field(..., description="Tracker type")
    status: RedmineStatus = Field(..., description="Current status")
    priority: RedminePriority = Field(..., description="Priority level")
    author: Optional[RedmineUser] = Field(None, description="Issue author")
    assigned_to: Optional[RedmineUser] = Field(None, description="Assigned user")
    subject: str = Field(..., description="Issue subject")
    description: Optional[str] = Field(None, description="Issue description")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    due_date: Optional[str] = Field(None, description="Due date (YYYY-MM-DD)")
    done_ratio: int = Field(0, description="Percent complete")
    created_on: datetime = Field(..., description="Creation timestamp")
    updated_on: Optional[datetime] = Field(None, description="Last update timestamp")

class RedmineWikiPage(BaseModel):
    """Represents a Redmine Wiki Page."""
    title: str = Field(..., description="Wiki page title")
    text: Optional[str] = Field(None, description="Content of the wiki page")
    version: Optional[int] = Field(None, description="Wiki page version")
    author: Optional[RedmineUser] = Field(None, description="Last author")
    created_on: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_on: Optional[datetime] = Field(None, description="Last update timestamp")
