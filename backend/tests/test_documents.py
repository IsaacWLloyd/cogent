"""
Tests for document endpoints.
"""

import pytest
from fastapi import status


def test_list_documents(client, test_user, test_project, test_document, auth_headers):
    """Test listing project documents"""
    response = client.get(f"/api/v1/projects/{test_project.id}/documents", headers=auth_headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert "documents" in data["data"]
    assert len(data["data"]["documents"]) >= 1


def test_create_document(client, test_user, test_project, auth_headers):
    """Test creating new document"""
    doc_data = {
        "filePath": "src/new_file.py",
        "content": "# New Python file\nprint('new file')",
        "summary": "New test file"
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/documents",
        json=doc_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"] is not None
    assert data["data"]["filePath"] == doc_data["filePath"]
    assert data["data"]["content"] == doc_data["content"]


def test_update_existing_document(client, test_user, test_project, test_document, auth_headers):
    """Test updating existing document"""
    doc_data = {
        "filePath": test_document.file_path,  # Same path
        "content": "# Updated content\nprint('updated')",
        "summary": "Updated test file"
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/documents",
        json=doc_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["data"]["content"] == doc_data["content"]
    assert data["data"]["summary"] == doc_data["summary"]


def test_create_document_invalid_path(client, test_user, test_project, auth_headers):
    """Test creating document with invalid file path"""
    doc_data = {
        "filePath": "../../../etc/passwd",  # Path traversal attempt
        "content": "malicious content",
        "summary": "Bad file"
    }
    
    response = client.post(
        f"/api/v1/projects/{test_project.id}/documents",
        json=doc_data,
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_documents_with_path_filter(client, test_user, test_project, test_document, auth_headers):
    """Test listing documents with path filter"""
    response = client.get(
        f"/api/v1/projects/{test_project.id}/documents?path=src/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Should include our test document
    assert len(data["data"]["documents"]) >= 1
    assert all(doc["filePath"].startswith("src/") for doc in data["data"]["documents"])