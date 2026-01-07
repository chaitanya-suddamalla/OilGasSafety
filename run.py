#!/usr/bin/env python
"""
Oil & Gas Safety Bot - Startup and Installation Script
Handles dependency installation and server startup
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Run a command and return success status"""
    if description:
        print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0 and "already satisfied" not in result.stderr:
            print(f"Warning: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Oil & Gas Plant Safety Bot - Server Startup")
    print("=" * 60)
    
    # Get Python executable
    python_exe = sys.executable
    print(f"Using Python: {python_exe}")
    print(f"Python Version: {sys.version}")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working Directory: {os.getcwd()}")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\nWARNING: .env file not found!")
        print("Please create a .env file with your API key:")
        print("  GENAI_API_KEY=your_api_key_here")
        input("\nPress Enter after creating the .env file...")
    else:
        print("\n✓ .env file found")
    
    # Install requirements
    print("\n" + "=" * 60)
    print("Installing Python dependencies...")
    print("=" * 60)
    
    requirements = [
        ('Flask', 'Flask>=2.0.0,<3.0.0'),
        ('dotenv', 'python-dotenv>=1.0.0'),
    ]
    
    # google.generativeai is optional (server has demo fallback)
    optional_packages = [
        ('google.generativeai', 'google-generativeai==0.3.0'),
    ]
    
    # First, uninstall any incompatible google-generativeai version
    print("  Cleaning up incompatible packages...")
    subprocess.run(f"{python_exe} -m pip uninstall -y google-generativeai 2>/dev/null", 
                   shell=True, capture_output=True)
    
    for import_name, package_name in requirements:
        try:
            __import__(import_name)
            print(f"✓ {package_name.split('>=')[0].split('==')[0]} already installed")
        except ImportError:
            print(f"  Installing {package_name.split('>=')[0].split('==')[0]}...")
            cmd = f"{python_exe} -m pip install {package_name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ {package_name.split('>=')[0].split('==')[0]} installed successfully")
            else:
                print(f"  ✗ Failed to install {package_name.split('>=')[0].split('==')[0]}")
    
    # Try to install optional google.generativeai (will fail gracefully)
    print("\n  Optional: Trying to install google-generativeai...")
    for import_name, package_name in optional_packages:
        try:
            __import__(import_name)
            print(f"  ✓ google-generativeai already installed")
        except ImportError:
            print(f"    Attempting to install google-generativeai...")
            cmd = f"{python_exe} -m pip install {package_name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"    ✓ google-generativeai installed")
            else:
                print(f"    ⚠ google-generativeai not available (server will use demo mode)")
                print(f"      This is OK - server includes demo responses for safety questions")
    
    # Start server
    print("\n" + "=" * 60)
    
    print("Starting Flask Server")
    print("=" * 60)
    print("\nServer running on: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        os.execvp(python_exe, [python_exe, 'server.py'])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
