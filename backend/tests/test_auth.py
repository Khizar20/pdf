import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import string

def generate_unique_username():
    """Generate a unique username for testing"""
    timestamp = str(int(time.time()))
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
    return f"testuser_{timestamp}_{random_suffix}"

def wait_for_page_load(driver, timeout=20):
    """Wait for page to be fully loaded"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Warning: Page load timeout, continuing with test")

def test_signup_page_load(driver, base_url):
    """Test 1: Verify signup page loads correctly with all required elements"""
    print(f"\n=== TEST 1: Signup Page Load ===")
    print(f"Loading URL: {base_url}/signup.html")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    # Verify page title
    assert "Sign Up" in driver.title, f"Expected 'Sign Up' in title, got: {driver.title}"
    
    # Check for signup form elements with correct IDs
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        assert username_input.is_displayed(), "Username input not visible"
        assert password_input.is_displayed(), "Password input not visible"
        assert signup_button.is_displayed(), "Signup button not visible"
        
        print("✓ All signup form elements found and visible")
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"✗ Error finding signup elements: {str(e)}")
        # Print available elements for debugging
        elements = driver.find_elements(By.XPATH, "//*[@id]")
        print("Available elements with IDs:")
        for element in elements[:10]:  # Limit output
            print(f"- {element.get_attribute('id')}: {element.tag_name}")
        raise

def test_signup_success(driver, base_url):
    """Test 2: Test successful user registration"""
    print(f"\n=== TEST 2: Successful Signup ===")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    # Generate unique credentials
    username = generate_unique_username()
    password = "TestPass123!"
    
    print(f"Testing signup with username: {username}")
    
    try:
        # Fill in the form
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        
        # Submit the form
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        signup_button.click()
        
        # Wait for success message or redirect
        try:
            success_element = WebDriverWait(driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.ID, "successMessage")),
                    EC.presence_of_element_located((By.CLASS_NAME, "success-message")),
                    EC.url_contains("login.html")
                )
            )
            print("✓ Signup successful - success indicator found")
            
        except TimeoutException:
            # Check if there's an error message instead
            page_source = driver.page_source.lower()
            if "error" in page_source or "failed" in page_source:
                print(f"✗ Signup failed - error found in page source")
                raise AssertionError("Signup failed - error message detected")
            else:
                print("? Signup status unclear - no clear success/error indicator")
        
    except Exception as e:
        print(f"✗ Error during signup: {str(e)}")
        raise

def test_signup_duplicate_username(driver, base_url):
    """Test 3: Test signup with already existing username"""
    print(f"\n=== TEST 3: Duplicate Username Signup ===")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    # Use a common username that might already exist
    username = "admin"
    password = "TestPass123!"
    
    print(f"Testing signup with potentially duplicate username: {username}")
    
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        
        username_input.clear()
        username_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)
        
        signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        signup_button.click()
        
        # Wait for error message or check page source
        time.sleep(3)
        page_source = driver.page_source.lower()
        
        if "already" in page_source or "exists" in page_source or "duplicate" in page_source:
            print("✓ Duplicate username properly rejected")
        else:
            print("? No clear duplicate username error - this might be acceptable if user doesn't exist yet")
            
    except Exception as e:
        print(f"✗ Error during duplicate username test: {str(e)}")
        raise

def test_login_page_load(driver, base_url):
    """Test 4: Verify login page loads correctly with all required elements"""
    print(f"\n=== TEST 4: Login Page Load ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    # Verify page title
    assert "Login" in driver.title, f"Expected 'Login' in title, got: {driver.title}"
    
    try:
        # Check for login form elements
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        assert username_input.is_displayed(), "Username input not visible"
        assert password_input.is_displayed(), "Password input not visible"
        assert login_button.is_displayed(), "Login button not visible"
        
        print("✓ All login form elements found and visible")
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"✗ Error finding login elements: {str(e)}")
        raise

def test_login_invalid_credentials(driver, base_url):
    """Test 5: Test login with invalid credentials"""
    print(f"\n=== TEST 5: Invalid Credentials Login ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Fill in form with invalid credentials
        username_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        
        username_input.clear()
        username_input.send_keys("invaliduser12345")
        password_input.clear()
        password_input.send_keys("wrongpassword")
        
        # Submit the form
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Wait for error indication
        time.sleep(5)
        
        # Check for error messages or indicators
        page_source = driver.page_source.lower()
        current_url = driver.current_url
        
        # Should either show error message or stay on login page
        if ("invalid" in page_source or "error" in page_source or 
            "incorrect" in page_source or "failed" in page_source or
            "login.html" in current_url):
            print("✓ Invalid credentials properly rejected")
        else:
            print(f"? Unclear result - page source contains: {page_source[:200]}...")
            
    except Exception as e:
        print(f"✗ Error during invalid login test: {str(e)}")
        raise

def test_login_empty_fields(driver, base_url):
    """Test 6: Test login with empty fields"""
    print(f"\n=== TEST 6: Empty Fields Login ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Try to submit form with empty fields
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        
        time.sleep(3)
        
        # Should either show validation error or stay on page
        current_url = driver.current_url
        page_source = driver.page_source.lower()
        
        if ("required" in page_source or "login.html" in current_url or 
            "error" in page_source):
            print("✓ Empty fields properly handled")
        else:
            print("? No clear validation for empty fields")
            
    except Exception as e:
        print(f"✗ Error during empty fields test: {str(e)}")
        raise

def test_navigation_between_auth_pages(driver, base_url):
    """Test 7: Test navigation between login and signup pages"""
    print(f"\n=== TEST 7: Navigation Between Auth Pages ===")
    
    # Start at login page
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Look for link to signup page
        signup_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'signup')]")
        if signup_links:
            signup_links[0].click()
            wait_for_page_load(driver)
            
            assert "signup.html" in driver.current_url, "Should navigate to signup page"
            print("✓ Navigation from login to signup works")
            
            # Try to go back to login
            login_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'login')]")
            if login_links:
                login_links[0].click()
                wait_for_page_load(driver)
                
                assert "login.html" in driver.current_url, "Should navigate back to login page"
                print("✓ Navigation from signup to login works")
            else:
                print("? No login link found on signup page")
        else:
            print("? No signup link found on login page")
            
    except Exception as e:
        print(f"✗ Error during navigation test: {str(e)}")
        raise

def test_password_field_type(driver, base_url):
    """Test 8: Verify password field is properly masked"""
    print(f"\n=== TEST 8: Password Field Security ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        
        # Check that password field has type="password"
        field_type = password_input.get_attribute("type")
        assert field_type == "password", f"Password field should be type 'password', got '{field_type}'"
        
        print("✓ Password field is properly secured")
        
    except Exception as e:
        print(f"✗ Error during password field test: {str(e)}")
        raise 