"""
Documents router for COGENT API.
Handles document creation and retrieval operations.
"""

import logging
import os
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.responses import (
    success_response, error_response, not_found_error_response,
    validation_error_response
)
from shared.models import Document, CreateDocumentRequest, DocumentsResponse
from models import Project as ProjectModel, Document as DocumentModel, SearchIndex as SearchIndexModel

logger = logging.getLogger(__name__)

router = APIRouter()


def validate_file_path(file_path: str) -> bool:
    """
    Validate file path to prevent directory traversal attacks.
    Ensures path is relative and doesn't escape project root.
    """
    # Normalize path and check for directory traversal
    normalized = os.path.normpath(file_path)
    
    # Reject absolute paths
    if os.path.isabs(normalized):
        return False
    
    # Reject paths that go above current directory
    if normalized.startswith('..') or '/..' in normalized or '\\..\\' in normalized:
        return False
    
    # Additional security checks
    if any(char in normalized for char in ['<', '>', ':', '"', '|', '?', '*']):
        return False
    
    return True


@router.get("/projects/{project_id}/documents")
async def list_documents(
    project_id: UUID,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    path: Optional[str] = Query(None, description="Filter by file path prefix")
):
    """List project documents with pagination and optional path filtering"""
    logger.info(f"Listing documents for project {project_id}, user: {current_user.user_id}")
    
    try:
        # Verify project ownership
        project = db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.user_id == current_user.user_id
        ).first()
        
        if not project:
            logger.warning(f"Project not found or access denied: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("Project")
            )
        
        # Build query
        query = db.query(DocumentModel).filter(DocumentModel.project_id == project_id)
        
        # Apply path filter if provided
        if path:
            if not validate_file_path(path):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=validation_error_response({"path": "Invalid file path format"})
                )
            query = query.filter(DocumentModel.file_path.startswith(path))
        
        # Get total count
        total = query.count()
        
        # Get documents with pagination
        document_models = query.order_by(
            DocumentModel.updated_at.desc()
        ).offset(offset).limit(limit).all()
        
        # Convert to response format
        documents = []
        for doc_model in document_models:
            document = Document(
                id=str(doc_model.id),
                projectId=str(doc_model.project_id),
                filePath=doc_model.file_path,
                content=doc_model.content,
                summary=doc_model.summary,
                createdAt=doc_model.created_at,
                updatedAt=doc_model.updated_at
            )
            documents.append(document)
        
        response = DocumentsResponse(
            documents=documents,
            total=total,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Listed {len(documents)} documents for project {project_id}")
        
        return success_response(response.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing documents: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to list documents")
        )


@router.post("/projects/{project_id}/documents")
async def create_or_update_document(
    project_id: UUID,
    request: CreateDocumentRequest,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create or update document.
    If document with same file_path exists, update it. Otherwise create new one.
    """
    logger.info(f"Creating/updating document for project {project_id}, user: {current_user.user_id}")
    
    try:
        # Validate file path
        if not validate_file_path(request.filePath):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=validation_error_response({"filePath": "Invalid file path format"})
            )
        
        # Verify project ownership
        project = db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.user_id == current_user.user_id
        ).first()
        
        if not project:
            logger.warning(f"Project not found or access denied: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("Project")
            )
        
        # Check if document already exists
        existing_doc = db.query(DocumentModel).filter(
            DocumentModel.project_id == project_id,
            DocumentModel.file_path == request.filePath
        ).first()
        
        if existing_doc:
            # Update existing document
            existing_doc.content = request.content
            existing_doc.summary = request.summary
            # updated_at will be automatically set by SQLAlchemy
            
            db.commit()
            db.refresh(existing_doc)
            
            # Update search index
            search_index = db.query(SearchIndexModel).filter(
                SearchIndexModel.document_id == existing_doc.id
            ).first()
            
            if search_index:
                search_index.full_text = request.content
                # Leave content_vector as None for now (Team 4 will handle vectors)
            else:
                # Create search index if it doesn't exist
                search_index = SearchIndexModel(
                    document_id=existing_doc.id,
                    full_text=request.content,
                    content_vector=None
                )
                db.add(search_index)
            
            db.commit()
            
            # Convert to response format
            document = Document(
                id=str(existing_doc.id),
                projectId=str(existing_doc.project_id),
                filePath=existing_doc.file_path,
                content=existing_doc.content,
                summary=existing_doc.summary,
                createdAt=existing_doc.created_at,
                updatedAt=existing_doc.updated_at
            )
            
            logger.info(f"Updated document {existing_doc.id}")
            
            return success_response(document.dict())
        
        else:
            # Create new document
            doc_model = DocumentModel(
                project_id=project_id,
                file_path=request.filePath,
                content=request.content,
                summary=request.summary
            )
            
            db.add(doc_model)
            db.commit()
            db.refresh(doc_model)
            
            # Create search index
            search_index = SearchIndexModel(
                document_id=doc_model.id,
                full_text=request.content,
                content_vector=None  # Leave null for now
            )
            db.add(search_index)
            db.commit()
            
            # Convert to response format
            document = Document(
                id=str(doc_model.id),
                projectId=str(doc_model.project_id),
                filePath=doc_model.file_path,
                content=doc_model.content,
                summary=doc_model.summary,
                createdAt=doc_model.created_at,
                updatedAt=doc_model.updated_at
            )
            
            logger.info(f"Created document {doc_model.id}")
            
            # Return 201 for creation
            return success_response(document.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating/updating document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to create/update document")
        )