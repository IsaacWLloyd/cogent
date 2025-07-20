"""
Tests for project endpoints.
"""

import pytest
from fastapi import status


def test_list_projects_authenticated(client, test_user, test_project, auth_headers):
    """Test listing projects for authenticated user"""
    response = client.get("/api/v1/projects", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert "projects" in data["data"]
    assert "total" in data["data"]
    assert len(data["data"]["projects"]) >= 1


def test_list_projects_unauthenticated(client):
    """Test listing projects without authentication"""
    response = client.get("/api/v1/projects")
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_project(client, test_user, auth_headers):
    """Test creating new project"""
    project_data = {
        "name": "New Test Project",
        "repoUrl": "https://github.com/test/new-repo"
    }
    
    response = client.post("/api/v1/projects", json=project_data, headers=auth_headers)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    assert data["data"] is not None
    assert data["data"]["name"] == project_data["name"]
    assert data["data"]["repoUrl"] == project_data["repoUrl"]
    assert "apiKey" in data["data"]


def test_get_project(client, test_user, test_project, auth_headers):
    """Test getting project details"""
    response = client.get(f"/api/v1/projects/{test_project.id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert data["data"]["id"] == str(test_project.id)
    assert data["data"]["name"] == test_project.name


def test_get_project_not_found(client, auth_headers):
    """Test getting non-existent project"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/projects/{fake_id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_project(client, test_user, test_project, auth_headers):
    """Test updating project"""
    update_data = {"name": "Updated Project Name"}
    
    response = client.put(
        f"/api/v1/projects/{test_project.id}", 
        json=update_data, 
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["name"] == update_data["name"]


def test_delete_project(client, test_user, test_project, auth_headers):
    """Test deleting project"""
    response = client.delete(f"/api/v1/projects/{test_project.id}", headers=auth_headers)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT