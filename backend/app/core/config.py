"""
Configuration management for COGENT backend.
Uses environment variables with sensible defaults.
"""

import os
from functools import lru_cache
from typing import List


class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        # Environment
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        
        # Database
        self.database_url: str = os.getenv(
            "DATABASE_URL", 
            "sqlite:///./cogent.db"
        )
        
        # JWT Settings
        self.jwt_secret_key: str = os.getenv(
            "JWT_SECRET_KEY", 
            "dev-secret-key-change-in-production"
        )
        self.jwt_algorithm: str = "HS256"
        self.access_token_expire_minutes: int = 15
        self.refresh_token_expire_days: int = 7
        
        # CORS Settings
        self.allowed_origins: List[str] = self._parse_origins()
        self.allowed_hosts: List[str] = self._parse_hosts()
        
        # PostgreSQL connection pool settings
        self.db_pool_size: int = int(os.getenv("DB_POOL_SIZE", "5"))
        self.db_max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        self.db_pool_timeout: int = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        
        # Pagination defaults
        self.default_project_limit: int = 20
        self.max_project_limit: int = 100
        self.default_document_limit: int = 50
        self.max_document_limit: int = 200
        self.default_search_limit: int = 10
        self.max_search_limit: int = 50
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
    def _parse_origins(self) -> List[str]:
        """Parse CORS allowed origins from environment"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "")
        if origins_str:
            return [origin.strip() for origin in origins_str.split(",")]
        
        # Default CORS settings based on environment
        if self.environment == "development":
            return [
                "http://localhost:3000",  # Frontend dev server
                "http://127.0.0.1:3000",
                "http://localhost:5173",  # Vite dev server alternative port
            ]
        else:
            return ["https://usecogent.io", "https://www.usecogent.io"]
    
    def _parse_hosts(self) -> List[str]:
        """Parse trusted hosts from environment"""
        hosts_str = os.getenv("ALLOWED_HOSTS", "")
        if hosts_str:
            return [host.strip() for host in hosts_str.split(",")]
        
        # Default trusted hosts
        if self.environment == "development":
            return ["localhost", "127.0.0.1", "testserver"]
        else:
            return ["api.usecogent.io", "usecogent.io"]
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment == "production"
    
    @property
    def cookie_secure(self) -> bool:
        """Whether to use secure cookies (HTTPS only)"""
        return self.is_production
    
    @property
    def cookie_domain(self) -> str:
        """Cookie domain setting"""
        if self.is_production:
            return ".usecogent.io"
        return None


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()