import pytest
import os
import sys
import subprocess
from datetime import datetime

def setup_environment():
    """Setup test environment and dependencies"""
    print("=== Setting up test environment ===")
    
    # Get the directory containing this script
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the parent directory to Python path
    sys.path.append(os.path.dirname(test_dir))
    
    # Check if chromedriver exists
    if sys.platform == "win32":
        chromedriver_path = os.path.join(test_dir, "chromedriver.exe")
    else:
        chromedriver_path = os.path.join(test_dir, "chromedriver")
    
    if not os.path.exists(chromedriver_path):
        print(f"Warning: ChromeDriver not found at {chromedriver_path}")
        print("Please ensure ChromeDriver is installed and available")
        return False
    
    print(f"✓ ChromeDriver found at: {chromedriver_path}")
    return True

def run_specific_test_suite(test_file=None):
    """Run a specific test suite or all tests"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Base pytest arguments
    pytest_args = [
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=test_report.html",  # HTML report
        "--self-contained-html",  # Embed CSS/JS in HTML
        "--capture=no",  # Show print statements
    ]
    
    if test_file:
        # Run specific test file
        test_path = os.path.join(test_dir, test_file)
        if os.path.exists(test_path):
            pytest_args.append(test_path)
        else:
            print(f"Test file {test_file} not found!")
            return False
    else:
        # Run all test files
        pytest_args.append(test_dir)
    
    print(f"Running tests with arguments: {pytest_args}")
    return pytest.main(pytest_args)

def main():
    """Main test runner function"""
    print("=== PDF Chatbot Selenium Test Suite ===")
    print(f"Test execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Setup environment
    if not setup_environment():
        print("Environment setup failed!")
        return 1
    
    # Check if specific test file is requested
    test_file = None
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        print(f"Running specific test file: {test_file}")
    else:
        print("Running all test files...")
    
    # Run tests
    exit_code = run_specific_test_suite(test_file)
    
    print(f"\nTest execution completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if exit_code == 0:
        print("✓ All tests passed successfully!")
    else:
        print(f"✗ Tests failed with exit code: {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    # Available test files for reference
    available_tests = [
        "test_auth.py",      # Authentication tests (8 tests)
        "test_pdf.py",       # PDF functionality tests (8 tests)
        "test_integration.py" # Integration and UI tests (8 tests)
    ]
    
    print("Available test suites:")
    for i, test in enumerate(available_tests, 1):
        print(f"  {i}. {test}")
    print()
    
    exit_code = main()
    sys.exit(exit_code) 