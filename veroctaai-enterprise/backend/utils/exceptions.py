"""
Custom Exceptions
"""

class APIException(Exception):
    """Base API exception class"""
    
    def __init__(self, message: str, status_code: int = 400, code: str = None):
        self.message = message
        self.status_code = status_code
        self.code = code or self.__class__.__name__.upper()
        super().__init__(self.message)

class ValidationError(APIException):
    """Validation error exception"""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400, "VALIDATION_ERROR")

class AuthenticationError(APIException):
    """Authentication error exception"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401, "AUTHENTICATION_ERROR")

class AuthorizationError(APIException):
    """Authorization error exception"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, 403, "AUTHORIZATION_ERROR")

class NotFoundError(APIException):
    """Not found error exception"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404, "NOT_FOUND")

class ConflictError(APIException):
    """Conflict error exception"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, 409, "CONFLICT")

class RateLimitError(APIException):
    """Rate limit error exception"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, 429, "RATE_LIMIT")

class InternalError(APIException):
    """Internal server error exception"""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, 500, "INTERNAL_ERROR")

class ServiceUnavailableError(APIException):
    """Service unavailable error exception"""
    
    def __init__(self, message: str = "Service unavailable"):
        super().__init__(message, 503, "SERVICE_UNAVAILABLE")
