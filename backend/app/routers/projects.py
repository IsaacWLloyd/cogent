"""
Projects router for COGENT API.
Handles project CRUD operations.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.responses import (
    success_response, error_response, not_found_error_response,
    conflict_error_response, validation_error_response
)
from shared.models import Project, CreateProjectRequest, UpdateProjectRequest, ProjectsResponse
from models import Project as ProjectModel, User as UserModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/projects")
async def list_projects(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """List user's projects with pagination"""
    logger.info(f"Listing projects for user: {current_user.user_id}")
    
    try:
        # Get total count
        total = db.query(ProjectModel).filter(
            ProjectModel.user_id == current_user.user_id
        ).count()
        
        # Get projects with pagination
        projects_query = db.query(ProjectModel).filter(
            ProjectModel.user_id == current_user.user_id
        ).order_by(ProjectModel.created_at.desc()).offset(offset).limit(limit)
        
        project_models = projects_query.all()
        
        # Convert to response format
        projects = []
        for project_model in project_models:
            project = Project(
                id=str(project_model.id),
                name=project_model.name,
                userId=str(project_model.user_id),
                repoUrl=project_model.repo_url,
                apiKey=project_model.api_key,
                createdAt=project_model.created_at
            )
            projects.append(project)
        
        response = ProjectsResponse(
            projects=projects,
            total=total,
            limit=limit,
            offset=offset
        )
        
        logger.info(f"Listed {len(projects)} projects for user {current_user.user_id}")
        
        return success_response(response.dict())
        
    except Exception as e:
        logger.error(f"Error listing projects: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to list projects")
        )


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project(
    request: CreateProjectRequest,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new project"""
    logger.info(f"Creating project '{request.name}' for user: {current_user.user_id}")
    
    try:
        # Check if user exists (for FK constraint)
        user = db.query(UserModel).filter(UserModel.id == current_user.user_id).first()
        if not user:
            logger.warning(f"User not found: {current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_response("INVALID_USER", "User not found")
            )
        
        # Create project model
        project_model = ProjectModel(
            name=request.name,
            user_id=current_user.user_id,
            repo_url=str(request.repoUrl) if request.repoUrl else None
        )
        
        db.add(project_model)
        db.commit()
        db.refresh(project_model)
        
        # Convert to response format
        project = Project(
            id=str(project_model.id),
            name=project_model.name,
            userId=str(project_model.user_id),
            repoUrl=project_model.repo_url,
            apiKey=project_model.api_key,
            createdAt=project_model.created_at
        )
        
        logger.info(f"Created project {project_model.id} for user {current_user.user_id}")
        
        return success_response(project.dict())
        
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Project creation integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=conflict_error_response("Project name already exists")
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to create project")
        )


@router.get("/projects/{project_id}")
async def get_project(
    project_id: UUID,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get project details"""
    logger.info(f"Getting project {project_id} for user: {current_user.user_id}")
    
    try:
        # Get project and verify ownership
        project_model = db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.user_id == current_user.user_id
        ).first()
        
        if not project_model:
            logger.warning(f"Project not found or access denied: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("Project")
            )
        
        # Convert to response format
        project = Project(
            id=str(project_model.id),
            name=project_model.name,
            userId=str(project_model.user_id),
            repoUrl=project_model.repo_url,
            apiKey=project_model.api_key,
            createdAt=project_model.created_at
        )
        
        logger.info(f"Retrieved project {project_id}")
        
        return success_response(project.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to get project")
        )


@router.put("/projects/{project_id}")
async def update_project(
    project_id: UUID,
    request: UpdateProjectRequest,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project"""
    logger.info(f"Updating project {project_id} for user: {current_user.user_id}")
    
    try:
        # Get project and verify ownership
        project_model = db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.user_id == current_user.user_id
        ).first()
        
        if not project_model:
            logger.warning(f"Project not found or access denied: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("Project")
            )
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "repoUrl" and value:
                setattr(project_model, "repo_url", str(value))
            elif field == "name":
                setattr(project_model, field, value)
        
        db.commit()
        db.refresh(project_model)
        
        # Convert to response format
        project = Project(
            id=str(project_model.id),
            name=project_model.name,
            userId=str(project_model.user_id),
            repoUrl=project_model.repo_url,
            apiKey=project_model.api_key,
            createdAt=project_model.created_at
        )
        
        logger.info(f"Updated project {project_id}")
        
        return success_response(project.dict())
        
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.warning(f"Project update integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=conflict_error_response("Project name already exists")
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating project: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to update project")
        )


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete project"""
    logger.info(f"Deleting project {project_id} for user: {current_user.user_id}")
    
    try:
        # Get project and verify ownership
        project_model = db.query(ProjectModel).filter(
            ProjectModel.id == project_id,
            ProjectModel.user_id == current_user.user_id
        ).first()
        
        if not project_model:
            logger.warning(f"Project not found or access denied: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("Project")
            )
        
        # Delete project (cascade will handle related documents)
        db.delete(project_model)
        db.commit()
        
        logger.info(f"Deleted project {project_id}")
        
        # 204 No Content - no response body
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting project: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to delete project")
        )