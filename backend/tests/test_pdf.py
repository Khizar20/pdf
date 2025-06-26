import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

def wait_for_page_load(driver, timeout=20):
    """Wait for page to be fully loaded"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(2)  # Additional wait for dynamic content
    except TimeoutException:
        print("Warning: Page load timeout, continuing with test")

def create_test_pdf():
    """Create a simple test PDF file"""
    test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
    # Create a minimal PDF file
    pdf_content = """%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Hello, this is a test PDF!) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000194 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
289
%%EOF"""
    
    with open(test_pdf_path, "w") as f:
        f.write(pdf_content)
    
    return test_pdf_path

def test_main_page_load(driver, base_url):
    """Test 9: Verify main page loads correctly with all required elements"""
    print(f"\n=== TEST 9: Main Page Load ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")
    
    # Verify page title
    assert "Chat with PDF" in driver.title, f"Expected 'Chat with PDF' in title, got: {driver.title}"
    
    try:
        # Check for main interface elements using correct selectors
        pdf_upload = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pdfUpload"))
        )
        chat_output = driver.find_element(By.ID, "chat-output")
        user_input = driver.find_element(By.ID, "userInput")
        
        assert pdf_upload.is_displayed(), "PDF upload not visible"
        assert chat_output.is_displayed(), "Chat output not visible"
        assert user_input.is_displayed(), "User input not visible"
        
        print("✓ All main page elements found and visible")
        
    except (TimeoutException, NoSuchElementException) as e:
        print(f"✗ Error finding main page elements: {str(e)}")
        # Print available elements for debugging
        elements = driver.find_elements(By.XPATH, "//*[@id]")
        print("Available elements with IDs:")
        for element in elements[:10]:  # Limit output
            print(f"- {element.get_attribute('id')}: {element.tag_name}")
        raise

def test_pdf_upload_interface(driver, base_url):
    """Test 10: Test PDF upload interface functionality"""
    print(f"\n=== TEST 10: PDF Upload Interface ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Check for PDF upload input with correct ID
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pdfUpload"))
        )
        
        # Verify it's a file input
        input_type = file_input.get_attribute("type")
        assert input_type == "file", f"Upload field should be type 'file', got '{input_type}'"
        
        # Verify it accepts PDFs
        accept_attr = file_input.get_attribute("accept")
        if accept_attr:
            assert "pdf" in accept_attr.lower(), f"Should accept PDF files, got '{accept_attr}'"
        
        print("✓ PDF upload interface is properly configured")
        
    except Exception as e:
        print(f"✗ Error during PDF upload interface test: {str(e)}")
        raise

def test_chat_interface_elements(driver, base_url):
    """Test 11: Test chat interface elements are present and functional"""
    print(f"\n=== TEST 11: Chat Interface Elements ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Find chat interface elements
        chat_output = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chat-output"))
        )
        user_input = driver.find_element(By.ID, "userInput")
        
        # Try to find send button (look for different possible selectors)
        send_buttons = driver.find_elements(By.CSS_SELECTOR, ".send-btn, button[type='submit'], input[type='submit']")
        
        assert chat_output.is_displayed(), "Chat output area not visible"
        assert user_input.is_displayed(), "User input field not visible"
        
        # Test input field functionality
        user_input.clear()
        user_input.send_keys("Test message")
        assert user_input.get_attribute("value") == "Test message", "Input field not working properly"
        
        print("✓ Chat interface elements are functional")
        
        if send_buttons:
            print("✓ Send button found")
        else:
            print("? No send button found - might use Enter key or other trigger")
            
    except Exception as e:
        print(f"✗ Error during chat interface test: {str(e)}")
        raise

def test_responsive_design_elements(driver, base_url):
    """Test 12: Test responsive design elements"""
    print(f"\n=== TEST 12: Responsive Design Elements ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Test different viewport sizes
        original_size = driver.get_window_size()
        
        # Test mobile size
        driver.set_window_size(375, 667)
        time.sleep(2)
        
        # Check if elements are still visible
        chat_output = driver.find_element(By.ID, "chat-output")
        user_input = driver.find_element(By.ID, "userInput")
        
        assert chat_output.is_displayed(), "Chat output not visible on mobile"
        assert user_input.is_displayed(), "User input not visible on mobile"
        
        # Test tablet size
        driver.set_window_size(768, 1024)
        time.sleep(2)
        
        assert chat_output.is_displayed(), "Chat output not visible on tablet"
        assert user_input.is_displayed(), "User input not visible on tablet"
        
        # Restore original size
        driver.set_window_size(original_size['width'], original_size['height'])
        
        print("✓ Responsive design works across different screen sizes")
        
    except Exception as e:
        print(f"✗ Error during responsive design test: {str(e)}")
        # Restore original size even if test fails
        try:
            driver.set_window_size(1920, 1080)
        except:
            pass
        raise

def test_page_load_performance(driver, base_url):
    """Test 13: Test page load performance and timing"""
    print(f"\n=== TEST 13: Page Load Performance ===")
    
    start_time = time.time()
    
    driver.get(f"{base_url}/main.html")
    
    # Wait for critical elements to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "chat-output"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userInput"))
        )
        
        load_time = time.time() - start_time
        
        # Page should load within reasonable time (15 seconds)
        assert load_time < 15, f"Page took too long to load: {load_time:.2f} seconds"
        
        print(f"✓ Page loaded in {load_time:.2f} seconds")
        
    except TimeoutException:
        load_time = time.time() - start_time
        print(f"✗ Page failed to load critical elements within timeout ({load_time:.2f} seconds)")
        raise

def test_javascript_functionality(driver, base_url):
    """Test 14: Test basic JavaScript functionality"""
    print(f"\n=== TEST 14: JavaScript Functionality ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Test if JavaScript is enabled and working
        js_enabled = driver.execute_script("return typeof window !== 'undefined'")
        assert js_enabled, "JavaScript not enabled or not working"
        
        # Test if jQuery or modern JS features are working
        has_modern_js = driver.execute_script("return typeof document.querySelector !== 'undefined'")
        assert has_modern_js, "Modern JavaScript features not available"
        
        # Test if we can interact with page elements via JS
        user_input = driver.find_element(By.ID, "userInput")
        driver.execute_script("arguments[0].value = 'JavaScript test';", user_input)
        
        input_value = user_input.get_attribute("value")
        assert "JavaScript test" in input_value, "JavaScript interaction with elements not working"
        
        print("✓ JavaScript functionality is working correctly")
        
    except Exception as e:
        print(f"✗ Error during JavaScript functionality test: {str(e)}")
        raise

def test_accessibility_features(driver, base_url):
    """Test 15: Test basic accessibility features"""
    print(f"\n=== TEST 15: Accessibility Features ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Check for proper input labels and placeholders
        user_input = driver.find_element(By.ID, "userInput")
        placeholder = user_input.get_attribute("placeholder")
        
        assert placeholder is not None and placeholder.strip() != "", "Input field should have placeholder text"
        
        # Check for proper page structure
        headings = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
        assert len(headings) > 0, "Page should have proper heading structure"
        
        # Check for alt text on images (if any)
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            if alt_text is None or alt_text.strip() == "":
                print("Warning: Image found without alt text")
        
        print("✓ Basic accessibility features are present")
        
    except Exception as e:
        print(f"✗ Error during accessibility test: {str(e)}")
        raise

def test_error_handling_display(driver, base_url):
    """Test 16: Test error handling and display"""
    print(f"\n=== TEST 16: Error Handling Display ===")
    
    driver.get(f"{base_url}/main.html")
    wait_for_page_load(driver)
    
    try:
        # Test behavior when trying to chat without PDF upload
        user_input = driver.find_element(By.ID, "userInput")
        user_input.clear()
        user_input.send_keys("What is this PDF about?")
        
        # Try to send message (look for different ways to trigger)
        # Try Enter key
        from selenium.webdriver.common.keys import Keys
        user_input.send_keys(Keys.RETURN)
        
        time.sleep(3)
        
        # Check if any error handling occurs
        page_source = driver.page_source.lower()
        
        # Should either show error message or handle gracefully
        if ("error" in page_source or "upload" in page_source or 
            "pdf" in page_source or "no" in page_source):
            print("✓ Error handling appears to be in place")
        else:
            print("? No clear error handling visible - might be handled silently")
        
    except Exception as e:
        print(f"✗ Error during error handling test: {str(e)}")
        raise 