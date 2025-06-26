#!/usr/bin/env python3
"""
Setup script for PDF Chatbot Selenium Test Environment
This script helps set up the testing environment including ChromeDriver installation.
"""

import os
import sys
import platform
import requests
import zipfile
import tarfile
import subprocess
from pathlib import Path

def get_chrome_version():
    """Get installed Chrome version"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Try to get Chrome version from registry or file version
            import winreg
            reg_path = r"SOFTWARE\Google\Chrome\BLBeacon"
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
            version, _ = winreg.QueryValueEx(reg_key, "version")
            winreg.CloseKey(reg_key)
            return version
        
        elif system == "Darwin":  # macOS
            result = subprocess.run([
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", 
                "--version"
            ], capture_output=True, text=True)
            return result.stdout.strip().split()[-1]
        
        elif system == "Linux":
            result = subprocess.run([
                "google-chrome", "--version"
            ], capture_output=True, text=True)
            if result.returncode != 0:
                # Try chromium
                result = subprocess.run([
                    "chromium-browser", "--version"
                ], capture_output=True, text=True)
            return result.stdout.strip().split()[-1]
    
    except Exception as e:
        print(f"Could not detect Chrome version: {e}")
        return None

def get_chromedriver_url(chrome_version):
    """Get ChromeDriver download URL for the given Chrome version"""
    if not chrome_version:
        print("Chrome version not detected, using latest ChromeDriver")
        return get_latest_chromedriver_url()
    
    major_version = chrome_version.split('.')[0]
    
    # ChromeDriver version mapping (simplified)
    # For production use, you'd want to use the ChromeDriver API
    base_url = "https://chromedriver.storage.googleapis.com"
    
    try:
        # Get latest version for major Chrome version
        response = requests.get(f"{base_url}/LATEST_RELEASE_{major_version}")
        if response.status_code == 200:
            driver_version = response.text.strip()
            system = platform.system()
            
            if system == "Windows":
                filename = "chromedriver_win32.zip"
            elif system == "Darwin":
                filename = "chromedriver_mac64.zip"
            elif system == "Linux":
                filename = "chromedriver_linux64.zip"
            else:
                raise Exception(f"Unsupported system: {system}")
            
            return f"{base_url}/{driver_version}/{filename}"
    
    except Exception as e:
        print(f"Error getting ChromeDriver URL: {e}")
        return get_latest_chromedriver_url()

def get_latest_chromedriver_url():
    """Get latest ChromeDriver URL"""
    base_url = "https://chromedriver.storage.googleapis.com"
    system = platform.system()
    
    try:
        response = requests.get(f"{base_url}/LATEST_RELEASE")
        driver_version = response.text.strip()
        
        if system == "Windows":
            filename = "chromedriver_win32.zip"
        elif system == "Darwin":
            filename = "chromedriver_mac64.zip"
        elif system == "Linux":
            filename = "chromedriver_linux64.zip"
        else:
            raise Exception(f"Unsupported system: {system}")
        
        return f"{base_url}/{driver_version}/{filename}"
    
    except Exception as e:
        print(f"Error getting latest ChromeDriver: {e}")
        return None

def download_chromedriver(url, destination):
    """Download and extract ChromeDriver"""
    print(f"Downloading ChromeDriver from: {url}")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Download to temporary file
        temp_file = destination.parent / "chromedriver_temp.zip"
        
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Extracting ChromeDriver...")
        
        # Extract the file
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            # Extract chromedriver executable
            for member in zip_ref.namelist():
                if 'chromedriver' in member.lower():
                    # Extract to destination
                    with zip_ref.open(member) as source, open(destination, 'wb') as target:
                        target.write(source.read())
                    break
        
        # Make executable on Unix systems
        if platform.system() != "Windows":
            os.chmod(destination, 0o755)
        
        # Clean up temp file
        temp_file.unlink()
        
        print(f"✓ ChromeDriver installed at: {destination}")
        return True
    
    except Exception as e:
        print(f"✗ Error downloading ChromeDriver: {e}")
        return False

def install_python_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    
    test_dir = Path(__file__).parent
    requirements_file = test_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("✗ requirements.txt not found!")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✓ Python dependencies installed successfully")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def check_chrome_installation():
    """Check if Chrome is installed"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Check common Chrome installation paths
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    print("✓ Google Chrome found")
                    return True
        
        elif system == "Darwin":
            if os.path.exists("/Applications/Google Chrome.app"):
                print("✓ Google Chrome found")
                return True
        
        elif system == "Linux":
            result = subprocess.run(["which", "google-chrome"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Google Chrome found")
                return True
            
            result = subprocess.run(["which", "chromium-browser"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Chromium browser found")
                return True
    
    except Exception:
        pass
    
    print("✗ Google Chrome not found. Please install Google Chrome first.")
    return False

def main():
    """Main setup function"""
    print("=== PDF Chatbot Selenium Test Environment Setup ===\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check Chrome installation
    if not check_chrome_installation():
        return False
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"✓ Chrome version: {chrome_version}")
    else:
        print("? Chrome version detection failed, will use latest ChromeDriver")
    
    # Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Setup ChromeDriver
    test_dir = Path(__file__).parent
    system = platform.system()
    
    if system == "Windows":
        chromedriver_path = test_dir / "chromedriver.exe"
    else:
        chromedriver_path = test_dir / "chromedriver"
    
    # Check if ChromeDriver already exists
    if chromedriver_path.exists():
        print(f"? ChromeDriver already exists at: {chromedriver_path}")
        response = input("Do you want to download a new version? (y/N): ")
        if response.lower() != 'y':
            print("✓ Using existing ChromeDriver")
            print("\n=== Setup Complete ===")
            print("Run tests with: python run_tests.py")
            return True
    
    # Download ChromeDriver
    url = get_chromedriver_url(chrome_version)
    if not url:
        print("✗ Could not determine ChromeDriver download URL")
        return False
    
    if download_chromedriver(url, chromedriver_path):
        print("\n=== Setup Complete ===")
        print("You can now run tests with: python run_tests.py")
        
        # Show configuration options
        print("\nConfiguration options:")
        print("- Set TEST_BASE_URL environment variable to test different URLs")
        print(f"- Default URL: http://localhost:80")
        print(f"- Example: export TEST_BASE_URL='https://your-domain.com'")
        
        return True
    else:
        print("\n✗ Setup failed. Please install ChromeDriver manually.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 