"""
Users router for COGENT API.
Handles user profile and usage statistics.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.responses import (
    success_response, error_response, not_found_error_response
)
from shared.models import User, UpdateUserRequest, UsageStats, DailyUsage
from models import User as UserModel, Usage as UsageModel, Project as ProjectModel, Document as DocumentModel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/user/profile")
async def get_user_profile(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    logger.info(f"Getting profile for user: {current_user.user_id}")
    
    try:
        # Get user from database
        user_model = db.query(UserModel).filter(UserModel.id == current_user.user_id).first()
        
        if not user_model:
            logger.warning(f"User not found in database: {current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("User")
            )
        
        # Convert to response format
        user = User(
            id=str(user_model.id),
            email=user_model.email,
            name=user_model.name,
            githubId=user_model.github_id,
            googleId=user_model.google_id,
            createdAt=user_model.created_at
        )
        
        logger.info(f"Retrieved profile for user {current_user.user_id}")
        
        return success_response(user.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to get user profile")
        )


@router.put("/user/profile")
async def update_user_profile(
    request: UpdateUserRequest,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    logger.info(f"Updating profile for user: {current_user.user_id}")
    
    try:
        # Get user from database
        user_model = db.query(UserModel).filter(UserModel.id == current_user.user_id).first()
        
        if not user_model:
            logger.warning(f"User not found in database: {current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_error_response("User")
            )
        
        # Update fields
        update_data = request.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user_model, field, value)
        
        db.commit()
        db.refresh(user_model)
        
        # Convert to response format
        user = User(
            id=str(user_model.id),
            email=user_model.email,
            name=user_model.name,
            githubId=user_model.github_id,
            googleId=user_model.google_id,
            createdAt=user_model.created_at
        )
        
        logger.info(f"Updated profile for user {current_user.user_id}")
        
        return success_response(user.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user profile: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to update user profile")
        )


@router.get("/user/usage")
async def get_user_usage(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    from_date: Optional[datetime] = Query(None, alias="from"),
    to_date: Optional[datetime] = Query(None, alias="to")
):
    """Get user's usage statistics"""
    logger.info(f"Getting usage stats for user: {current_user.user_id}")
    
    try:
        # Get user's projects
        user_projects = db.query(ProjectModel.id).filter(
            ProjectModel.user_id == current_user.user_id
        ).subquery()
        
        # Base usage query
        usage_query = db.query(UsageModel).filter(
            UsageModel.project_id.in_(user_projects)
        )
        
        # Apply date filters if provided
        if from_date:
            usage_query = usage_query.filter(UsageModel.timestamp >= from_date)
        if to_date:
            usage_query = usage_query.filter(UsageModel.timestamp <= to_date)
        
        # Calculate total stats
        total_stats = usage_query.with_entities(
            func.sum(UsageModel.tokens_used).label('total_tokens'),
            func.sum(UsageModel.cost).label('total_cost'),
            func.sum(func.case([(UsageModel.operation_type == 'document_generation', 1)], else_=0)).label('documents_generated'),
            func.sum(func.case([(UsageModel.operation_type == 'search', 1)], else_=0)).label('searches_performed')
        ).first()
        
        # Get daily usage if date range is specified
        daily_usage = []
        if from_date and to_date:
            daily_stats = usage_query.with_entities(
                func.date(UsageModel.timestamp).label('date'),
                func.sum(UsageModel.tokens_used).label('tokens'),
                func.sum(UsageModel.cost).label('cost')
            ).group_by(func.date(UsageModel.timestamp)).order_by(func.date(UsageModel.timestamp)).all()
            
            daily_usage = [
                DailyUsage(
                    date=stat.date.isoformat(),
                    tokens=int(stat.tokens or 0),
                    cost=float(stat.cost or 0.0)
                ) for stat in daily_stats
            ]
        
        # Create response
        usage_stats = UsageStats(
            totalTokens=int(total_stats.total_tokens or 0),
            totalCost=float(total_stats.total_cost or 0.0),
            documentsGenerated=int(total_stats.documents_generated or 0),
            searchesPerformed=int(total_stats.searches_performed or 0),
            dailyUsage=daily_usage if daily_usage else None
        )
        
        logger.info(f"Retrieved usage stats for user {current_user.user_id}")
        
        return success_response(usage_stats.dict())
        
    except Exception as e:
        logger.error(f"Error getting usage stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Failed to get usage statistics")
        )