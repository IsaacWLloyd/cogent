"""
Waitlist API endpoints using raw SQL (like cogent-landing)
Simple and fast for serverless deployment
"""

import os
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, EmailStr
import asyncpg
from typing import List, Dict, Any

router = APIRouter()

# Database connection helper
async def get_db_connection():
    """Get database connection using asyncpg (like Neon serverless driver)"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=500, detail="Database not configured")
    
    try:
        conn = await asyncpg.connect(database_url)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Request/Response models
class WaitlistRequest(BaseModel):
    email: EmailStr

class WaitlistResponse(BaseModel):
    success: bool
    message: str

class AdminWaitlistResponse(BaseModel):
    total: int
    emails: List[Dict[str, Any]]

@router.post("/waitlist", response_model=WaitlistResponse)
async def add_to_waitlist(request: WaitlistRequest, req: Request):
    """Add email to waitlist (matches cogent-landing functionality)"""
    
    conn = await get_db_connection()
    
    try:
        # Extract request metadata (same as cogent-landing)
        ip_address = req.headers.get('x-forwarded-for') or req.client.host if req.client else None
        user_agent = req.headers.get('user-agent')
        
        # Insert into waitlist with conflict handling (same SQL as cogent-landing)
        result = await conn.fetch("""
            INSERT INTO waitlist (email, source, ip_address, user_agent)
            VALUES ($1, 'landing-page', $2, $3)
            ON CONFLICT (email) DO NOTHING
            RETURNING id
        """, request.email, ip_address, user_agent)
        
        if len(result) == 0:
            # Email already exists (same response as cogent-landing)
            return WaitlistResponse(
                success=True,
                message="You're already on the waitlist!"
            )
        
        return WaitlistResponse(
            success=True,
            message="Successfully added to waitlist"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to add to waitlist"
        )
    finally:
        await conn.close()

@router.get("/waitlist/admin", response_model=AdminWaitlistResponse)
async def get_waitlist_admin(password: str):
    """Get waitlist entries for admin (same as cogent-landing)"""
    
    # Simple password protection (same as cogent-landing)
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password or password != admin_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    conn = await get_db_connection()
    
    try:
        # Get all waitlist entries (same query as cogent-landing)
        emails = await conn.fetch("""
            SELECT email, created_at, source, ip_address
            FROM waitlist 
            ORDER BY created_at DESC
        """)
        
        # Get total count
        count_result = await conn.fetchval("SELECT COUNT(*) FROM waitlist")
        
        # Format response (same structure as cogent-landing)
        formatted_emails = [
            {
                "email": row["email"],
                "created_at": row["created_at"].isoformat(),
                "source": row["source"],
                "ip_address": row["ip_address"]
            }
            for row in emails
        ]
        
        return AdminWaitlistResponse(
            total=count_result,
            emails=formatted_emails
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch waitlist"
        )
    finally:
        await conn.close()