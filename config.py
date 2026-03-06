"""
Configuration settings for the Customer Service Analytics Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application Settings
APP_NAME = "Intelligent Customer Service Analytics Platform"
APP_VERSION = "2.0.0-enterprise"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# File Upload Settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_FILE_TYPES = {'txt', 'pdf'}

# NLP Settings
MIN_TEXT_LENGTH = 10
KEYWORD_EXTRACTION_TOP_N = 15

# Performance Settings
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API Settings
API_TIMEOUT = 30
MAX_BATCH_SIZE = 100

# Industry Configurations
INDUSTRIES = {
    "E-Commerce": {
        "keywords": ["product", "shipping", "quality", "price"],
        "focus_areas": ["Product Quality", "Delivery", "Customer Service"]
    },
    "SaaS": {
        "keywords": ["feature", "bug", "performance", "support"],
        "focus_areas": ["User Experience", "Performance", "Support"]
    },
    "Hospitality": {
        "keywords": ["staff", "cleanliness", "service", "location"],
        "focus_areas": ["Service Quality", "Facilities", "Staff"]
    },
    "Healthcare": {
        "keywords": ["doctor", "treatment", "wait", "care"],
        "focus_areas": ["Care Quality", "Wait Times", "Staff"]
    }
}

# Sentiment Thresholds
POLARITY_POSITIVE_THRESHOLD = 0.1
POLARITY_NEGATIVE_THRESHOLD = -0.1
SUBJECTIVITY_HIGH_THRESHOLD = 0.7
SUBJECTIVITY_LOW_THRESHOLD = 0.3