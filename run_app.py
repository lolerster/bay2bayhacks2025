#!/usr/bin/env python3
"""
Bay2BayHacks2025 - AI Notes App Launcher
This script helps you run both the FastAPI backend and Streamlit frontend.
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['fastapi', 'uvicorn', 'streamlit', 'openai', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists."""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    return True

def main():
    print("🚀 Bay2BayHacks2025 - AI Notes App Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("\n📋 Available options:")
    print("1. Run FastAPI backend only")
    print("2. Run Streamlit frontend only")
    print("3. Run both (recommended)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting FastAPI backend...")
        print("API will be available at: http://localhost:8000")
        print("API docs at: http://localhost:8000/docs")
        print("Press Ctrl+C to stop")
        subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    
    elif choice == "2":
        print("\n🚀 Starting Streamlit frontend...")
        print("Frontend will be available at: http://localhost:8501")
        print("Press Ctrl+C to stop")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
    
    elif choice == "3":
        print("\n🚀 Starting both FastAPI backend and Streamlit frontend...")
        print("API: http://localhost:8000")
        print("Frontend: http://localhost:8501")
        print("API docs: http://localhost:8000/docs")
        print("\n⏳ Starting services...")
        
        # Start FastAPI in background
        api_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
        
        # Wait a moment for API to start
        time.sleep(3)
        
        # Start Streamlit
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"
            ])
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
        finally:
            api_process.terminate()
            api_process.wait()
            print("✅ Services stopped")
    
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
