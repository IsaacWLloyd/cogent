"""
Tests for search endpoints.
"""

import pytest
from fastapi import status


def test_search_documents(client, test_user, test_project, test_document, auth_headers):
    """Test searching documents"""
    search_data = {
        "query": "test",
        "limit": 10,
        "offset": 0
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/search",
        json=search_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert "results" in data["data"]
    assert "total" in data["data"]
    assert "query" in data["data"]
    assert data["data"]["query"] == search_data["query"]


def test_search_with_results(client, test_user, test_project, test_document, auth_headers):
    """Test search that should return results"""
    search_data = {
        "query": "hello world",  # This should match our test document
        "limit": 5
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/search",
        json=search_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should find our test document
    assert len(data["data"]["results"]) >= 1
    
    # Check result structure
    result = data["data"]["results"][0]
    assert "documentId" in result
    assert "filePath" in result
    assert "content" in result
    assert "relevanceScore" in result
    assert 0 <= result["relevanceScore"] <= 1


def test_search_no_results(client, test_user, test_project, test_document, auth_headers):
    """Test search with no results"""
    search_data = {
        "query": "nonexistenttermalskdjalskdj"
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/search",
        json=search_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["results"] == []
    assert data["data"]["total"] == 0


def test_search_project_not_found(client, auth_headers):
    """Test search on non-existent project"""
    fake_id = "00000000-0000-0000-0000-000000000000"
    search_data = {"query": "test"}
    
    response = client.post(
        f"/api/v1/projects/{fake_id}/search",
        json=search_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND