"""
SQLAlchemy model tests for COGENT
Tests all database models, relationships, constraints, and validation
"""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4

from conftest import assert_datetime_close
from shared.database import (
    User, Project, Document, ApiKey, Usage, SearchIndex,
    VisibilityEnum, OperationTypeEnum
)
from factories import UserFactory, ProjectFactory, DocumentFactory, ApiKeyFactory, UsageFactory


class TestUserModel:
    """Test User model functionality"""
    
    def test_user_creation(self, test_db: Session):
        """Test basic user creation"""
        user = User(
            id=uuid4(),
            clerk_id="user_clerk_123",
            email="test@example.com",
            name="Test User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(user)
        test_db.commit()
        
        assert user.id is not None
        assert user.clerk_id == "user_clerk_123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert_datetime_close(user.created_at, datetime.now())
    
    def test_user_clerk_id_unique_constraint(self, test_db: Session):
        """Test Clerk ID uniqueness constraint"""
        user1 = User(
            id=uuid4(),
            clerk_id="duplicate_clerk_id",
            email="user1@example.com",
            name="User 1",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(user1)
        test_db.commit()
        
        # Try to create another user with same clerk_id
        user2 = User(
            id=uuid4(),
            clerk_id="duplicate_clerk_id",
            email="user2@example.com",
            name="User 2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_email_unique_constraint(self, test_db: Session):
        """Test email uniqueness constraint"""
        user1 = User(
            id=uuid4(),
            clerk_id="clerk_1",
            email="duplicate@example.com",
            name="User 1",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(user1)
        test_db.commit()
        
        # Try to create another user with same email
        user2 = User(
            id=uuid4(),
            clerk_id="clerk_2",
            email="duplicate@example.com",
            name="User 2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_settings_json_field(self, test_db: Session):
        """Test JSON settings field"""
        settings = {"theme": "dark", "notifications": True, "language": "en"}
        user = User(
            id=uuid4(),
            clerk_id="user_with_settings",
            email="settings@example.com",
            name="Settings User",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            settings_json=settings
        )
        test_db.add(user)
        test_db.commit()
        
        retrieved_user = test_db.query(User).filter(User.clerk_id == "user_with_settings").first()
        assert retrieved_user.settings_json == settings
    
    def test_user_projects_relationship(self, test_db: Session, sample_user: User):
        """Test User -> Projects relationship"""
        project1 = Project(
            id=uuid4(),
            name="Project 1",
            user_id=sample_user.id,
            github_repo_url="https://github.com/user/repo1",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        project2 = Project(
            id=uuid4(),
            name="Project 2",
            user_id=sample_user.id,
            github_repo_url="https://github.com/user/repo2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(project1)
        test_db.add(project2)
        test_db.commit()
        
        # Test relationship
        assert len(sample_user.projects) == 2
        project_names = [p.name for p in sample_user.projects]
        assert "Project 1" in project_names
        assert "Project 2" in project_names


class TestProjectModel:
    """Test Project model functionality"""
    
    def test_project_creation(self, test_db: Session, sample_user: User):
        """Test basic project creation"""
        project = Project(
            id=uuid4(),
            name="Test Project",
            user_id=sample_user.id,
            github_repo_url="https://github.com/test/repo",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            description="Test project description"
        )
        test_db.add(project)
        test_db.commit()
        
        assert project.id is not None
        assert project.name == "Test Project"
        assert project.user_id == sample_user.id
        assert project.github_repo_url == "https://github.com/test/repo"
        assert project.visibility == VisibilityEnum.PRIVATE  # default
        assert project.branch_name == "main"  # default
    
    def test_project_unique_user_repo_constraint(self, test_db: Session, sample_user: User):
        """Test unique constraint on user_id + github_repo_url"""
        repo_url = "https://github.com/user/same-repo"
        
        project1 = Project(
            id=uuid4(),
            name="Project 1",
            user_id=sample_user.id,
            github_repo_url=repo_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(project1)
        test_db.commit()
        
        # Try to create another project with same user and repo
        project2 = Project(
            id=uuid4(),
            name="Project 2",
            user_id=sample_user.id,
            github_repo_url=repo_url,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(project2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_project_include_exclude_patterns(self, test_db: Session, sample_user: User):
        """Test include/exclude pattern arrays"""
        include_patterns = ["src/**/*", "tests/**/*", "*.py"]
        exclude_patterns = ["node_modules/**", ".git/**", "*.pyc", "__pycache__/**"]
        
        project = Project(
            id=uuid4(),
            name="Pattern Project",
            user_id=sample_user.id,
            github_repo_url="https://github.com/test/patterns",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns
        )
        test_db.add(project)
        test_db.commit()
        
        retrieved_project = test_db.query(Project).filter(Project.name == "Pattern Project").first()
        assert retrieved_project.include_patterns == include_patterns
        assert retrieved_project.exclude_patterns == exclude_patterns
    
    def test_project_user_relationship(self, test_db: Session, sample_project: Project, sample_user: User):
        """Test Project -> User relationship"""
        assert sample_project.user.id == sample_user.id
        assert sample_project.user.email == sample_user.email


class TestDocumentModel:
    """Test Document model functionality"""
    
    def test_document_creation(self, test_db: Session, sample_project: Project):
        """Test basic document creation"""
        document = Document(
            id=uuid4(),
            project_id=sample_project.id,
            file_path="src/main.py",
            content="def main():\n    pass",
            summary="Main entry point",
            commit_hash="abc123def456",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            language="python"
        )
        test_db.add(document)
        test_db.commit()
        
        assert document.id is not None
        assert document.project_id == sample_project.id
        assert document.file_path == "src/main.py"
        assert document.language == "python"
        assert document.version == 1  # default
    
    def test_document_unique_project_file_commit_constraint(self, test_db: Session, sample_project: Project):
        """Test unique constraint on project_id + file_path + commit_hash"""
        file_path = "src/auth.py"
        commit_hash = "same_commit_123"
        
        doc1 = Document(
            id=uuid4(),
            project_id=sample_project.id,
            file_path=file_path,
            content="# Auth module v1",
            summary="Authentication module",
            commit_hash=commit_hash,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(doc1)
        test_db.commit()
        
        # Try to create another document with same project, file, and commit
        doc2 = Document(
            id=uuid4(),
            project_id=sample_project.id,
            file_path=file_path,
            content="# Auth module v2",
            summary="Updated authentication module",
            commit_hash=commit_hash,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        test_db.add(doc2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_document_arrays_fields(self, test_db: Session, sample_project: Project):
        """Test imports, exports, references arrays"""
        imports = ["os", "sys", "hashlib", "jwt"]
        exports = ["login", "logout", "validate_token"]
        references = ["src/utils.py", "src/config.py", "tests/test_auth.py"]
        
        document = Document(
            id=uuid4(),
            project_id=sample_project.id,
            file_path="src/auth.py",
            content="# Auth module with imports",
            summary="Authentication with dependencies",
            commit_hash="deps123",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            imports=imports,
            exports=exports,
            references=references
        )
        test_db.add(document)
        test_db.commit()
        
        retrieved_doc = test_db.query(Document).filter(Document.file_path == "src/auth.py").first()
        assert retrieved_doc.imports == imports
        assert retrieved_doc.exports == exports
        assert retrieved_doc.references == references
    
    def test_document_project_relationship(self, test_db: Session, sample_document: Document, sample_project: Project):
        """Test Document -> Project relationship"""
        assert sample_document.project.id == sample_project.id
        assert sample_document.project.name == sample_project.name


class TestApiKeyModel:
    """Test ApiKey model functionality"""
    
    def test_api_key_creation(self, test_db: Session, sample_project: Project):
        """Test basic API key creation"""
        api_key = ApiKey(
            id=uuid4(),
            project_id=sample_project.id,
            key_hash="hashed_key_123",
            name="Test API Key",
            created_at=datetime.now()
        )
        test_db.add(api_key)
        test_db.commit()
        
        assert api_key.id is not None
        assert api_key.project_id == sample_project.id
        assert api_key.key_hash == "hashed_key_123"
        assert api_key.name == "Test API Key"
        assert api_key.last_used is None  # not used yet
    
    def test_api_key_unique_hash_constraint(self, test_db: Session, sample_project: Project):
        """Test unique constraint on key_hash"""
        hash_value = "duplicate_hash_123"
        
        key1 = ApiKey(
            id=uuid4(),
            project_id=sample_project.id,
            key_hash=hash_value,
            name="Key 1",
            created_at=datetime.now()
        )
        test_db.add(key1)
        test_db.commit()
        
        # Try to create another key with same hash
        key2 = ApiKey(
            id=uuid4(),
            project_id=sample_project.id,
            key_hash=hash_value,
            name="Key 2",
            created_at=datetime.now()
        )
        test_db.add(key2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_api_key_unique_project_name_constraint(self, test_db: Session, sample_project: Project):
        """Test unique constraint on project_id + name"""
        key_name = "Production Key"
        
        key1 = ApiKey(
            id=uuid4(),
            project_id=sample_project.id,
            key_hash="hash_1",
            name=key_name,
            created_at=datetime.now()
        )
        test_db.add(key1)
        test_db.commit()
        
        # Try to create another key with same project and name
        key2 = ApiKey(
            id=uuid4(),
            project_id=sample_project.id,
            key_hash="hash_2",
            name=key_name,
            created_at=datetime.now()
        )
        test_db.add(key2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()


class TestUsageModel:
    """Test Usage model functionality"""
    
    def test_usage_creation(self, test_db: Session, sample_project: Project):
        """Test basic usage creation"""
        usage = Usage(
            id=uuid4(),
            project_id=sample_project.id,
            timestamp=datetime.now(),
            operation_type=OperationTypeEnum.SEARCH,
            tokens_used=1500,
            cost=0.15,
            llm_model="openai/gpt-4-turbo",
            endpoint_called="/api/v1/search",
            response_time=250
        )
        test_db.add(usage)
        test_db.commit()
        
        assert usage.id is not None
        assert usage.project_id == sample_project.id
        assert usage.operation_type == OperationTypeEnum.SEARCH
        assert usage.tokens_used == 1500
        assert usage.cost == 0.15
    
    def test_usage_positive_constraints(self, test_db: Session, sample_project: Project):
        """Test positive value constraints on tokens_used and cost"""
        # Test negative tokens_used
        with pytest.raises(IntegrityError):
            usage1 = Usage(
                id=uuid4(),
                project_id=sample_project.id,
                timestamp=datetime.now(),
                operation_type=OperationTypeEnum.GENERATE,
                tokens_used=-100,  # Invalid negative value
                cost=0.10,
                llm_model="openai/gpt-4",
                endpoint_called="/api/v1/generate"
            )
            test_db.add(usage1)
            test_db.commit()
        
        test_db.rollback()
        
        # Test negative cost
        with pytest.raises(IntegrityError):
            usage2 = Usage(
                id=uuid4(),
                project_id=sample_project.id,
                timestamp=datetime.now(),
                operation_type=OperationTypeEnum.MCP_CALL,
                tokens_used=500,
                cost=-0.05,  # Invalid negative value
                llm_model="anthropic/claude-3-sonnet",
                endpoint_called="/mcp/context"
            )
            test_db.add(usage2)
            test_db.commit()
    
    def test_usage_operation_type_enum(self, test_db: Session, sample_project: Project):
        """Test operation type enum validation"""
        for op_type in [OperationTypeEnum.SEARCH, OperationTypeEnum.GENERATE, OperationTypeEnum.MCP_CALL]:
            usage = Usage(
                id=uuid4(),
                project_id=sample_project.id,
                timestamp=datetime.now(),
                operation_type=op_type,
                tokens_used=1000,
                cost=0.10,
                llm_model="test/model",
                endpoint_called="/test/endpoint"
            )
            test_db.add(usage)
            test_db.commit()
            
            assert usage.operation_type == op_type
            test_db.delete(usage)
            test_db.commit()


class TestSearchIndexModel:
    """Test SearchIndex model functionality"""
    
    def test_search_index_creation(self, test_db: Session, sample_document: Document):
        """Test basic search index creation"""
        search_index = SearchIndex(
            id=uuid4(),
            document_id=sample_document.id,
            full_text="test search content",
            content_vector=None,  # Vector will be populated by embedding service
            relevance_scores={"tf_idf": 0.85, "bm25": 0.90},
            metadata_json={"language": "python", "file_size": 1024}
        )
        test_db.add(search_index)
        test_db.commit()
        
        assert search_index.id is not None
        assert search_index.document_id == sample_document.id
        assert search_index.relevance_scores["tf_idf"] == 0.85
    
    def test_search_index_document_relationship(self, test_db: Session, sample_document: Document):
        """Test SearchIndex -> Document relationship"""
        search_index = SearchIndex(
            id=uuid4(),
            document_id=sample_document.id,
            full_text="relationship test",
            content_vector=None
        )
        test_db.add(search_index)
        test_db.commit()
        
        # Test relationship
        assert search_index.document.id == sample_document.id
        assert search_index.document.file_path == sample_document.file_path
        
        # Test back reference
        assert sample_document.search_index.id == search_index.id


class TestModelFactories:
    """Test factory classes for generating test data"""
    
    def test_user_factory(self, test_db: Session):
        """Test UserFactory creates valid users"""
        user = UserFactory()
        assert user.clerk_id is not None
        assert "@" in user.email
        assert user.name is not None
        assert user.created_at is not None
    
    def test_project_factory(self, test_db: Session):
        """Test ProjectFactory creates valid projects"""
        project = ProjectFactory()
        assert project.name is not None
        assert project.github_repo_url is not None
        assert project.visibility in [VisibilityEnum.PRIVATE, VisibilityEnum.PUBLIC]
        assert isinstance(project.include_patterns, list)
        assert isinstance(project.exclude_patterns, list)
    
    def test_document_factory(self, test_db: Session):
        """Test DocumentFactory creates valid documents"""
        document = DocumentFactory()
        assert document.file_path is not None
        assert document.content is not None
        assert document.commit_hash is not None
        assert document.language in ['python', 'javascript', 'typescript', 'java', 'go']
        assert isinstance(document.imports, list)
        assert isinstance(document.exports, list)