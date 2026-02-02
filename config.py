"""
Configuration management for Job Bid Generator
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Upload directories
UPLOAD_FOLDER = BASE_DIR / 'uploads'
PRICING_SHEET_FOLDER = UPLOAD_FOLDER / 'pricing_sheets'
IMAGE_FOLDER = UPLOAD_FOLDER / 'images'
OUTPUT_FOLDER = BASE_DIR / 'generated_bids'

# Create directories if they don't exist
for folder in [UPLOAD_FOLDER, PRICING_SHEET_FOLDER, IMAGE_FOLDER, OUTPUT_FOLDER]:
    folder.mkdir(parents=True, exist_ok=True)

# File upload settings
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
ALLOWED_PRICING_EXTENSIONS = {'xlsx', 'xls', 'csv'}
MAX_IMAGE_SIZE = 16 * 1024 * 1024  # 16MB
MAX_PRICING_SIZE = 10 * 1024 * 1024  # 10MB

# OpenAI settings (from environment)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Business settings
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Premium Metal Fabrication & Welding')
COMPANY_ADDRESS = os.getenv('COMPANY_ADDRESS', '123 Industrial Way, Manufacturing City, ST 12345')
COMPANY_PHONE = os.getenv('COMPANY_PHONE', '(555) 123-4567')
COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'bids@metalfab.com')

# Bid settings
DEFAULT_PROFIT_MARGIN = float(os.getenv('PROFIT_MARGIN', '0.25'))  # 25%
DEFAULT_OVERHEAD_RATE = float(os.getenv('OVERHEAD_RATE', '0.15'))  # 15%
TAX_RATE = float(os.getenv('TAX_RATE', '0.08'))  # 8%

# Flask settings
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
