"""
Mock data generator for COGENT development and testing
Generates realistic test data for all entities as specified in PHASE0_SPEC.md
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
import random

fake = Faker()

# Sample code content for different file types
SAMPLE_CODE = {
    "python": {
        "auth.py": '''"""
Authentication utilities for the application.
Handles user login, logout, and session management.
"""

from flask import session, request, redirect, url_for
from werkzeug.security import check_password_hash
import jwt

class AuthManager:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def login_user(self, username: str, password: str) -> bool:
        """
        Authenticate user with username and password.
        Returns True if authentication successful.
        """
        # Implementation here
        pass
    
    def generate_token(self, user_id: str) -> str:
        """Generate JWT token for authenticated user."""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
''',
        "database.py": '''"""
Database connection and ORM models.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

def init_db(database_url: str):
    """Initialize database connection."""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
''',
        "utils.py": '''"""
Utility functions used across the application.
"""

import hashlib
import secrets
from typing import Optional

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest() + ':' + salt

def verify_password(password: str, hash_with_salt: str) -> bool:
    """Verify password against hash."""
    hash_part, salt = hash_with_salt.rsplit(':', 1)
    return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part

def generate_api_key() -> str:
    """Generate secure API key."""
    return secrets.token_urlsafe(32)
''',
    },
    "javascript": {
        "auth.js": '''/**
 * Authentication module for frontend
 * Handles login, logout, and token management
 */

class AuthService {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
        this.token = localStorage.getItem('token');
    }

    async login(provider, code) {
        const response = await fetch(`${this.apiUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ provider, code })
        });
        
        if (response.ok) {
            const data = await response.json();
            this.token = data.token;
            localStorage.setItem('token', this.token);
            return data.user;
        }
        throw new Error('Login failed');
    }

    logout() {
        this.token = null;
        localStorage.removeItem('token');
    }

    isAuthenticated() {
        return !!this.token;
    }
}

export default AuthService;
''',
        "api.js": '''/**
 * API client for communicating with backend
 */

class ApiClient {
    constructor(baseUrl, authService) {
        this.baseUrl = baseUrl;
        this.authService = authService;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        if (this.authService.token) {
            config.headers.Authorization = `Bearer ${this.authService.token}`;
        }

        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        return response.json();
    }

    async getProjects() {
        return this.request('/projects');
    }

    async createProject(projectData) {
        return this.request('/projects', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }
}

export default ApiClient;
''',
        "components/Button.jsx": '''/**
 * Reusable button component
 */

import React from 'react';
import PropTypes from 'prop-types';

const Button = ({ 
    children, 
    variant = 'primary', 
    size = 'medium',
    disabled = false,
    onClick,
    ...props 
}) => {
    const baseClasses = 'btn font-medium rounded focus:outline-none';
    const variantClasses = {
        primary: 'bg-blue-500 hover:bg-blue-600 text-white',
        secondary: 'bg-gray-500 hover:bg-gray-600 text-white',
        outline: 'border border-blue-500 text-blue-500 hover:bg-blue-50'
    };
    const sizeClasses = {
        small: 'px-3 py-1 text-sm',
        medium: 'px-4 py-2',
        large: 'px-6 py-3 text-lg'
    };

    const className = [
        baseClasses,
        variantClasses[variant],
        sizeClasses[size],
        disabled ? 'opacity-50 cursor-not-allowed' : ''
    ].join(' ');

    return (
        <button 
            className={className}
            disabled={disabled}
            onClick={onClick}
            {...props}
        >
            {children}
        </button>
    );
};

Button.propTypes = {
    children: PropTypes.node.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary', 'outline']),
    size: PropTypes.oneOf(['small', 'medium', 'large']),
    disabled: PropTypes.bool,
    onClick: PropTypes.func
};

export default Button;
''',
    }
}

# Sample documentation content
SAMPLE_DOCS = {
    "auth.py": """# Authentication Module

## Purpose
This module handles all authentication-related functionality including user login, logout, session management, and JWT token generation.

## Key Classes
- `AuthManager`: Main authentication class that handles user verification and token generation

## Key Functions
- `login_user()`: Authenticates user credentials against the database
- `generate_token()`: Creates JWT tokens for authenticated sessions
- `verify_token()`: Validates JWT tokens for protected routes

## Dependencies
- `flask`: Web framework for session management
- `jwt`: JSON Web Token library for token handling
- `werkzeug.security`: Password hashing utilities

## Usage Example
```python
auth_manager = AuthManager(secret_key="your-secret-key")
if auth_manager.login_user(username, password):
    token = auth_manager.generate_token(user_id)
```

## Security Considerations
- Passwords are never stored in plain text
- JWT tokens have 24-hour expiration
- Session data is stored server-side for additional security
""",

    "database.py": """# Database Module

## Purpose
Defines ORM models and database connection logic using SQLAlchemy. Handles all database operations and schema definitions.

## Key Models
- `User`: Represents application users with authentication data
- `Base`: SQLAlchemy declarative base for all models

## Key Functions
- `init_db()`: Initializes database connection and creates tables

## Database Schema
### Users Table
- `id`: Primary key (Integer)
- `username`: Unique username (String, 80 chars)
- `email`: User email address (String, 120 chars)
- `created_at`: Account creation timestamp

## Dependencies
- `sqlalchemy`: ORM and database toolkit
- Standard datetime library for timestamps

## Connection
Supports multiple database backends through SQLAlchemy engine configuration.
""",

    "auth.js": """# Frontend Authentication Service

## Purpose
Client-side authentication service that manages user login/logout flows, token storage, and authentication state.

## Key Classes
- `AuthService`: Main authentication service class

## Key Methods
- `login()`: Handles OAuth provider authentication
- `logout()`: Clears authentication tokens and session
- `isAuthenticated()`: Checks if user is currently logged in

## OAuth Flow
1. User initiates login with provider (GitHub/Google)
2. OAuth code received from provider
3. Code sent to backend for token exchange
4. JWT token stored in localStorage

## Token Management
- Tokens stored in browser localStorage
- Automatic token inclusion in API requests
- Token validation on page load

## Dependencies
- Modern browser fetch API
- localStorage for token persistence

## Usage
```javascript
const auth = new AuthService('https://api.example.com');
const user = await auth.login('github', authCode);
```
""",

    "api.js": """# API Client Module

## Purpose
Centralized HTTP client for making authenticated requests to the backend API. Handles request configuration, authentication headers, and error handling.

## Key Classes
- `ApiClient`: Main API client with authentication integration

## Key Methods
- `request()`: Generic HTTP request method with auth handling
- `getProjects()`: Fetches user's projects
- `createProject()`: Creates new project

## Authentication
- Automatically includes Bearer token in requests
- Integrates with AuthService for token management
- Handles 401 responses for token refresh

## Error Handling
- Throws descriptive errors for failed requests
- Includes HTTP status codes in error messages
- Automatic JSON parsing for successful responses

## Usage
```javascript
const api = new ApiClient(baseUrl, authService);
const projects = await api.getProjects();
```

## Request Flow
1. Construct full URL from baseUrl + endpoint
2. Add authentication headers if token available
3. Send request with fetch API
4. Parse JSON response or throw error
""",
}

def generate_user_data() -> Dict[str, Any]:
    """Generate mock user data"""
    user_id = str(uuid.uuid4())
    return {
        "id": user_id,
        "email": fake.email(),
        "name": fake.name(),
        "github_id": str(fake.random_int(min=100000, max=9999999)),
        "google_id": None,
        "created_at": fake.date_time_between(start_date='-1y', end_date='now')
    }

def generate_project_data(user_id: str) -> Dict[str, Any]:
    """Generate mock project data"""
    project_names = [
        "E-commerce Platform",
        "Task Management API", 
        "Data Analytics Dashboard",
        "Chat Application",
        "File Storage Service"
    ]
    
    return {
        "id": str(uuid.uuid4()),
        "name": random.choice(project_names),
        "user_id": user_id,
        "repo_url": f"https://github.com/{fake.user_name()}/{fake.slug()}",
        "api_key": str(uuid.uuid4()),
        "created_at": fake.date_time_between(start_date='-6m', end_date='now')
    }

def generate_document_data(project_id: str, file_type: str = "python") -> Dict[str, Any]:
    """Generate mock document data"""
    file_extensions = {
        "python": [".py"],
        "javascript": [".js", ".jsx", ".ts", ".tsx"]
    }
    
    # Select random file from samples
    files = list(SAMPLE_CODE[file_type].keys())
    selected_file = random.choice(files)
    ext = random.choice(file_extensions[file_type])
    
    # Use file extension if not already present
    if not selected_file.endswith(tuple(file_extensions[file_type])):
        file_path = f"src/{selected_file}{ext}"
    else:
        file_path = f"src/{selected_file}"
    
    content = SAMPLE_CODE[file_type][selected_file]
    summary = SAMPLE_DOCS.get(selected_file, f"Documentation for {selected_file}")
    
    return {
        "id": str(uuid.uuid4()),
        "project_id": project_id,
        "file_path": file_path,
        "content": content,
        "summary": summary,
        "created_at": fake.date_time_between(start_date='-3m', end_date='now'),
        "updated_at": fake.date_time_between(start_date='-1m', end_date='now')
    }

def generate_search_index_data(document_id: str, content: str) -> Dict[str, Any]:
    """Generate mock search index data"""
    return {
        "id": str(uuid.uuid4()),
        "document_id": document_id,
        "content_vector": None,  # Would be generated by embedding service
        "full_text": content
    }

def generate_complete_dataset() -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate complete mock dataset as specified:
    - 1 test user
    - 2-3 test projects
    - 10-20 documents per project
    """
    dataset = {
        "users": [],
        "projects": [],
        "documents": [],
        "search_indexes": []
    }
    
    # Generate 1 test user
    user = generate_user_data()
    dataset["users"].append(user)
    
    # Generate 2-3 projects for the user
    num_projects = random.randint(2, 3)
    for _ in range(num_projects):
        project = generate_project_data(user["id"])
        dataset["projects"].append(project)
        
        # Generate 10-20 documents per project
        num_docs = random.randint(10, 20)
        file_type = random.choice(["python", "javascript"])
        
        for _ in range(num_docs):
            document = generate_document_data(project["id"], file_type)
            dataset["documents"].append(document)
            
            # Generate search index for each document
            search_index = generate_search_index_data(
                document["id"], 
                document["content"]
            )
            dataset["search_indexes"].append(search_index)
    
    return dataset

def generate_search_results(query: str, documents: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
    """Generate mock search results for a given query"""
    # Simple keyword matching for mock data
    query_words = query.lower().split()
    results = []
    
    for doc in documents:
        # Calculate simple relevance score based on keyword matches
        content_lower = doc["content"].lower()
        matches = sum(1 for word in query_words if word in content_lower)
        
        if matches > 0:
            relevance_score = min(matches / len(query_words), 1.0)
            
            # Extract relevant excerpt (first 200 chars containing query terms)
            excerpt_start = 0
            for word in query_words:
                pos = content_lower.find(word)
                if pos != -1:
                    excerpt_start = max(0, pos - 50)
                    break
            
            excerpt = doc["content"][excerpt_start:excerpt_start + 200]
            if excerpt_start > 0:
                excerpt = "..." + excerpt
            if len(doc["content"]) > excerpt_start + 200:
                excerpt += "..."
            
            results.append({
                "document_id": doc["id"],
                "file_path": doc["file_path"],
                "content": excerpt,
                "relevance_score": relevance_score
            })
    
    # Sort by relevance score and return top results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:limit]

if __name__ == "__main__":
    # Generate and print sample dataset
    dataset = generate_complete_dataset()
    
    print("Generated Mock Dataset:")
    print(f"Users: {len(dataset['users'])}")
    print(f"Projects: {len(dataset['projects'])}")
    print(f"Documents: {len(dataset['documents'])}")
    print(f"Search Indexes: {len(dataset['search_indexes'])}")
    
    # Test search functionality
    test_query = "authentication"
    results = generate_search_results(test_query, dataset["documents"])
    print(f"\nSearch results for '{test_query}': {len(results)} found")