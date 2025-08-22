#!/usr/bin/env python3
"""
Setup script for Secondary Sales AI Bot
Helps configure environment variables and dependencies
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# Environment Configuration for Secondary Sales AI Bot
# Fill in your actual values

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
MAX_RETRIES=3
TIMEOUT_SECONDS=30

# Data Configuration
DATA_PATH=./data/
BACKUP_ENABLED=True

# Voice Configuration
VOICE_RATE=200
VOICE_VOLUME=0.9

# Security
SECRET_KEY=your_secret_key_here
"""
        env_file.write_text(env_content)
        print("✅ .env file created!")
        print("⚠️  Please edit .env file and add your Google API key")
    else:
        print("✅ .env file already exists")

def check_api_key():
    """Check if Google API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("❌ Google API key not configured")
        print("📝 Get your API key from: https://makersuite.google.com/app/apikey")
        print("📝 Then edit .env file and replace 'your_google_api_key_here' with your actual key")
        return False
    else:
        print("✅ Google API key configured")
        return True

def main():
    """Main setup function"""
    print("🤖 Secondary Sales AI Bot Setup")
    print("=" * 40)
    
    # Setup environment
    setup_environment()
    
    # Check API key
    api_configured = check_api_key()
    
    print("\n📋 Next Steps:")
    if not api_configured:
        print("1. Get Google API key from: https://makersuite.google.com/app/apikey")
        print("2. Edit .env file and add your API key")
        print("3. Run: streamlit run bot/app.py")
    else:
        print("1. Run: streamlit run bot/app.py")
        print("2. Open browser to: http://localhost:8501")
    
    print("\n🎉 Setup complete!")

if __name__ == "__main__":
    main()
