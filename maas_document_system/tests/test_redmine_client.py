import pytest
import requests_mock
from maas_document_system.tools.redmine_client import RedmineClient, RedmineHttpError
from maas_document_system.schemas.redmine import RedmineProject, RedmineIssue
import os

@pytest.fixture
def redmine_client():
    return RedmineClient(base_url="https://redmine.test", api_key="dummy")

def test_list_projects_pagination(redmine_client):
    with requests_mock.Mocker() as m:
        # Page 1
        m.get("https://redmine.test/projects.json?limit=100&offset=0", json={
            "projects": [{"id": 1, "name": "P1", "identifier": "p1", "status": 1}] * 100,
            "total_count": 150,
            "limit": 100,
            "offset": 0
        })
        # Page 2
        m.get("https://redmine.test/projects.json?limit=100&offset=100", json={
            "projects": [{"id": 2, "name": "P2", "identifier": "p2", "status": 1}] * 50,
            "total_count": 150,
            "limit": 100,
            "offset": 100
        })
        
        projects = redmine_client.list_projects()
        assert len(projects) == 150
        assert isinstance(projects[0], RedmineProject)

def test_get_project(redmine_client):
    with requests_mock.Mocker() as m:
        m.get("https://redmine.test/projects/1.json", json={
            "project": {"id": 1, "name": "P1", "identifier": "p1", "status": 1}
        })
        
        project = redmine_client.get_project(1)
        assert project.id == 1
        assert project.name == "P1"

def test_http_error_handling(redmine_client):
    with requests_mock.Mocker() as m:
        m.get("https://redmine.test/projects/999.json", status_code=404)
        
        with pytest.raises(RedmineHttpError) as exc:
            redmine_client.get_project(999)
        assert exc.value.status_code == 404

def test_auth_headers(redmine_client):
    with requests_mock.Mocker() as m:
        m.get("https://redmine.test/users.json?limit=100&offset=0", json={"users": []})
        
        redmine_client.list_users()
        
        last_request = m.last_request
        assert last_request.headers["X-Redmine-API-Key"] == "dummy"
