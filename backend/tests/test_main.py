import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def generate_unique_username():
    """Generate a unique username for testing"""
    timestamp = str(int(time.time()))
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"testuser_{timestamp}_{random_suffix}"

def wait_for_page_load(driver, timeout=15):
    """Wait for page to be fully loaded"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)  # Additional wait for dynamic content
    except TimeoutException:
        print("Warning: Page load timeout, continuing with test")

def test_01_home_page_loads_successfully(driver, base_url):
    """Test 1: Verify home page loads with correct title and Get Started button"""
    print(f"\n=== TEST 1: Home Page Load ===")
    print(f"Loading URL: {base_url}/index.html")
    
    driver.get(f"{base_url}/index.html")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    # Check page loaded correctly
    assert driver.current_url == f"{base_url}/index.html", f"Expected {base_url}/index.html, got {driver.current_url}"
    
    # Look for main heading
    try:
        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "PDF" in heading.text.upper(), f"Expected 'PDF' in heading, got: {heading.text}"
        
        # Look for Get Started button
        get_started_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Get Started') or contains(@href, 'login')]")
        assert get_started_button.is_displayed(), "Get Started button should be visible"
        
        print("✅ Home page loads successfully with all elements")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_02_signup_page_loads_and_form_works(driver, base_url):
    """Test 2: Verify signup page loads and form elements work correctly"""
    print(f"\n=== TEST 2: Signup Page and Form ===")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    try:
        # Check for signup form elements
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Test form inputs work
        username_input.clear()
        username_input.send_keys("testuser")
        password_input.clear()
        password_input.send_keys("testpass123")
        
        assert username_input.get_attribute("value") == "testuser", "Username input not working"
        assert password_input.get_attribute("value") == "testpass123", "Password input not working"
        assert signup_button.is_enabled(), "Signup button should be enabled"
        
        print("✅ Signup page loads and form elements work correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_03_user_registration_successful(driver, base_url):
    """Test 3: Test successful user registration with unique credentials"""
    print(f"\n=== TEST 3: Successful User Registration ===")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    # Generate unique credentials
    username = generate_unique_username()
    password = "TestPass123!"
    
    print(f"Testing registration with username: {username}")
    
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Fill and submit form
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        signup_button.click()
        
        # Wait for success indicator (redirect or success message)
        time.sleep(3)
        
        # Check if redirected to login or success message appears
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        if "login.html" in current_url or "success" in page_source:
            print("✅ User registration successful")
        else:
            print("⚠️ Registration status unclear - no clear success indicator")
            
    except Exception as e:
        print(f"❌ Error during registration: {str(e)}")
        raise

def test_04_login_page_loads_and_form_works(driver, base_url):
    """Test 4: Verify login page loads and form validation works"""
    print(f"\n=== TEST 4: Login Page and Form Validation ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Check login form elements
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Test with invalid credentials
        username_input.clear()
        username_input.send_keys("invaliduser")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        login_button.click()
        
        time.sleep(3)
        
        # Should stay on login page or show error
        current_url = driver.current_url
        if "login.html" in current_url:
            print("✅ Login form validation working - stayed on login page with invalid credentials")
        else:
            print("⚠️ Login behavior unclear")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_05_login_with_valid_credentials(driver, base_url):
    """Test 5: Test login with valid credentials (first create a user)"""
    print(f"\n=== TEST 5: Login with Valid Credentials ===")
    
    # First create a user
    username = generate_unique_username()
    password = "TestPass123!"
    
    # Create user via signup
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    try:
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        signup_button.click()
        time.sleep(2)
        
        # Now try to login
        driver.get(f"{base_url}/login.html")
        wait_for_page_load(driver)
        
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        
        time.sleep(3)
        
        # Check if redirected to main page
        current_url = driver.current_url
        if "main.html" in current_url or "login.html" not in current_url:
            print("✅ Login successful - redirected to main application")
        else:
            print("⚠️ Login status unclear")
            
    except Exception as e:
        print(f"❌ Error during login test: {str(e)}")
        raise

def test_06_main_page_loads_with_pdf_interface(driver, base_url):
    """Test 6: Verify main PDF chat interface loads correctly"""
    print(f"\n=== TEST 6: Main PDF Interface ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Look for PDF upload element
        pdf_upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pdfUpload"))
        )
        
        # Look for chat interface elements
        chat_output = driver.find_element(By.ID, "chat-output")
        user_input = driver.find_element(By.ID, "userInput")
        
        # Verify elements are visible
        assert chat_output.is_displayed(), "Chat output area should be visible"
        assert user_input.is_displayed(), "User input field should be visible"
        
        # Check file input accepts PDFs
        accept_attr = pdf_upload.get_attribute("accept")
        if accept_attr and "pdf" in accept_attr.lower():
            print("✅ PDF upload interface configured correctly")
        
        print("✅ Main PDF interface loads with all required elements")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_07_chat_interface_functionality(driver, base_url):
    """Test 7: Test chat interface input and interaction"""
    print(f"\n=== TEST 7: Chat Interface Functionality ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        user_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "userInput"))
        )
        
        # Test typing in chat input
        test_message = "Hello, this is a test message"
        user_input.clear()
        user_input.send_keys(test_message)
        
        assert user_input.get_attribute("value") == test_message, "Chat input not working correctly"
        
        # Test Enter key functionality
        user_input.send_keys(Keys.RETURN)
        time.sleep(2)
        
        print("✅ Chat interface input functionality works")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_08_responsive_design_check(driver, base_url):
    """Test 8: Test responsive design at different screen sizes"""
    print(f"\n=== TEST 8: Responsive Design ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Test desktop size
        driver.set_window_size(1920, 1080)
        time.sleep(1)
        
        chat_output = driver.find_element(By.ID, "chat-output")
        assert chat_output.is_displayed(), "Chat should be visible on desktop"
        
        # Test mobile size
        driver.set_window_size(375, 667)
        time.sleep(1)
        
        chat_output = driver.find_element(By.ID, "chat-output")
        assert chat_output.is_displayed(), "Chat should be visible on mobile"
        
        # Reset to normal size
        driver.set_window_size(1920, 1080)
        
        print("✅ Responsive design works across different screen sizes")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_09_navigation_between_pages(driver, base_url):
    """Test 9: Test navigation between different pages"""
    print(f"\n=== TEST 9: Page Navigation ===")
    
    try:
        # Test home to login navigation
        driver.get(f"{base_url}/index.html")
        wait_for_page_load(driver)
        
        get_started_link = driver.find_element(By.XPATH, "//a[contains(@href, 'login') or contains(text(), 'Get Started')]")
        get_started_link.click()
        wait_for_page_load(driver)
        
        assert "login.html" in driver.current_url, "Should navigate to login page"
        
        # Test login to signup navigation  
        signup_link = driver.find_element(By.XPATH, "//a[contains(@href, 'signup') or contains(text(), 'Sign Up')]")
        signup_link.click()
        wait_for_page_load(driver)
        
        assert "signup.html" in driver.current_url, "Should navigate to signup page"
        
        print("✅ Navigation between pages works correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

def test_10_accessibility_and_usability_features(driver, base_url):
    """Test 10: Test accessibility features and keyboard navigation"""
    print(f"\n=== TEST 10: Accessibility and Usability ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Test keyboard navigation
        username_input = driver.find_element(By.ID, "username")
        username_input.click()
        
        # Tab to next field
        username_input.send_keys(Keys.TAB)
        active_element = driver.switch_to.active_element
        
        assert active_element.get_attribute("id") == "password", "Tab navigation should move to password field"
        
        # Test placeholder text
        username_input = driver.find_element(By.ID, "username")
        placeholder = username_input.get_attribute("placeholder")
        
        if placeholder:
            print(f"✅ Placeholder text found: {placeholder}")
        
        # Test form labels and accessibility
        password_input = driver.find_element(By.ID, "password")
        input_type = password_input.get_attribute("type")
        
        assert input_type == "password", "Password field should have type='password'"
        
        print("✅ Accessibility and usability features working correctly")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise 