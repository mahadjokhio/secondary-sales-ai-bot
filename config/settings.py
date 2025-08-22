"""
Centralized configuration management for the Secondary Sales AI Bot.

This module handles all application settings, environment variables,
and configuration validation with proper error handling.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class Settings:
    """
    Centralized settings management with validation and fallbacks.
    
    Handles environment-based configuration with proper validation
    and fallback values for optional settings.
    """
    
    def __init__(self):
        """Initialize settings and validate required configurations."""
        self._validate_environment()
        self._setup_logging()
        
    def _validate_environment(self) -> None:
        """Validate required environment variables and settings."""
        # Make Google API key optional for now - app can work without AI chat
        optional_vars = ["GOOGLE_API_KEY"]
        missing_vars = [var for var in optional_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(
                f"Optional environment variables not set: {', '.join(missing_vars)}. "
                f"AI chat functionality will be limited."
            )
    
    def _setup_logging(self) -> None:
        """Configure logging based on environment settings."""
        log_level = self.LOG_LEVEL
        
        # Remove default logger
        logger.remove()
        
        # Add console logger
        logger.add(
            sys.stderr,
            level=log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "<level>{message}</level>"
        )
        
        # Add file logger for production
        if not self.DEBUG_MODE:
            logger.add(
                "logs/app_{time:YYYY-MM-DD}.log",
                rotation="1 day",
                retention="7 days",
                level="INFO",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
            )
    
    # API Configuration
    @property
    def GOOGLE_API_KEY(self) -> str:
        """Google Gemini API key."""
        return os.getenv("GOOGLE_API_KEY", "")
    
    @property
    def GEMINI_MODEL(self) -> str:
        """Google Gemini model name."""
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # Application Settings
    @property
    def APP_TITLE(self) -> str:
        """Application title."""
        return os.getenv("APP_TITLE", "Secondary Sales AI Bot - Sukkur Beverages")
    
    @property
    def DEBUG_MODE(self) -> bool:
        """Debug mode flag."""
        return os.getenv("DEBUG_MODE", "False").lower() == "true"
    
    @property
    def TEST_MODE(self) -> bool:
        """Test mode flag."""
        return os.getenv("TEST_MODE", "False").lower() == "true"
    
    @property
    def LOG_LEVEL(self) -> str:
        """Logging level."""
        return os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Voice Settings
    @property
    def VOICE_LANGUAGE(self) -> str:
        """Voice recognition language."""
        return os.getenv("VOICE_LANGUAGE", "en-US")
    
    @property
    def TTS_RATE(self) -> int:
        """Text-to-speech rate."""
        try:
            return int(os.getenv("TTS_RATE", "150"))
        except ValueError:
            logger.warning("Invalid TTS_RATE value, using default: 150")
            return 150
    
    @property
    def TTS_VOICE(self) -> str:
        """Text-to-speech voice gender."""
        return os.getenv("TTS_VOICE", "female")
    
    # Database Settings
    @property
    def DATA_DIRECTORY(self) -> Path:
        """Data directory path."""
        data_dir = Path(os.getenv("DATA_DIRECTORY", "./data"))
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    @property
    def BACKUP_ENABLED(self) -> bool:
        """Backup enabled flag."""
        return os.getenv("BACKUP_ENABLED", "True").lower() == "true"
    
    @property
    def BACKUP_INTERVAL(self) -> int:
        """Backup interval in seconds."""
        try:
            return int(os.getenv("BACKUP_INTERVAL", "3600"))
        except ValueError:
            logger.warning("Invalid BACKUP_INTERVAL value, using default: 3600")
            return 3600
    
    # Performance Settings
    @property
    def MAX_CHAT_HISTORY(self) -> int:
        """Maximum chat history entries."""
        try:
            return int(os.getenv("MAX_CHAT_HISTORY", "50"))
        except ValueError:
            logger.warning("Invalid MAX_CHAT_HISTORY value, using default: 50")
            return 50
    
    @property
    def API_TIMEOUT(self) -> int:
        """API request timeout in seconds."""
        try:
            return int(os.getenv("API_TIMEOUT", "30"))
        except ValueError:
            logger.warning("Invalid API_TIMEOUT value, using default: 30")
            return 30
    
    @property
    def MAX_FILE_SIZE(self) -> str:
        """Maximum file size for uploads."""
        return os.getenv("MAX_FILE_SIZE", "10MB")
    
    # Security Settings
    @property
    def ENABLE_RATE_LIMITING(self) -> bool:
        """Rate limiting enabled flag."""
        return os.getenv("ENABLE_RATE_LIMITING", "True").lower() == "true"
    
    @property
    def MAX_REQUESTS_PER_MINUTE(self) -> int:
        """Maximum requests per minute."""
        try:
            return int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))
        except ValueError:
            logger.warning("Invalid MAX_REQUESTS_PER_MINUTE value, using default: 60")
            return 60
    
    @property
    def ENABLE_INPUT_SANITIZATION(self) -> bool:
        """Input sanitization enabled flag."""
        return os.getenv("ENABLE_INPUT_SANITIZATION", "True").lower() == "true"
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            "app_title": self.APP_TITLE,
            "debug_mode": self.DEBUG_MODE,
            "test_mode": self.TEST_MODE,
            "log_level": self.LOG_LEVEL,
            "voice_language": self.VOICE_LANGUAGE,
            "tts_rate": self.TTS_RATE,
            "tts_voice": self.TTS_VOICE,
            "data_directory": str(self.DATA_DIRECTORY),
            "backup_enabled": self.BACKUP_ENABLED,
            "backup_interval": self.BACKUP_INTERVAL,
            "max_chat_history": self.MAX_CHAT_HISTORY,
            "api_timeout": self.API_TIMEOUT,
            "max_file_size": self.MAX_FILE_SIZE,
            "enable_rate_limiting": self.ENABLE_RATE_LIMITING,
            "max_requests_per_minute": self.MAX_REQUESTS_PER_MINUTE,
            "enable_input_sanitization": self.ENABLE_INPUT_SANITIZATION,
        }
    
    def validate_api_key(self) -> bool:
        """Validate API key format and accessibility."""
        api_key = self.GOOGLE_API_KEY
        
        if not api_key or api_key == "your_google_api_key_here":
            logger.warning("Google API key not configured. AI chat will be unavailable.")
            return False
        
        if len(api_key) < 10:
            logger.error("Invalid Google API key format")
            return False
        
        # Additional API key validation can be added here
        logger.info("Google API key validated successfully")
        return True
    
    def validate_file_paths(self) -> bool:
        """Validate file path accessibility."""
        try:
            # Check data directory
            data_dir = self.DATA_DIRECTORY
            if not data_dir.exists():
                data_dir.mkdir(parents=True)
            
            # Check write permissions
            test_file = data_dir / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            
            return True
        except Exception as e:
            logger.error(f"File path validation failed: {e}")
            return False


# Global settings instance
try:
    settings = Settings()
    logger.info("Configuration loaded successfully")
except ConfigError as e:
    logger.error(f"Configuration error: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error loading configuration: {e}")
    sys.exit(1)


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings
