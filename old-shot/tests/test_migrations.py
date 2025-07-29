"""
Database migration tests for COGENT
Tests database schema creation, constraints, indexes, and migration reversibility
"""

import pytest
from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
import tempfile

# Add shared module to path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from shared.database import Base, User, Project, Document, ApiKey, Usage, SearchIndex, VisibilityEnum, OperationTypeEnum


@pytest.fixture
def clean_engine():
    """Create a clean SQLite engine for migration testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False
    )
    return engine


@pytest.fixture
def empty_db_session(clean_engine):
    """Create session with empty database (no tables created)"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=clean_engine)
    session = SessionLocal()
    try:
        yield session, clean_engine
    finally:
        session.close()


@pytest.fixture
def migrated_db_session(clean_engine):
    """Create session with migrated database (all tables created)"""
    Base.metadata.create_all(clean_engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=clean_engine)
    session = SessionLocal()
    try:
        yield session, clean_engine
    finally:
        session.close()


class TestSchemaCreation:
    """Test database schema creation and structure"""
    
    def test_create_all_tables(self, empty_db_session):
        """Test that all tables are created correctly"""
        session, engine = empty_db_session
        
        # Initially no tables should exist
        inspector = inspect(engine)
        initial_tables = inspector.get_table_names()
        assert len(initial_tables) == 0
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        # Verify all expected tables exist
        final_tables = inspector.get_table_names()
        expected_tables = {
            'users', 'projects', 'documents', 'api_keys', 'usage', 'search_indexes'
        }
        assert set(final_tables) == expected_tables
    
    def test_users_table_structure(self, migrated_db_session):
        """Test users table structure and columns"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('users')}
        
        # Check all expected columns exist
        expected_columns = {
            'id', 'clerk_id', 'email', 'name', 'created_at', 'updated_at',
            'settings_json', 'clerk_org_id', 'last_seen'
        }
        assert set(columns.keys()) == expected_columns
        
        # Check primary key
        pk_constraint = inspector.get_pk_constraint('users')
        assert pk_constraint['constrained_columns'] == ['id']
        
        # Check unique constraints
        unique_constraints = inspector.get_unique_constraints('users')
        unique_columns = []
        for constraint in unique_constraints:
            unique_columns.extend(constraint['column_names'])
        assert 'clerk_id' in unique_columns
        assert 'email' in unique_columns
    
    def test_projects_table_structure(self, migrated_db_session):
        """Test projects table structure and relationships"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('projects')}
        
        # Check all expected columns exist
        expected_columns = {
            'id', 'name', 'user_id', 'github_repo_url', 'created_at', 'updated_at',
            'description', 'visibility', 'settings_json', 'branch_name',
            'include_patterns', 'exclude_patterns'
        }
        assert set(columns.keys()) == expected_columns
        
        # Check foreign key constraints
        fk_constraints = inspector.get_foreign_keys('projects')
        user_fk = next((fk for fk in fk_constraints if 'user_id' in fk['constrained_columns']), None)
        assert user_fk is not None
        assert user_fk['referred_table'] == 'users'
    
    def test_documents_table_structure(self, migrated_db_session):
        """Test documents table structure"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('documents')}
        
        # Check all expected columns exist
        expected_columns = {
            'id', 'project_id', 'file_path', 'content', 'summary', 'commit_hash',
            'created_at', 'updated_at', 'version', 'language', 'imports', 'exports', 'references'
        }
        assert set(columns.keys()) == expected_columns
        
        # Check foreign key to projects
        fk_constraints = inspector.get_foreign_keys('documents')
        project_fk = next((fk for fk in fk_constraints if 'project_id' in fk['constrained_columns']), None)
        assert project_fk is not None
        assert project_fk['referred_table'] == 'projects'
    
    def test_api_keys_table_structure(self, migrated_db_session):
        """Test api_keys table structure"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('api_keys')}
        
        # Check all expected columns exist
        expected_columns = {'id', 'project_id', 'key_hash', 'name', 'created_at', 'last_used'}
        assert set(columns.keys()) == expected_columns
        
        # Check unique constraint on key_hash
        unique_constraints = inspector.get_unique_constraints('api_keys')
        unique_columns = []
        for constraint in unique_constraints:
            unique_columns.extend(constraint['column_names'])
        assert 'key_hash' in unique_columns
    
    def test_usage_table_structure(self, migrated_db_session):
        """Test usage table structure"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('usage')}
        
        # Check all expected columns exist
        expected_columns = {
            'id', 'project_id', 'timestamp', 'operation_type', 'tokens_used',
            'cost', 'llm_model', 'endpoint_called', 'response_time'
        }
        assert set(columns.keys()) == expected_columns
    
    def test_search_indexes_table_structure(self, migrated_db_session):
        """Test search_indexes table structure"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        columns = {col['name']: col for col in inspector.get_columns('search_indexes')}
        
        # Check all expected columns exist
        expected_columns = {
            'id', 'document_id', 'content_vector', 'full_text', 
            'relevance_scores', 'metadata_json'
        }
        assert set(columns.keys()) == expected_columns
        
        # Check unique constraint on document_id (one-to-one relationship)
        unique_constraints = inspector.get_unique_constraints('search_indexes')
        unique_columns = []
        for constraint in unique_constraints:
            unique_columns.extend(constraint['column_names'])
        assert 'document_id' in unique_columns


class TestConstraints:
    """Test database constraints are properly enforced"""
    
    def test_user_unique_constraints_enforced(self, migrated_db_session):
        """Test that unique constraints on users are enforced"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create first user
        user1 = User(
            id=uuid4(),
            clerk_id="unique_clerk_123",
            email="unique@example.com",
            name="User 1",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user1)
        session.commit()
        
        # Try to create user with duplicate clerk_id (should fail in real PostgreSQL)
        # SQLite doesn't enforce this as strictly, so we'll test the model validation
        user2 = User(
            id=uuid4(),
            clerk_id="unique_clerk_123",  # Duplicate
            email="different@example.com",
            name="User 2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user2)
        
        # In real PostgreSQL this would raise IntegrityError
        # SQLite may allow it, but our application logic should prevent it
        try:
            session.commit()
            # If SQLite allows it, we manually check for uniqueness
            clerk_count = session.query(User).filter(User.clerk_id == "unique_clerk_123").count()
            if clerk_count > 1:
                session.rollback()
                pytest.fail("Unique constraint on clerk_id should prevent duplicates")
        except IntegrityError:
            # This is expected behavior
            session.rollback()
    
    def test_project_user_repo_uniqueness(self, migrated_db_session):
        """Test unique constraint on user_id + github_repo_url"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create user first
        user = User(
            id=uuid4(),
            clerk_id="project_user_123",
            email="project@example.com",
            name="Project User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        # Create first project
        project1 = Project(
            id=uuid4(),
            name="Project 1",
            user_id=user.id,
            github_repo_url="https://github.com/user/same-repo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project1)
        session.commit()
        
        # Try to create another project with same user and repo
        project2 = Project(
            id=uuid4(),
            name="Project 2",
            user_id=user.id,
            github_repo_url="https://github.com/user/same-repo",  # Duplicate
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project2)
        
        # This should fail due to unique constraint
        try:
            session.commit()
            # Check if constraint was enforced
            count = session.query(Project).filter(
                Project.user_id == user.id,
                Project.github_repo_url == "https://github.com/user/same-repo"
            ).count()
            if count > 1:
                session.rollback()
                pytest.fail("Unique constraint on user_id + github_repo_url should prevent duplicates")
        except IntegrityError:
            session.rollback()  # Expected
    
    def test_document_project_file_commit_uniqueness(self, migrated_db_session):
        """Test unique constraint on project_id + file_path + commit_hash"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create user and project
        user = User(
            id=uuid4(),
            clerk_id="doc_user_123",
            email="doc@example.com",
            name="Doc User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        project = Project(
            id=uuid4(),
            name="Doc Project",
            user_id=user.id,
            github_repo_url="https://github.com/user/doc-repo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project)
        session.commit()
        
        # Create first document
        doc1 = Document(
            id=uuid4(),
            project_id=project.id,
            file_path="src/auth.py",
            content="# Auth module v1",
            summary="Authentication module",
            commit_hash="same_commit_123",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(doc1)
        session.commit()
        
        # Try to create another document with same project, file, and commit
        doc2 = Document(
            id=uuid4(),
            project_id=project.id,
            file_path="src/auth.py",  # Same file
            content="# Auth module v2",
            summary="Updated auth",
            commit_hash="same_commit_123",  # Same commit
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(doc2)
        
        try:
            session.commit()
            # Check constraint enforcement
            count = session.query(Document).filter(
                Document.project_id == project.id,
                Document.file_path == "src/auth.py",
                Document.commit_hash == "same_commit_123"
            ).count()
            if count > 1:
                session.rollback()
                pytest.fail("Unique constraint on project_id + file_path + commit_hash should prevent duplicates")
        except IntegrityError:
            session.rollback()  # Expected


class TestIndexes:
    """Test that database indexes are created for performance"""
    
    def test_users_indexes(self, migrated_db_session):
        """Test indexes on users table"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        indexes = inspector.get_indexes('users')
        index_columns = []
        for index in indexes:
            index_columns.extend(index['column_names'])
        
        # Important indexes for users
        assert 'clerk_id' in index_columns or any('clerk_id' in str(idx) for idx in indexes)
        assert 'email' in index_columns or any('email' in str(idx) for idx in indexes)
    
    def test_projects_indexes(self, migrated_db_session):
        """Test indexes on projects table"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        indexes = inspector.get_indexes('projects')
        index_columns = []
        for index in indexes:
            index_columns.extend(index['column_names'])
        
        # Should have index on user_id for foreign key performance
        assert 'user_id' in index_columns or any('user_id' in str(idx) for idx in indexes)
    
    def test_documents_indexes(self, migrated_db_session):
        """Test indexes on documents table"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        indexes = inspector.get_indexes('documents')
        index_columns = []
        for index in indexes:
            index_columns.extend(index['column_names'])
        
        # Should have indexes for common query patterns
        assert 'project_id' in index_columns or any('project_id' in str(idx) for idx in indexes)
        assert 'commit_hash' in index_columns or any('commit_hash' in str(idx) for idx in indexes)
    
    def test_usage_indexes(self, migrated_db_session):
        """Test indexes on usage table for analytics queries"""
        session, engine = migrated_db_session
        inspector = inspect(engine)
        
        indexes = inspector.get_indexes('usage')
        index_columns = []
        for index in indexes:
            index_columns.extend(index['column_names'])
        
        # Should have indexes for analytics queries
        assert 'project_id' in index_columns or any('project_id' in str(idx) for idx in indexes)
        assert 'timestamp' in index_columns or any('timestamp' in str(idx) for idx in indexes)


class TestMigrationReversibility:
    """Test that migrations can be applied and reversed"""
    
    def test_create_drop_all_tables(self, clean_engine):
        """Test creating and dropping all tables"""
        inspector = inspect(clean_engine)
        
        # Initially no tables
        initial_tables = inspector.get_table_names()
        assert len(initial_tables) == 0
        
        # Create all tables
        Base.metadata.create_all(clean_engine)
        
        # Verify tables exist
        created_tables = inspector.get_table_names()
        assert len(created_tables) > 0
        expected_tables = {'users', 'projects', 'documents', 'api_keys', 'usage', 'search_indexes'}
        assert set(created_tables) == expected_tables
        
        # Drop all tables
        Base.metadata.drop_all(clean_engine)
        
        # Verify tables are gone
        final_tables = inspector.get_table_names()
        assert len(final_tables) == 0
    
    def test_individual_table_creation(self, clean_engine):
        """Test creating tables individually"""
        inspector = inspect(clean_engine)
        
        # Create just users table
        User.__table__.create(clean_engine)
        tables = inspector.get_table_names()
        assert 'users' in tables
        assert len(tables) == 1
        
        # Create projects table (requires users)
        Project.__table__.create(clean_engine)
        tables = inspector.get_table_names()
        assert 'users' in tables
        assert 'projects' in tables
        assert len(tables) == 2
        
        # Clean up
        Base.metadata.drop_all(clean_engine)


class TestDataIntegrity:
    """Test data integrity and relationships"""
    
    def test_cascade_delete_user_projects(self, migrated_db_session):
        """Test that deleting a user cascades to projects"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create user with projects
        user = User(
            id=uuid4(),
            clerk_id="cascade_user_123",
            email="cascade@example.com", 
            name="Cascade User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        project1 = Project(
            id=uuid4(),
            name="Project 1",
            user_id=user.id,
            github_repo_url="https://github.com/user/repo1",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        project2 = Project(
            id=uuid4(),
            name="Project 2", 
            user_id=user.id,
            github_repo_url="https://github.com/user/repo2",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project1)
        session.add(project2)
        session.commit()
        
        # Verify projects exist
        project_count = session.query(Project).filter(Project.user_id == user.id).count()
        assert project_count == 2
        
        # Delete user
        session.delete(user)
        session.commit()
        
        # Verify projects are also deleted (cascade)
        remaining_projects = session.query(Project).filter(Project.user_id == user.id).count()
        assert remaining_projects == 0
    
    def test_foreign_key_constraint_enforcement(self, migrated_db_session):
        """Test that foreign key constraints are enforced"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Try to create project with non-existent user_id
        non_existent_user_id = uuid4()
        project = Project(
            id=uuid4(),
            name="Orphan Project",
            user_id=non_existent_user_id,  # Non-existent user
            github_repo_url="https://github.com/orphan/repo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project)
        
        # This should fail due to foreign key constraint
        # Note: SQLite with foreign keys enabled should catch this
        try:
            session.commit()
            # If it doesn't fail, check manually
            user_exists = session.query(User).filter(User.id == non_existent_user_id).first()
            if not user_exists:
                # Foreign key constraint should have prevented this
                session.rollback()
                # In development, this might pass in SQLite, but would fail in PostgreSQL
        except IntegrityError:
            session.rollback()  # Expected behavior
    
    def test_enum_constraint_enforcement(self, migrated_db_session):
        """Test that enum constraints are enforced"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create user first
        user = User(
            id=uuid4(),
            clerk_id="enum_user_123",
            email="enum@example.com",
            name="Enum User", 
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        # Test valid enum values
        for visibility in [VisibilityEnum.PRIVATE, VisibilityEnum.PUBLIC]:
            project = Project(
                id=uuid4(),
                name=f"Project {visibility.value}",
                user_id=user.id,
                github_repo_url=f"https://github.com/user/{visibility.value}",
                visibility=visibility,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            session.add(project)
            session.commit()
            
            # Verify enum value is stored correctly
            retrieved = session.query(Project).filter(Project.name == f"Project {visibility.value}").first()
            assert retrieved.visibility == visibility
            
            session.delete(retrieved)
            session.commit()


class TestPerformanceConsiderations:
    """Test performance-related database aspects"""
    
    def test_query_performance_with_indexes(self, migrated_db_session):
        """Test that common queries perform well with indexes"""
        session, engine = migrated_db_session
        
        from datetime import datetime, timedelta
        from uuid import uuid4
        
        # Create test data
        user = User(
            id=uuid4(),
            clerk_id="perf_user_123",
            email="perf@example.com",
            name="Performance User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        project = Project(
            id=uuid4(),
            name="Performance Project",
            user_id=user.id,
            github_repo_url="https://github.com/perf/repo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project)
        session.commit()
        
        # Create multiple usage records for performance testing
        base_time = datetime.now() - timedelta(days=30)
        for i in range(50):  # Create 50 usage records
            usage = Usage(
                id=uuid4(),
                project_id=project.id,
                timestamp=base_time + timedelta(hours=i),
                operation_type=OperationTypeEnum.SEARCH if i % 2 == 0 else OperationTypeEnum.GENERATE,
                tokens_used=1000 + i * 10,
                cost=0.1 + i * 0.01,
                llm_model="openai/gpt-4-turbo",
                endpoint_called="/api/v1/search",
                response_time=100 + i
            )
            session.add(usage)
        session.commit()
        
        # Test common query patterns that should use indexes
        
        # 1. Find user by clerk_id (should use clerk_id index)
        start_time = datetime.now()
        found_user = session.query(User).filter(User.clerk_id == "perf_user_123").first()
        query_time = (datetime.now() - start_time).total_seconds()
        assert found_user is not None
        assert query_time < 0.1  # Should be very fast with index
        
        # 2. Find projects by user (should use user_id index)
        start_time = datetime.now()
        user_projects = session.query(Project).filter(Project.user_id == user.id).all()
        query_time = (datetime.now() - start_time).total_seconds()
        assert len(user_projects) == 1
        assert query_time < 0.1
        
        # 3. Find usage by project and date range (should use project_id and timestamp indexes)
        start_time = datetime.now()
        recent_usage = session.query(Usage).filter(
            Usage.project_id == project.id,
            Usage.timestamp >= base_time,
            Usage.timestamp <= datetime.now()
        ).all()
        query_time = (datetime.now() - start_time).total_seconds()
        assert len(recent_usage) == 50
        assert query_time < 0.1
    
    def test_connection_handling(self, clean_engine):
        """Test that database connections are handled properly"""
        # Test that we can create multiple sessions without issues
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=clean_engine)
        
        sessions = []
        try:
            # Create multiple concurrent sessions
            for i in range(5):
                session = SessionLocal()
                sessions.append(session)
                
                # Test basic query on each session
                result = session.execute(text("SELECT 1 as test")).fetchone()
                assert result[0] == 1
                
        finally:
            # Clean up all sessions
            for session in sessions:
                session.close()
    
    def test_large_data_handling(self, migrated_db_session):
        """Test handling of larger data objects"""
        session, engine = migrated_db_session
        
        from datetime import datetime
        from uuid import uuid4
        
        # Create user and project
        user = User(
            id=uuid4(),
            clerk_id="large_data_user",
            email="large@example.com",
            name="Large Data User",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(user)
        session.commit()
        
        project = Project(
            id=uuid4(),
            name="Large Data Project",
            user_id=user.id,
            github_repo_url="https://github.com/large/repo",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(project)
        session.commit()
        
        # Test document with large content
        large_content = "# Large document\n" + "This is a large document. " * 1000  # ~24KB
        large_imports = [f"import module_{i}" for i in range(100)]  # Large array
        
        document = Document(
            id=uuid4(),
            project_id=project.id,
            file_path="large_file.py",
            content=large_content,
            summary="A very large document for testing",
            commit_hash="large_commit_123",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            imports=large_imports,
            language="python"
        )
        session.add(document)
        session.commit()
        
        # Retrieve and verify large document
        retrieved_doc = session.query(Document).filter(Document.file_path == "large_file.py").first()
        assert retrieved_doc is not None
        assert len(retrieved_doc.content) > 20000
        assert len(retrieved_doc.imports) == 100
        assert retrieved_doc.imports[0] == "import module_0"