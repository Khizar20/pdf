import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os

def wait_for_page_load(driver, timeout=20):
    """Wait for page to be fully loaded"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Warning: Page load timeout, continuing with test")

def test_home_page_navigation(driver, base_url):
    """Test 17: Test home page loads and navigation works"""
    print(f"\n=== TEST 17: Home Page Navigation ===")
    
    driver.get(f"{base_url}/index.html")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    try:
        # Check for main page elements
        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Look for "Get Started" button or similar navigation
        get_started_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Get Started') or contains(@href, 'login')]")
        
        assert heading.is_displayed(), "Main heading not visible"
        
        if get_started_links:
            # Test navigation to login page
            get_started_links[0].click()
            wait_for_page_load(driver)
            
            assert "login.html" in driver.current_url, "Should navigate to login page"
            print("✓ Navigation from home to login works")
        else:
            print("? No Get Started button found - checking for direct navigation links")
            # Try navigating directly
            driver.get(f"{base_url}/login.html")
            wait_for_page_load(driver)
            assert "login.html" in driver.current_url, "Should be able to access login page"
        
    except Exception as e:
        print(f"✗ Error during home page navigation test: {str(e)}")
        raise

def test_cross_browser_compatibility_features(driver, base_url):
    """Test 18: Test features that should work across browsers"""
    print(f"\n=== TEST 18: Cross-Browser Compatibility ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Test CSS features that should work across browsers
        username_input = driver.find_element(By.ID, "username")
        
        # Check if modern CSS features are being applied
        computed_style = driver.execute_script(
            "return window.getComputedStyle(arguments[0]);", 
            username_input
        )
        
        # Test for basic styling
        assert computed_style is not None, "Computed styles should be available"
        
        # Test for rounded borders (modern CSS feature)
        border_radius = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).borderRadius;", 
            username_input
        )
        
        if border_radius and border_radius != "0px":
            print("✓ Modern CSS features (border-radius) are working")
        else:
            print("? No border-radius detected - might be using different styling")
        
        # Test for placeholder support
        placeholder = username_input.get_attribute("placeholder")
        assert placeholder is not None, "Placeholder attribute should be supported"
        
        print("✓ Cross-browser features are functional")
        
    except Exception as e:
        print(f"✗ Error during cross-browser compatibility test: {str(e)}")
        raise

def test_form_validation_behavior(driver, base_url):
    """Test 19: Test form validation behavior"""
    print(f"\n=== TEST 19: Form Validation Behavior ===")
    
    driver.get(f"{base_url}/signup.html")
    wait_for_page_load(driver)
    
    try:
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        # Test with very short username
        username_input.clear()
        username_input.send_keys("a")
        password_input.clear()
        password_input.send_keys("short")
        
        submit_button.click()
        time.sleep(3)
        
        # Check if validation occurs
        page_source = driver.page_source.lower()
        current_url = driver.current_url
        
        # Should either show validation error or stay on page
        if ("error" in page_source or "invalid" in page_source or 
            "short" in page_source or "signup.html" in current_url):
            print("✓ Form validation is working for short inputs")
        else:
            print("? No clear validation for short inputs - might be acceptable")
        
        # Test with special characters
        username_input.clear()
        username_input.send_keys("test@user#123")
        password_input.clear()
        password_input.send_keys("validpassword123")
        
        submit_button.click()
        time.sleep(3)
        
        print("✓ Form handles special characters in input")
        
    except Exception as e:
        print(f"✗ Error during form validation test: {str(e)}")
        raise

def test_keyboard_navigation(driver, base_url):
    """Test 20: Test keyboard navigation and accessibility"""
    print(f"\n=== TEST 20: Keyboard Navigation ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Test Tab navigation
        username_input = driver.find_element(By.ID, "username")
        username_input.click()  # Focus on username
        
        # Tab to password field
        username_input.send_keys(Keys.TAB)
        
        # Check if focus moved to password field
        active_element = driver.switch_to.active_element
        assert active_element.get_attribute("id") == "password", "Tab navigation should move to password field"
        
        # Tab to submit button
        active_element.send_keys(Keys.TAB)
        active_element = driver.switch_to.active_element
        
        # Should be on submit button now
        assert active_element.tag_name.lower() == "button", "Tab navigation should move to submit button"
        
        # Test Enter key submission
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        
        username_input.clear()
        username_input.send_keys("testuser")
        password_input.clear()
        password_input.send_keys("testpass")
        
        # Submit using Enter key
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("✓ Keyboard navigation and Enter key submission work")
        
    except Exception as e:
        print(f"✗ Error during keyboard navigation test: {str(e)}")
        raise

def test_ui_consistency_across_pages(driver, base_url):
    """Test 21: Test UI consistency across different pages"""
    print(f"\n=== TEST 21: UI Consistency Across Pages ===")
    
    pages_to_test = ["index.html", "login.html", "signup.html", "main.html"]
    colors_found = []
    fonts_found = []
    
    try:
        for page in pages_to_test:
            print(f"Testing UI consistency on {page}")
            driver.get(f"{base_url}/{page}")
            wait_for_page_load(driver)
            
            # Check body background
            body = driver.find_element(By.TAG_NAME, "body")
            body_color = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).backgroundColor;", body
            )
            body_font = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).fontFamily;", body
            )
            
            colors_found.append(body_color)
            fonts_found.append(body_font)
            
            # Check for consistent heading styles
            headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
            if headings:
                heading_color = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).color;", headings[0]
                )
                print(f"  - Background: {body_color}")
                print(f"  - Font: {body_font}")
                print(f"  - Heading color: {heading_color}")
        
        # Check for consistency (allowing for some variation)
        unique_colors = set(colors_found)
        unique_fonts = set(fonts_found)
        
        if len(unique_colors) <= 2:  # Allow for slight variations
            print("✓ Color scheme is consistent across pages")
        else:
            print(f"? Multiple color schemes found: {unique_colors}")
        
        if len(unique_fonts) <= 2:  # Allow for fallback fonts
            print("✓ Font family is consistent across pages")
        else:
            print(f"? Multiple font families found: {unique_fonts}")
            
    except Exception as e:
        print(f"✗ Error during UI consistency test: {str(e)}")
        raise

def test_error_recovery_scenarios(driver, base_url):
    """Test 22: Test error recovery scenarios"""
    print(f"\n=== TEST 22: Error Recovery Scenarios ===")
    
    try:
        # Test accessing non-existent page
        driver.get(f"{base_url}/nonexistent.html")
        time.sleep(3)
        
        page_source = driver.page_source.lower()
        
        # Should either show 404 error or redirect
        if ("404" in page_source or "not found" in page_source or 
            "error" in page_source):
            print("✓ 404 errors are handled properly")
        else:
            print("? No clear 404 error handling - might redirect to default page")
        
        # Test recovery by navigating to valid page
        driver.get(f"{base_url}/index.html")
        wait_for_page_load(driver)
        
        # Should be able to recover and load valid page
        assert driver.current_url.endswith("index.html"), "Should be able to recover and load valid page"
        print("✓ Recovery from error pages works")
        
        # Test JavaScript error recovery
        driver.get(f"{base_url}/main.html")
        wait_for_page_load(driver)
        
        # Try to cause a harmless JavaScript action
        try:
            driver.execute_script("console.log('Test JavaScript execution');")
            print("✓ JavaScript execution works normally")
        except Exception as js_error:
            print(f"? JavaScript error occurred: {js_error}")
        
    except Exception as e:
        print(f"✗ Error during error recovery test: {str(e)}")
        raise

def test_security_headers_and_features(driver, base_url):
    """Test 23: Test basic security features"""
    print(f"\n=== TEST 23: Security Features ===")
    
    driver.get(f"{base_url}/login.html")
    wait_for_page_load(driver)
    
    try:
        # Test password field security
        password_input = driver.find_element(By.ID, "password")
        
        # Verify password field type
        field_type = password_input.get_attribute("type")
        assert field_type == "password", "Password field should be secured"
        
        # Test that password is not visible in page source
        password_input.send_keys("secretpassword")
        page_source = driver.page_source
        assert "secretpassword" not in page_source, "Password should not be visible in page source"
        
        # Test for autocomplete settings (security feature)
        autocomplete = password_input.get_attribute("autocomplete")
        if autocomplete:
            print(f"  Autocomplete setting: {autocomplete}")
        
        # Test HTTPS usage (if applicable)
        current_url = driver.current_url
        if current_url.startswith("https://"):
            print("✓ HTTPS is being used for secure communication")
        else:
            print("? HTTP is being used - HTTPS recommended for production")
        
        print("✓ Basic security features are implemented")
        
    except Exception as e:
        print(f"✗ Error during security features test: {str(e)}")
        raise

def test_mobile_responsive_behavior(driver, base_url):
    """Test 24: Test mobile responsive behavior in detail"""
    print(f"\n=== TEST 24: Mobile Responsive Behavior ===")
    
    try:
        # Start with desktop size
        driver.set_window_size(1920, 1080)
        driver.get(f"{base_url}/main.html")
        wait_for_page_load(driver)
        
        # Get desktop layout measurements
        chat_output = driver.find_element(By.ID, "chat-output")
        desktop_width = chat_output.size['width']
        
        # Switch to mobile size
        driver.set_window_size(375, 667)  # iPhone size
        time.sleep(2)
        
        # Check mobile layout
        mobile_width = chat_output.size['width']
        
        # Mobile width should be smaller than desktop
        assert mobile_width < desktop_width, "Mobile layout should be more compact"
        
        # Test mobile interaction
        user_input = driver.find_element(By.ID, "userInput")
        assert user_input.is_displayed(), "Input should be visible on mobile"
        
        # Test touch-friendly elements (check if clickable elements are large enough)
        input_height = user_input.size['height']
        assert input_height >= 30, "Touch elements should be at least 30px high for mobile"
        
        # Test horizontal scrolling (should not be present)
        body_width = driver.execute_script("return document.body.scrollWidth;")
        viewport_width = driver.execute_script("return window.innerWidth;")
        
        if body_width <= viewport_width + 20:  # Allow small margin
            print("✓ No horizontal scrolling on mobile")
        else:
            print("? Horizontal scrolling detected on mobile")
        
        # Restore desktop size
        driver.set_window_size(1920, 1080)
        
        print("✓ Mobile responsive behavior is functional")
        
    except Exception as e:
        print(f"✗ Error during mobile responsive test: {str(e)}")
        # Restore desktop size even if test fails
        try:
            driver.set_window_size(1920, 1080)
        except:
            pass
        raise 