"""
Mock data generator for COGENT development and testing
Generates realistic test data for all entities according to SPRINT0_SPEC.md
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import json

# Mock data constants
PROGRAMMING_LANGUAGES = [
    'javascript', 'typescript', 'python', 'java', 'go', 'rust', 
    'cpp', 'csharp', 'php', 'ruby', 'swift', 'kotlin'
]

FILE_EXTENSIONS = {
    'javascript': ['.js', '.jsx'],
    'typescript': ['.ts', '.tsx'], 
    'python': ['.py'],
    'java': ['.java'],
    'go': ['.go'],
    'rust': ['.rs'],
    'cpp': ['.cpp', '.cc', '.cxx'],
    'csharp': ['.cs'],
    'php': ['.php'],
    'ruby': ['.rb'],
    'swift': ['.swift'],
    'kotlin': ['.kt']
}

SAMPLE_REPOS = [
    "acme-corp/web-app",
    "startupco/mobile-api", 
    "techfirm/data-pipeline",
    "devshop/e-commerce-platform",
    "innovate/ml-service"
]

SAMPLE_NAMES = [
    "Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", 
    "Emily Brown", "Frank Miller", "Grace Lee", "Henry Taylor"
]

SAMPLE_EMAILS = [
    "alice.johnson@example.com", "bob.smith@techcorp.com", 
    "carol.davis@startup.io", "david.wilson@devfirm.com",
    "emily.brown@innovate.co", "frank.miller@acme.com",
    "grace.lee@buildtech.net", "henry.taylor@codebase.org"
]

LLM_MODELS = [
    "openai/gpt-4-turbo", "openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet",
    "anthropic/claude-3-haiku", "meta-llama/llama-2-70b", "mistralai/mistral-7b"
]

API_ENDPOINTS = [
    "/api/v1/search", "/api/v1/documents", "/api/v1/projects",
    "/mcp/context", "/mcp/validate", "/api/v1/user/usage"
]


@dataclass
class MockUser:
    id: str
    clerk_id: str
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    settings_json: Dict[str, Any]
    clerk_org_id: str
    last_seen: datetime


@dataclass 
class MockProject:
    id: str
    name: str
    user_id: str
    github_repo_url: str
    created_at: datetime
    updated_at: datetime
    description: str
    visibility: str
    settings_json: Dict[str, Any]
    branch_name: str
    include_patterns: List[str]
    exclude_patterns: List[str]


@dataclass
class MockDocument:
    id: str
    project_id: str
    file_path: str
    content: str
    summary: str
    commit_hash: str
    created_at: datetime
    updated_at: datetime
    version: int
    language: str
    imports: List[str]
    exports: List[str] 
    references: List[str]


@dataclass
class MockApiKey:
    id: str
    project_id: str
    key_hash: str
    name: str
    created_at: datetime
    last_used: datetime


@dataclass
class MockUsage:
    id: str
    project_id: str
    timestamp: datetime
    operation_type: str
    tokens_used: int
    cost: float
    llm_model: str
    endpoint_called: str
    response_time: int


class MockDataGenerator:
    """Generate realistic mock data for COGENT development"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.users: List[MockUser] = []
        self.projects: List[MockProject] = []
        self.documents: List[MockDocument] = []
        self.api_keys: List[MockApiKey] = []
        self.usage_records: List[MockUsage] = []
    
    def generate_users(self, count: int = 3) -> List[MockUser]:
        """Generate mock users with Clerk integration"""
        users = []
        
        for i in range(count):
            now = datetime.now()
            created_at = now - timedelta(days=random.randint(30, 365))
            
            user = MockUser(
                id=str(uuid.uuid4()),
                clerk_id=f"user_{uuid.uuid4().hex[:12]}",
                email=SAMPLE_EMAILS[i],
                name=SAMPLE_NAMES[i],
                created_at=created_at,
                updated_at=created_at + timedelta(days=random.randint(1, 30)),
                settings_json={
                    "theme": random.choice(["light", "dark"]),
                    "notifications": random.choice([True, False]),
                    "default_visibility": random.choice(["private", "public"])
                },
                clerk_org_id=f"org_{uuid.uuid4().hex[:8]}" if random.random() > 0.5 else None,
                last_seen=now - timedelta(hours=random.randint(1, 168))
            )
            users.append(user)
            
        self.users = users
        return users
    
    def generate_projects(self, users: List[MockUser], count: int = 5) -> List[MockProject]:
        """Generate mock projects with varied configurations"""
        projects = []
        
        for i in range(count):
            user = random.choice(users)
            now = datetime.now()
            created_at = user.created_at + timedelta(days=random.randint(1, 30))
            
            project = MockProject(
                id=str(uuid.uuid4()),
                name=f"Project {i+1}",
                user_id=user.id,
                github_repo_url=f"https://github.com/{SAMPLE_REPOS[i]}",
                created_at=created_at,
                updated_at=created_at + timedelta(days=random.randint(1, 60)),
                description=f"Description for project {i+1} - a {random.choice(['web app', 'API service', 'data pipeline', 'mobile app', 'ML model'])}",
                visibility=random.choice(["private", "public"]),
                settings_json={
                    "auto_generate": random.choice([True, False]),
                    "doc_template": "default",
                    "include_tests": random.choice([True, False])
                },
                branch_name=random.choice(["main", "master", "develop"]),
                include_patterns=["**/*", "src/**/*"] if random.random() > 0.5 else ["**/*"],
                exclude_patterns=[
                    "node_modules/**", ".git/**", "dist/**", "build/**"
                ] + (["*.test.js", "*.spec.ts"] if random.random() > 0.7 else [])
            )
            projects.append(project)
            
        self.projects = projects
        return projects
    
    def generate_documents(self, projects: List[MockProject], count_per_project: int = 10) -> List[MockDocument]:
        """Generate mock documents with realistic code content"""
        documents = []
        
        code_samples = {
            'javascript': '''// Authentication utility functions
export function validateToken(token) {
    if (!token) return false;
    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        return decoded.userId;
    } catch (error) {
        return false;
    }
}

export function generateApiKey() {
    return crypto.randomBytes(32).toString('hex');
}''',
            
            'python': '''"""
Database connection and query utilities
"""
import asyncio
import asyncpg
from contextlib import asynccontextmanager

class DatabasePool:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.pool = None
    
    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.connection_url)
    
    @asynccontextmanager
    async def get_connection(self):
        async with self.pool.acquire() as conn:
            yield conn''',
            
            'typescript': '''interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

interface Project {
  id: string;
  name: string;
  userId: string;
  repoUrl: string;
}

export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }
  
  async fetchProjects(): Promise<Project[]> {
    const response = await fetch(`${this.baseUrl}/projects`);
    return response.json();
  }
}'''
        }
        
        for project in projects:
            for i in range(count_per_project):
                language = random.choice(PROGRAMMING_LANGUAGES)
                extension = random.choice(FILE_EXTENSIONS[language])
                file_path = f"src/{random.choice(['components', 'utils', 'services', 'models'])}/{random.choice(['auth', 'user', 'project', 'document', 'api'])}{extension}"
                
                document = MockDocument(
                    id=str(uuid.uuid4()),
                    project_id=project.id,
                    file_path=file_path,
                    content=code_samples.get(language, f"// {language.title()} code example\nfunction example() {{\n  return 'Hello World';\n}}"),
                    summary=f"This file contains {random.choice(['utility functions', 'API endpoints', 'data models', 'authentication logic', 'database queries'])} for {random.choice(['user management', 'project handling', 'document processing', 'search functionality'])}.",
                    commit_hash=f"{random.randint(100000, 999999):x}{uuid.uuid4().hex[:8]}",
                    created_at=project.created_at + timedelta(days=random.randint(1, 30)),
                    updated_at=project.updated_at - timedelta(days=random.randint(0, 10)),
                    version=random.randint(1, 5),
                    language=language,
                    imports=[
                        random.choice(['react', 'express', 'lodash', 'axios', 'moment', 'uuid']),
                        random.choice(['dotenv', 'cors', 'helmet', 'bcrypt', 'jsonwebtoken'])
                    ] if random.random() > 0.3 else [],
                    exports=[
                        random.choice(['validateToken', 'generateHash', 'ApiClient', 'DatabasePool']),
                        random.choice(['User', 'Project', 'Document', 'AuthService'])
                    ] if random.random() > 0.4 else [],
                    references=[
                        f"src/types/{random.choice(['user', 'project', 'api'])}.ts",
                        f"src/config/{random.choice(['database', 'auth', 'app'])}.js"
                    ] if random.random() > 0.6 else []
                )
                documents.append(document)
        
        self.documents = documents
        return documents
    
    def generate_api_keys(self, projects: List[MockProject]) -> List[MockApiKey]:
        """Generate API keys for projects"""
        api_keys = []
        
        for project in projects:
            # Each project gets 1-3 API keys
            for i in range(random.randint(1, 3)):
                key = MockApiKey(
                    id=str(uuid.uuid4()),
                    project_id=project.id,
                    key_hash=f"sk_{uuid.uuid4().hex}",
                    name=random.choice(["Production", "Development", "Testing", "MCP Server", "CI/CD"]),
                    created_at=project.created_at + timedelta(days=random.randint(1, 20)),
                    last_used=datetime.now() - timedelta(hours=random.randint(1, 720)) if random.random() > 0.2 else None
                )
                api_keys.append(key)
        
        self.api_keys = api_keys
        return api_keys
    
    def generate_usage_records(self, projects: List[MockProject], days: int = 30) -> List[MockUsage]:
        """Generate usage records for billing analytics"""
        usage_records = []
        
        for project in projects:
            # Generate 5-50 usage records per project over the past 30 days
            record_count = random.randint(5, 50)
            
            for _ in range(record_count):
                timestamp = datetime.now() - timedelta(
                    days=random.randint(0, days),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                operation_type = random.choice(["search", "generate", "mcp_call"])
                tokens_used = random.randint(100, 5000)
                
                # Cost calculation (mock pricing)
                cost_per_token = {
                    "search": 0.0001,
                    "generate": 0.0003, 
                    "mcp_call": 0.0002
                }[operation_type]
                
                usage = MockUsage(
                    id=str(uuid.uuid4()),
                    project_id=project.id,
                    timestamp=timestamp,
                    operation_type=operation_type,
                    tokens_used=tokens_used,
                    cost=round(tokens_used * cost_per_token, 6),
                    llm_model=random.choice(LLM_MODELS),
                    endpoint_called=random.choice(API_ENDPOINTS),
                    response_time=random.randint(50, 2000)
                )
                usage_records.append(usage)
        
        self.usage_records = usage_records
        return usage_records
    
    def generate_all(self) -> Dict[str, Any]:
        """Generate complete mock dataset"""
        users = self.generate_users(3)
        projects = self.generate_projects(users, 5)
        documents = self.generate_documents(projects, 12)
        api_keys = self.generate_api_keys(projects)
        usage_records = self.generate_usage_records(projects, 30)
        
        return {
            "users": [asdict(user) for user in users],
            "projects": [asdict(project) for project in projects], 
            "documents": [asdict(document) for document in documents],
            "api_keys": [asdict(api_key) for api_key in api_keys],
            "usage_records": [asdict(usage) for usage in usage_records],
            "stats": {
                "total_users": len(users),
                "total_projects": len(projects),
                "total_documents": len(documents),
                "total_api_keys": len(api_keys),
                "total_usage_records": len(usage_records)
            }
        }
    
    def save_to_files(self, output_dir: str = "."):
        """Save generated data to JSON files"""
        data = self.generate_all()
        
        # Convert datetime objects to ISO strings for JSON serialization
        def serialize_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj
        
        for entity_type, records in data.items():
            if entity_type != "stats":
                filename = f"{output_dir}/{entity_type}.json"
                with open(filename, 'w') as f:
                    json.dump(records, f, indent=2, default=serialize_datetime)
        
        # Save summary stats
        with open(f"{output_dir}/stats.json", 'w') as f:
            json.dump(data["stats"], f, indent=2)
        
        print(f"Generated mock data saved to {output_dir}/")
        print(f"Stats: {data['stats']}")


if __name__ == "__main__":
    generator = MockDataGenerator()
    generator.save_to_files("/home/isaac/Workspaces/cogent/mock-data")