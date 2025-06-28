#!/usr/bin/env python3
"""
Docker-specific test runner for PDF Chatbot Selenium tests
Optimized for Jenkins and AWS EC2 execution
"""

import pytest
import os
import sys
import subprocess
import time
from datetime import datetime

def check_application_health():
    """Check if the application is accessible before running tests"""
    base_url = os.getenv("TEST_BASE_URL", "http://host.docker.internal:80")
    
    print(f"🔍 Checking application health at: {base_url}")
    
    max_retries = 30
    for i in range(max_retries):
        try:
            # Use curl to check if application is responsive
            result = subprocess.run(['curl', '-f', '-s', base_url], 
                                  capture_output=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ Application is healthy and accessible at {base_url}")
                return True
        except subprocess.TimeoutExpired:
            print(f"⏱️ Timeout checking application (attempt {i+1}/{max_retries})")
        except Exception as e:
            print(f"⚠️ Error checking application: {e}")
        
        if i < max_retries - 1:
            print(f"🔄 Retrying in 5 seconds... (attempt {i+1}/{max_retries})")
            time.sleep(5)
    
    print(f"❌ Application not accessible after {max_retries} attempts")
    return False

def setup_environment():
    """Setup test environment for Docker execution"""
    print("=== Setting up Docker test environment ===")
    
    # Set environment variables
    os.environ['DISPLAY'] = ':99'
    
    # Verify ChromeDriver
    try:
        result = subprocess.run(['which', 'chromedriver'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ChromeDriver found at: {result.stdout.strip()}")
        else:
            print("❌ ChromeDriver not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking ChromeDriver: {e}")
        return False
    
    # Verify Chrome
    try:
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Chrome version: {result.stdout.strip()}")
        else:
            print("❌ Chrome not found")
            return False
    except Exception as e:
        print(f"❌ Error checking Chrome: {e}")
        return False
    
    return True

def run_tests():
    """Run the Selenium test suite"""
    print("=== Running 10 Comprehensive Selenium Tests ===")
    
    # Test configuration
    base_url = os.getenv("TEST_BASE_URL", "http://host.docker.internal:80")
    print(f"🎯 Target Application: {base_url}")
    
    # Pytest arguments optimized for Docker/CI environment
    pytest_args = [
        "test_simplified.py",
        "-v",                                    # Verbose output
        "--tb=short",                           # Short traceback format
        "--html=test_reports/test_report.html", # HTML report
        "--self-contained-html",                # Embed CSS/JS in HTML
        "--capture=no",                         # Show print statements
        "--maxfail=3",                          # Stop after 3 failures
        "-x"                                    # Stop on first failure in CI
    ]
    
    print(f"📋 Running pytest with args: {pytest_args}")
    
    # Run tests
    start_time = time.time()
    exit_code = pytest.main(pytest_args)
    end_time = time.time()
    
    duration = end_time - start_time
    print(f"⏱️ Test execution completed in {duration:.2f} seconds")
    
    return exit_code

def generate_summary_report():
    """Generate a summary report of test execution"""
    print("\n" + "="*60)
    print("📊 SELENIUM TEST EXECUTION SUMMARY")
    print("="*60)
    print("✅ Test Framework: Selenium WebDriver with Python/pytest")
    print("✅ Browser: Headless Chrome (containerized)")
    print("✅ Environment: Docker container")
    print("✅ Test Count: 10 comprehensive test cases")
    print("✅ Application: PDF Chatbot")
    print(f"✅ Target URL: {os.getenv('TEST_BASE_URL', 'http://host.docker.internal:80')}")
    print("")
    print("🧪 Test Categories:")
    print("   • Home Page Loading")
    print("   • User Registration/Signup")
    print("   • User Authentication/Login")
    print("   • PDF Upload Interface")
    print("   • Chat Interface Functionality")
    print("   • Responsive Design")
    print("   • Page Navigation")
    print("   • Accessibility Features")
    print("   • Form Validation")
    print("   • UI/UX Components")
    print("="*60)

def main():
    """Main execution function"""
    print("🐳 PDF Chatbot Docker Test Runner")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed!")
        sys.exit(1)
    
    # Check application health
    if not check_application_health():
        print("❌ Application health check failed!")
        sys.exit(1)
    
    # Wait a bit more for application to stabilize
    print("⏳ Waiting for application to stabilize...")
    time.sleep(10)
    
    # Run tests
    exit_code = run_tests()
    
    # Generate summary
    generate_summary_report()
    
    # Final status
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exit_code == 0:
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print(f"❌ TESTS FAILED (exit code: {exit_code})")
        print("📋 Check test_reports/test_report.html for detailed results")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 