"""
Custom exception classes for the Secondary Sales AI Bot.

This module defines all custom exceptions used throughout the application
for better error handling and debugging.
"""

from typing import Optional, Any, Dict


class BotException(Exception):
    """Base exception class for all bot-related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ConfigurationError(BotException):
    """Raised when there's a configuration-related error."""
    pass


class VoiceProcessingError(BotException):
    """Raised when voice processing fails."""
    pass


class OrderProcessingError(BotException):
    """Raised when order processing fails."""
    pass


class DataValidationError(BotException):
    """Raised when data validation fails."""
    pass


class APIError(BotException):
    """Raised when external API calls fail."""
    pass


class DatabaseError(BotException):
    """Raised when database operations fail."""
    pass


class AuthenticationError(BotException):
    """Raised when authentication fails."""
    pass


class RateLimitError(BotException):
    """Raised when rate limits are exceeded."""
    pass


class AudioProcessingError(VoiceProcessingError):
    """Raised when audio processing fails."""
    pass


class SpeechRecognitionError(VoiceProcessingError):
    """Raised when speech recognition fails."""
    pass


class TextToSpeechError(VoiceProcessingError):
    """Raised when text-to-speech fails."""
    pass


class InvalidProductError(OrderProcessingError):
    """Raised when an invalid product is specified."""
    pass


class InsufficientStockError(OrderProcessingError):
    """Raised when there's insufficient stock for an order."""
    pass


class CreditLimitExceededError(OrderProcessingError):
    """Raised when an order exceeds credit limit."""
    pass


class InvalidOutletError(OrderProcessingError):
    """Raised when an invalid outlet is specified."""
    pass


class LLMResponseError(APIError):
    """Raised when LLM response is invalid or unexpected."""
    pass


class NetworkError(APIError):
    """Raised when network connectivity issues occur."""
    pass


class FileCorruptionError(DatabaseError):
    """Raised when data files are corrupted."""
    pass


class BackupError(DatabaseError):
    """Raised when backup operations fail."""
    pass
