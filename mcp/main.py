"""
PydanticAI MCP Server entry point for Vercel
Handles documentation search and context injection
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from typing import Optional

# Add shared module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.models import (
    ContextRequest, ContextResponse, DocumentContext, ApiError
)

# Create FastAPI app for MCP server
app = FastAPI(
    title="COGENT MCP Server",
    description="PydanticAI MCP Server for documentation search and context injection",
    version="1.0.0",
    docs_url="/mcp/docs",
    redoc_url="/mcp/redoc",
    openapi_url="/mcp/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication dependency
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify API key for MCP server access"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # TODO: Implement actual API key verification against database
    # For now, just check if key is provided
    if len(x_api_key) < 32:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key

# Health check endpoint
@app.get("/mcp/health")
async def health_check():
    return {"status": "healthy", "service": "cogent-mcp"}

# Root endpoint
@app.get("/mcp")
async def root():
    return {
        "message": "COGENT MCP Server",
        "version": "1.0.0",
        "docs": "/mcp/docs"
    }

# Context search endpoint
@app.post("/mcp/context", response_model=ContextResponse)
async def search_context(
    request: ContextRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Search for relevant documentation context
    This is the main MCP endpoint that Claude Code will call
    """
    try:
        # TODO: Implement actual document search using PydanticAI
        # For now, return mock response
        
        contexts = [
            DocumentContext(
                project_id=request.project_id,
                file_path="src/example.py",
                content="# Example Python file\ndef example_function():\n    pass",
                summary="Example Python file with a simple function",
                relevance_score=0.95
            )
        ]
        
        return ContextResponse(
            contexts=contexts,
            total_found=len(contexts)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Context search failed: {str(e)}"
        )

# Document validation endpoint
@app.post("/mcp/validate")
async def validate_document_relevance(
    document_id: str,
    query: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Validate if a document is relevant to a query using PydanticAI
    Used for relevance scoring during search
    """
    try:
        # TODO: Implement PydanticAI relevance validation
        
        return {
            "document_id": document_id,
            "query": query,
            "is_relevant": True,
            "relevance_score": 0.85,
            "reasoning": "Document contains relevant information about the query topic"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document validation failed: {str(e)}"
        )

# MCP tools registration endpoint
@app.get("/mcp/tools")
async def list_mcp_tools():
    """List available MCP tools for Claude Code integration"""
    return {
        "tools": [
            {
                "name": "search_context",
                "description": "Search for relevant documentation context",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "project_id": {"type": "string"},
                        "query": {"type": "string"},
                        "max_results": {"type": "integer", "default": 10}
                    },
                    "required": ["project_id", "query"]
                }
            },
            {
                "name": "validate_relevance",
                "description": "Validate document relevance to a query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "query": {"type": "string"}
                    },
                    "required": ["document_id", "query"]
                }
            }
        ]
    }

# Vercel serverless function handler
def handler(request, context):
    """Vercel serverless function entry point"""
    return app(request, context)

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)