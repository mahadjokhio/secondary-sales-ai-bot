# Secondary Sales AI Bot - Sukkur Beverages

# Sukkur Beverages - Secondary Sales AI Bot

A comprehensive AI-powered sales management system built with Python/Streamlit and React, designed specifically for Sukkur Beverages Limited's secondary sales operations.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

## 🚀 Overview

This project provides a complete secondary sales management solution with both **Streamlit** (Python) and **React** implementations, featuring AI-powered assistance, voice commands, and comprehensive analytics.

### **Key Features**
- 🤖 **AI Sales Assistant** with Google Gemini integration
- 🎤 **Voice Commands** and text-to-speech responses
- 📊 **Real-time Analytics** and performance dashboards
- 🛒 **Order Management** system with complete workflow
- 🎁 **Promotion Management** and tracking
- 🏪 **Outlet Performance** monitoring
- 📈 **Advanced Reporting** with interactive charts
- 🎨 **Pepsi Brand Compliant** design system

## 📁 Project Structure

```
botsales/
├── 📱 Streamlit Application (Python)
│   ├── bot/                    # Main Streamlit app
│   ├── components/             # UI components
│   ├── config/                 # Configuration management
│   ├── utils/                  # Utility functions
│   ├── data/                   # Sample data (JSON)
│   └── requirements.txt        # Python dependencies
│
├── ⚛️ React Dashboard
│   ├── src/                    # React source code
│   ├── public/                 # Static assets
│   ├── package.json           # Node.js dependencies
│   └── preview.html           # Standalone HTML demo
│
└── 📚 Documentation
    ├── README.md              # This file
    └── setup/                 # Setup guides
```

## 🏃‍♂️ Quick Start

### **Option 1: Streamlit Application (Recommended)**

1. **Install Python dependencies:**
   ```bash
   cd botsales
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Add your Google API key to .env
   ```

3. **Run the application:**
   ```bash
   streamlit run bot/app.py
   ```

4. **Access the app:**
   - Local: http://localhost:8501
   - Network: http://[your-ip]:8501

### **Option 2: React Dashboard**

1. **Install Node.js dependencies:**
   ```bash
   cd react-dashboard
   npm install
   ```

2. **Start development server:**
   ```bash
   npm start
   ```

3. **Access the dashboard:**
   - Local: http://localhost:3000

### **Option 3: Instant Preview (No Installation)**

Open `react-dashboard/preview.html` directly in your browser for an immediate preview of the React dashboard.

## 🎯 Project Overview

**Company:** Sukkur Beverages (PepsiCo Distributor)  
**Tech Stack:** Python 3.9+, Streamlit, Google Gemini, Speech Recognition, TTS  
**Architecture:** Modular, component-based with comprehensive testing  

## ✨ Features

### 🤖 AI-Powered Sales Assistant
- **Natural Language Processing**: Understanding sales-specific queries
- **Voice Commands**: Speech-to-text and text-to-speech capabilities
- **Context Awareness**: Remembering conversation history
- **Action Execution**: Creating orders through conversation

### 📦 Order Management
- **Voice Orders**: "Create order for Ahmed Traders with 50 Pepsi bottles"
- **Smart Search**: Product search with fuzzy matching
- **Validation**: Stock availability, credit limits, business rules
- **Workflow**: Draft → Review → Confirm → Track → Invoice

### 🎯 Promotions & Analytics
- **Promotion Management**: Display and apply promotions automatically
- **Performance Reports**: Sales analytics with interactive charts
- **Outlet Management**: Credit tracking and performance metrics
- **Real-time Dashboard**: KPIs and live data updates

### 🔊 Voice Integration
- **Speech Recognition**: Google Speech-to-Text with error handling
- **Text-to-Speech**: Multilingual TTS with customizable voices
- **Voice Commands**: Natural language command processing
- **Audio Quality**: Noise filtering and validation

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Git
- Microphone (for voice features)
- Internet connection (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/sales-bot.git
   cd sales-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies (optional)**
   ```bash
   pip install -r requirements-dev.txt
   ```

5. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Application Settings
APP_TITLE=Secondary Sales AI Bot - Sukkur Beverages
DEBUG_MODE=True
LOG_LEVEL=INFO

# Voice Settings
VOICE_LANGUAGE=en-US
TTS_RATE=150
TTS_VOICE=female

# Performance Settings
MAX_CHAT_HISTORY=50
API_TIMEOUT=30
```

### Google Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file as `GOOGLE_API_KEY`

## 📁 Project Structure

```
sales_bot_project/
│
├── 📄 app.py                      # Main Streamlit application
├── 📄 requirements.txt            # Production dependencies
├── 📄 requirements-dev.txt        # Development dependencies
├── 📄 .env.example               # Environment variables template
├── 📄 README.md                  # This file
├── 📄 pytest.ini                # Pytest configuration
│
├── 📁 config/
│   ├── 📄 __init__.py
│   └── 📄 settings.py            # Configuration management
│
├── 📁 components/
│   ├── 📄 __init__.py
│   ├── 📄 voice_handler.py       # Voice processing
│   ├── 📄 order_manager.py       # Order management
│   ├── 📄 chat_interface.py      # AI chat
│   ├── 📄 promotions.py          # Promotions
│   ├── 📄 outlets.py             # Outlet management
│   └── 📄 reports.py             # Reporting
│
├── 📁 utils/
│   ├── 📄 __init__.py
│   ├── 📄 llm_handler.py         # AI integration
│   ├── 📄 data_processor.py      # Data processing
│   ├── 📄 validators.py          # Input validation
│   └── 📄 exceptions.py          # Custom exceptions
│
├── 📁 data/
│   ├── 📄 products.json          # Product catalog
│   ├── 📄 outlets.json           # Outlet database
│   ├── 📄 promotions.json        # Promotions
│   ├── 📄 orders.json            # Order history
│   └── 📄 company_knowledge.json # Company info
│
└── 📁 tests/
    ├── 📄 conftest.py            # Test configuration
    └── 📄 test_*.py              # Test files
```

## 🎮 Usage Guide

### Dashboard
- View key performance indicators (KPIs)
- Monitor today's sales metrics
- Check system status and alerts
- Quick access to all features

### Order Management
1. **Select Outlet**: Choose from active outlets
2. **Add Products**: Search and add products to order
3. **Review**: Check totals, apply discounts
4. **Confirm**: Validate credit limits and submit

### Voice Commands

#### Order Commands
- "Create order for Ahmed Traders"
- "Add 10 Pepsi 500ml to order"
- "Show me the order total"
- "Confirm and submit this order"

#### Query Commands
- "What's the price of Pepsi 500ml?"
- "Show active promotions"
- "Display outlet performance"
- "Generate sales report for today"

#### Navigation Commands
- "Go to dashboard"
- "Open order management"
- "Show outlet information"

### AI Chat
- Ask questions about products, pricing, and company info
- Get sales recommendations
- Process natural language requests
- Execute actions through conversation




-
