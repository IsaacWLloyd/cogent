"""
Waitlist API endpoints
Handles waitlist signups from the landing page
"""

import os
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import sys

# Add shared module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from shared.database import Waitlist
from shared.models import ApiError

router = APIRouter()

# Database dependency
def get_db():
    """Get database session - placeholder for now"""
    # TODO: Implement actual database session management with SQLAlchemy engine
    # This will need to be implemented when database connection is set up
    raise HTTPException(status_code=500, detail="Database not yet configured")

class WaitlistRequest(BaseModel):
    email: EmailStr

class WaitlistResponse(BaseModel):
    success: bool
    message: str

@router.post("/", response_model=WaitlistResponse)
async def add_to_waitlist(
    request: WaitlistRequest,
    req: Request,
    db: Session = Depends(get_db)
):
    """Add email to waitlist"""
    try:
        # Extract request metadata
        ip_address = req.headers.get('x-forwarded-for') or req.client.host if req.client else None
        user_agent = req.headers.get('user-agent')
        
        # Create waitlist entry
        waitlist_entry = Waitlist(
            email=request.email,
            source='landing-page',
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(waitlist_entry)
        db.commit()
        
        return WaitlistResponse(
            success=True,
            message="Successfully added to waitlist"
        )
        
    except IntegrityError:
        # Email already exists
        db.rollback()
        return WaitlistResponse(
            success=True,
            message="You're already on the waitlist!"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to add to waitlist"
        )

class AdminWaitlistResponse(BaseModel):
    total: int
    emails: list[dict]

@router.get("/admin", response_model=AdminWaitlistResponse)
async def get_waitlist_admin(
    password: str,
    db: Session = Depends(get_db)
):
    """Get waitlist entries for admin (simple password protection)"""
    
    # Simple password protection
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password or password != admin_password:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    
    try:
        # Get all waitlist entries
        waitlist_entries = (
            db.query(Waitlist)
            .order_by(Waitlist.created_at.desc())
            .all()
        )
        
        # Get total count
        total = len(waitlist_entries)
        
        # Format response
        emails = [
            {
                "email": entry.email,
                "created_at": entry.created_at.isoformat(),
                "source": entry.source,
                "ip_address": entry.ip_address
            }
            for entry in waitlist_entries
        ]
        
        return AdminWaitlistResponse(
            total=total,
            emails=emails
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch waitlist"
        )