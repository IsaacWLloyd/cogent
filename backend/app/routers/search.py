"""
Search router for COGENT API.
Handles document search operations.
"""

import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.core.auth import get_current_user, TokenData
from app.core.responses import (
    success_response, error_response, not_found_error_response
)
from shared.models import SearchRequest, SearchResult, SearchResponse
from models import Project as ProjectModel, Document as DocumentModel, SearchIndex as SearchIndexModel

logger = logging.getLogger(__name__)

router = APIRouter()


def perform_fulltext_search(
    db: Session, 
    project_id: UUID, 
    query: str, 
    limit: int, 
    offset: int
) -> List[SearchResult]:
    """
    Perform full-text search on documents.
    Basic implementation using SQL LIKE for now.
    Team 4 will enhance with proper full-text search and vector search.
    """
    logger.info(f"Performing full-text search for query: {query}")
    
    # Simple keyword search using LIKE
    # This is a basic implementation - Team 4 will add proper FTS
    query_words = query.lower().split()
    
    # Build search query
    search_conditions = []
    params = {"project_id": str(project_id)}
    
    for i, word in enumerate(query_words):
        param_name = f"word_{i}"
        search_conditions.append(f"LOWER(si.full_text) LIKE :{param_name}")
        params[param_name] = f"%{word}%"
    
    where_clause = " AND ".join(search_conditions)
    
    sql_query = f"""
    SELECT 
        d.id as document_id,
        d.file_path,
        d.content,
        d.summary,
        -- Simple relevance scoring based on keyword matches
        (LENGTH(LOWER(si.full_text)) - LENGTH(REPLACE(LOWER(si.full_text), :query_lower, ''))) / LENGTH(:query_lower) as relevance_score
    FROM documents d
    JOIN search_indexes si ON d.id = si.document_id
    WHERE d.project_id = :project_id
    AND ({where_clause})
    ORDER BY relevance_score DESC, d.updated_at DESC
    LIMIT :limit OFFSET :offset
    """
    
    params["query_lower"] = query.lower()
    params["limit"] = limit
    params["offset"] = offset
    
    try:
        result = db.execute(text(sql_query), params)
        rows = result.fetchall()
        
        search_results = []
        for row in rows:
            # Extract relevant excerpt (first 200 chars containing query terms)
            content = row.content
            excerpt = extract_relevant_excerpt(content, query_words)
            
            # Calculate simple relevance score (0-1)
            relevance_score = min(1.0, max(0.1, float(row.relevance_score or 0) / 10))
            
            search_result = SearchResult(
                documentId=str(row.document_id),
                filePath=row.file_path,
                content=excerpt,
                relevanceScore=relevance_score
            )
            search_results.append(search_result)
        
        return search_results
        
    except Exception as e:
        logger.error(f"Search query error: {e}")
        return []


def extract_relevant_excerpt(content: str, query_words: List[str], max_length: int = 200) -> str:
    """
    Extract relevant excerpt from content containing query words.
    """
    content_lower = content.lower()
    
    # Find first occurrence of any query word
    best_start = 0
    for word in query_words:
        pos = content_lower.find(word.lower())
        if pos != -1:
            best_start = max(0, pos - 50)
            break
    
    # Extract excerpt
    excerpt = content[best_start:best_start + max_length]
    
    # Add ellipsis if truncated
    if best_start > 0:
        excerpt = "..." + excerpt
    if len(content) > best_start + max_length:
        excerpt = excerpt + "..."
    
    return excerpt


@router.post("/projects/{project_id}/search")
async def search_documents(
    project_id: UUID,
    request: SearchRequest,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Search documents within a project.
    Basic implementation using full-text search.
    """
    logger.info(f"Searching documents in project {project_id} for: {request.query}")
    
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
        
        # Perform search
        search_results = perform_fulltext_search(
            db=db,
            project_id=project_id,
            query=request.query,
            limit=request.limit,
            offset=request.offset
        )
        
        # Get total count for the same query (without limit/offset)
        total_results = perform_fulltext_search(
            db=db,
            project_id=project_id,
            query=request.query,
            limit=1000,  # Large limit to count all
            offset=0
        )
        total = len(total_results)
        
        response = SearchResponse(
            results=search_results,
            total=total,
            query=request.query
        )
        
        logger.info(f"Search returned {len(search_results)} results out of {total} total")
        
        return success_response(response.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching documents: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_response("INTERNAL_ERROR", "Search failed")
        )