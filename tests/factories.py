"""
Factory classes for generating test data
"""

import factory
from factory import fuzzy
from datetime import datetime, timedelta
from uuid import uuid4

# Add shared module to path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.database import User, Project, Document, ApiKey, Usage, VisibilityEnum, OperationTypeEnum


class UserFactory(factory.Factory):
    """Factory for creating User instances"""
    
    class Meta:
        model = User
    
    id = factory.LazyFunction(uuid4)
    clerk_id = factory.Sequence(lambda n: f"user_clerk_{n}_{uuid4().hex[:8]}")
    email = factory.Faker('email')
    name = factory.Faker('name')
    created_at = factory.LazyFunction(lambda: datetime.now() - timedelta(days=30))
    updated_at = factory.LazyFunction(datetime.now)
    settings_json = factory.LazyFunction(lambda: {"theme": "light", "notifications": True})
    clerk_org_id = factory.Maybe(
        'has_org',
        yes_declaration=factory.Sequence(lambda n: f"org_{uuid4().hex[:8]}"),
        no_declaration=None
    )
    last_seen = factory.LazyFunction(lambda: datetime.now() - timedelta(hours=2))
    
    class Params:
        has_org = fuzzy.FuzzyChoice([True, False])


class ProjectFactory(factory.Factory):
    """Factory for creating Project instances"""
    
    class Meta:
        model = Project
    
    id = factory.LazyFunction(uuid4)
    name = factory.Faker('company')
    user_id = factory.LazyAttribute(lambda obj: uuid4())
    github_repo_url = factory.Faker('url')
    created_at = factory.LazyFunction(lambda: datetime.now() - timedelta(days=15))
    updated_at = factory.LazyFunction(datetime.now)
    description = factory.Faker('text', max_nb_chars=200)
    visibility = fuzzy.FuzzyChoice([VisibilityEnum.PRIVATE, VisibilityEnum.PUBLIC])
    settings_json = factory.LazyFunction(lambda: {"auto_generate": True, "doc_template": "default"})
    branch_name = fuzzy.FuzzyChoice(["main", "master", "develop"])
    include_patterns = factory.LazyFunction(lambda: ["**/*", "src/**/*"])
    exclude_patterns = factory.LazyFunction(lambda: ["node_modules/**", ".git/**", "dist/**"])


class DocumentFactory(factory.Factory):
    """Factory for creating Document instances"""
    
    class Meta:
        model = Document
    
    id = factory.LazyFunction(uuid4)
    project_id = factory.LazyAttribute(lambda obj: uuid4())
    file_path = factory.Faker('file_path', depth=3, category='text')
    content = factory.Faker('text', max_nb_chars=1000)
    summary = factory.Faker('sentence')
    commit_hash = factory.LazyFunction(lambda: uuid4().hex[:40])
    created_at = factory.LazyFunction(lambda: datetime.now() - timedelta(days=5))
    updated_at = factory.LazyFunction(datetime.now)
    version = fuzzy.FuzzyInteger(1, 5)
    language = fuzzy.FuzzyChoice(['python', 'javascript', 'typescript', 'java', 'go'])
    imports = factory.LazyFunction(lambda: ['os', 'sys', 'datetime'])
    exports = factory.LazyFunction(lambda: ['main', 'helper_function'])
    references = factory.LazyFunction(lambda: ['src/utils.py', 'src/config.py'])


class ApiKeyFactory(factory.Factory):
    """Factory for creating ApiKey instances"""
    
    class Meta:
        model = ApiKey
    
    id = factory.LazyFunction(uuid4)
    project_id = factory.LazyAttribute(lambda obj: uuid4())
    key_hash = factory.LazyFunction(lambda: f"sk_{uuid4().hex}")
    name = fuzzy.FuzzyChoice(["Production", "Development", "Testing", "MCP Server"])
    created_at = factory.LazyFunction(lambda: datetime.now() - timedelta(days=10))
    last_used = factory.Maybe(
        'is_used',
        yes_declaration=factory.LazyFunction(lambda: datetime.now() - timedelta(hours=5)),
        no_declaration=None
    )
    
    class Params:
        is_used = fuzzy.FuzzyChoice([True, False])


class UsageFactory(factory.Factory):
    """Factory for creating Usage instances"""
    
    class Meta:
        model = Usage
    
    id = factory.LazyFunction(uuid4)
    project_id = factory.LazyAttribute(lambda obj: uuid4())
    timestamp = factory.LazyFunction(lambda: datetime.now() - timedelta(hours=fuzzy.FuzzyInteger(1, 24).fuzz()))
    operation_type = fuzzy.FuzzyChoice([OperationTypeEnum.SEARCH, OperationTypeEnum.GENERATE, OperationTypeEnum.MCP_CALL])
    tokens_used = fuzzy.FuzzyInteger(100, 5000)
    cost = factory.LazyAttribute(lambda obj: obj.tokens_used * 0.0002)
    llm_model = fuzzy.FuzzyChoice([
        "openai/gpt-4-turbo", "openai/gpt-3.5-turbo", 
        "anthropic/claude-3-sonnet", "meta-llama/llama-2-70b"
    ])
    endpoint_called = fuzzy.FuzzyChoice([
        "/api/v1/search", "/api/v1/documents", "/mcp/context"
    ])
    response_time = fuzzy.FuzzyInteger(50, 2000)