import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import sys
import time

@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application - can be overridden via environment variable"""
    return os.getenv("TEST_BASE_URL", "http://localhost:80")

@pytest.fixture(scope="function")
def driver():
    """Create a new Chrome driver instance for each test"""
    chrome_options = Options()
    
    # Essential headless settings for Jenkins/EC2
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    
    # SSL and Security Settings for HTTPS
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Additional stability settings
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins')
    chrome_options.add_argument('--disable-images')
    chrome_options.add_argument('--disable-javascript-harmony-shipping')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    
    # Set page load strategy for faster tests
    chrome_options.page_load_strategy = 'eager'
    
    # Get the current directory for chromedriver
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set up ChromeDriver path - check multiple common locations
    chromedriver_paths = []
    
    if sys.platform == "win32":
        chromedriver_paths = [
            os.path.join(current_dir, "chromedriver.exe"),
            r"C:\chromedriver\chromedriver.exe",
            "chromedriver.exe"
        ]
    else:
        chromedriver_paths = [
            "/usr/local/bin/chromedriver",  # Docker/system installation
            os.path.join(current_dir, "chromedriver"),  # Local directory
            "/usr/bin/chromedriver",  # Alternative system path
            "chromedriver"  # PATH
        ]
    
    # Find the first existing chromedriver
    chromedriver_path = None
    for path in chromedriver_paths:
        if os.path.exists(path):
            chromedriver_path = path
            break
    
    # Verify chromedriver exists
    if not chromedriver_path:
        raise FileNotFoundError(f"ChromeDriver not found in any of these locations: {chromedriver_paths}")
    
    # Create service with explicit path
    service = Service(executable_path=chromedriver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        yield driver
        
    except Exception as e:
        print(f"Error creating Chrome driver: {e}")
        raise
    finally:
        try:
            driver.quit()
        except:
            pass 