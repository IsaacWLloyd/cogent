"""
Vercel serverless function for waitlist endpoint
Handles POST /api/v1/waitlist directly
"""

import json
import os
from http.server import BaseHTTPRequestHandler
import asyncpg
import asyncio
from typing import Dict, Any

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to add email to waitlist"""
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON
            request_data = json.loads(post_data.decode('utf-8'))
            email = request_data.get('email')
            
            if not email:
                response = {
                    "success": False,
                    "message": "Email is required"
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Run async database operation
            result = asyncio.run(self.add_to_waitlist(email))
            
            # Send response
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            error_response = {
                "success": False,
                "message": f"Server error: {str(e)}"
            }
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    async def add_to_waitlist(self, email: str) -> Dict[str, Any]:
        """Add email to waitlist database
        
        This function handles database operations for the waitlist
        """
        
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return {
                "success": False,
                "message": "Database not configured"
            }
        
        try:
            conn = await asyncpg.connect(database_url)
            
            # Extract request metadata
            ip_address = self.headers.get('x-forwarded-for') or self.client_address[0]
            user_agent = self.headers.get('user-agent')
            
            # Insert into waitlist with conflict handling
            result = await conn.fetch("""
                INSERT INTO waitlist (email, source, ip_address, user_agent)
                VALUES ($1, 'landing-page', $2, $3)
                ON CONFLICT (email) DO NOTHING
                RETURNING id
            """, email, ip_address, user_agent)
            
            await conn.close()
            
            if len(result) == 0:
                # Email already exists
                return {
                    "success": True,
                    "message": "You're already on the waitlist!"
                }
            
            return {
                "success": True,
                "message": "Successfully added to waitlist"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "Failed to add to waitlist"
            }