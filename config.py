import os
from datetime import timedelta

class Config:
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database Configuration
    DATABASE_NAME = 'users.db'
    
    # AI/Gemini Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    GEMINI_MODEL = 'gemini-2.0-flash-001'
    
    # Interview Configuration
    MAX_QUESTIONS_PER_SESSION = 10
    DEFAULT_INTERVIEW_DIFFICULTY = 'intermediate'
    DEFAULT_SESSION_TYPE = 'technical'
    
    # Resume Analysis Configuration
    MIN_RESUME_TEXT_LENGTH = 100  # Minimum characters for meaningful analysis
    ANALYSIS_TIMEOUT = 300  # 5 minutes timeout for analysis
    
    # Application Features
    ENABLE_RESUME_SCANNER = True
    ENABLE_MOCK_INTERVIEWS = True
    ENABLE_JOB_TRACKER = True
    ENABLE_ROADMAPS = True
    
    # Rate Limiting (requests per minute)
    ROADMAP_GENERATION_LIMIT = 5
    RESUME_ANALYSIS_LIMIT = 10
    INTERVIEW_SESSION_LIMIT = 3

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    # Add production-specific configurations

class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = ':memory:'  # Use in-memory database for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Application constants
class AppConstants:
    # Interview question types
    QUESTION_TYPES = {
        'TECHNICAL': 'technical',
        'BEHAVIORAL': 'behavioral',
        'SITUATIONAL': 'situational'
    }
    
    # Difficulty levels
    DIFFICULTY_LEVELS = {
        'BEGINNER': 'beginner',
        'INTERMEDIATE': 'intermediate', 
        'ADVANCED': 'advanced',
        'EXPERT': 'expert'
    }
    
    # Session types
    SESSION_TYPES = {
        'TECHNICAL': 'technical',
        'BEHAVIORAL': 'behavioral',
        'MIXED': 'mixed'
    }
    
    # Resume categories
    RESUME_CATEGORIES = {
        'GENERAL': 'general',
        'TECHNICAL': 'technical',
        'EXECUTIVE': 'executive',
        'CREATIVE': 'creative',
        'ACADEMIC': 'academic'
    }
    
    # Application statuses
    APPLICATION_STATUSES = {
        'APPLIED': 'applied',
        'UNDER_REVIEW': 'under_review',
        'INTERVIEW_SCHEDULED': 'interview_scheduled',
        'INTERVIEWED': 'interviewed',
        'OFFER_RECEIVED': 'offer_received',
        'ACCEPTED': 'accepted',
        'REJECTED': 'rejected',
        'WITHDRAWN': 'withdrawn'
    }
    
    # Analysis statuses
    ANALYSIS_STATUSES = {
        'PENDING': 'pending',
        'ANALYZING': 'analyzing',
        'COMPLETED': 'completed',
        'FAILED': 'failed'
    }
    
    # Experience levels
    EXPERIENCE_LEVELS = {
        'ENTRY': 'entry',
        'MID': 'mid',
        'SENIOR': 'senior',
        'LEAD': 'lead',
        'EXECUTIVE': 'executive'
    }

# Utility functions
def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

def create_directories():
    """Create necessary directories"""
    directories = [
        Config.UPLOAD_FOLDER,
        'logs',
        'templates',
        'static/css',
        'static/js',
        'static/images'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Validation functions
def validate_file_type(filename):
    """Validate if file type is allowed"""
    if not filename:
        return False
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_file_size(file_size):
    """Validate if file size is within limits"""
    return file_size <= Config.MAX_CONTENT_LENGTH

# Error messages
ERROR_MESSAGES = {
    'INVALID_FILE_TYPE': 'Invalid file format. Please upload PDF, DOC, DOCX, or TXT files.',
    'FILE_TOO_LARGE': f'File too large. Maximum size is {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB.',
    'NO_FILE_SELECTED': 'No file selected for upload.',
    'ANALYSIS_FAILED': 'Resume analysis failed. Please try again.',
    'UNAUTHORIZED': 'You are not authorized to access this resource.',
    'SESSION_EXPIRED': 'Your session has expired. Please log in again.',
    'INVALID_CREDENTIALS': 'Invalid email or password.',
    'USER_EXISTS': 'A user with this email already exists.',
    'RESUME_NOT_FOUND': 'Resume not found or access denied.',
    'INTERVIEW_SESSION_NOT_FOUND': 'Interview session not found or access denied.',
    'QUESTION_GENERATION_FAILED': 'Failed to generate interview question. Please try again.',
    'ANSWER_VALIDATION_FAILED': 'Failed to validate answer. Please try again.',
    'ROADMAP_GENERATION_FAILED': 'Failed to generate roadmap. Please try again.'
}

# Success messages
SUCCESS_MESSAGES = {
    'RESUME_UPLOADED': 'Resume uploaded successfully! Analysis will be ready in a few minutes.',
    'PROFILE_UPDATED': 'Profile updated successfully!',
    'ACCOUNT_CREATED': 'Account created successfully! Please log in.',
    'LOGIN_SUCCESS': 'Welcome back!',
    'LOGOUT_SUCCESS': 'You have been logged out successfully.',
    'RESUME_DELETED': 'Resume deleted successfully.',
    'INTERVIEW_COMPLETED': 'Interview session completed successfully!',
    'APPLICATION_ADDED': 'Job application added successfully!',
    'APPLICATION_UPDATED': 'Application status updated successfully!',
    'ROADMAP_GENERATED': 'Roadmap generated successfully!'
}