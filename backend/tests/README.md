# PDF Chatbot - Selenium Test Suite

This directory contains comprehensive automated test cases using Selenium WebDriver for testing the PDF Chatbot web application.

## Test Coverage

The test suite includes **24 comprehensive test cases** covering:

### Authentication Tests (`test_auth.py`) - 8 Tests
1. **Signup Page Load** - Verify signup page loads with all required elements
2. **Successful Signup** - Test user registration with unique credentials
3. **Duplicate Username Signup** - Test duplicate username handling
4. **Login Page Load** - Verify login page loads with all required elements
5. **Invalid Credentials Login** - Test login with invalid credentials
6. **Empty Fields Login** - Test form validation for empty fields
7. **Navigation Between Auth Pages** - Test navigation links between login/signup
8. **Password Field Security** - Verify password field is properly masked

### PDF Functionality Tests (`test_pdf.py`) - 8 Tests
9. **Main Page Load** - Verify main chat page loads with all elements
10. **PDF Upload Interface** - Test PDF upload field functionality
11. **Chat Interface Elements** - Test chat interface components
12. **Responsive Design Elements** - Test responsive behavior across screen sizes
13. **Page Load Performance** - Test page load timing and performance
14. **JavaScript Functionality** - Test JavaScript features and interactions
15. **Accessibility Features** - Test basic accessibility compliance
16. **Error Handling Display** - Test error handling and user feedback

### Integration Tests (`test_integration.py`) - 8 Tests
17. **Home Page Navigation** - Test home page and navigation flows
18. **Cross-Browser Compatibility** - Test browser compatibility features
19. **Form Validation Behavior** - Test comprehensive form validation
20. **Keyboard Navigation** - Test keyboard accessibility and navigation
21. **UI Consistency Across Pages** - Test design consistency
22. **Error Recovery Scenarios** - Test error handling and recovery
23. **Security Features** - Test basic security implementations
24. **Mobile Responsive Behavior** - Test detailed mobile responsiveness

## Prerequisites

### Required Software
- **Python 3.8+**
- **Google Chrome Browser**
- **ChromeDriver** (compatible with your Chrome version)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:
- `selenium==4.18.1`
- `pytest==8.0.2`
- `webdriver-manager==4.0.1`
- `pytest-html==4.1.1`

### ChromeDriver Setup
1. Download ChromeDriver from: https://chromedriver.chromium.org/
2. Place the executable in the `backend/tests/` directory
3. For Windows: Name it `chromedriver.exe`
4. For Linux/Mac: Name it `chromedriver` and make it executable

## Test Configuration

### Base URL Configuration
The tests use a configurable base URL:
- **Default**: `http://localhost:80`
- **Override**: Set environment variable `TEST_BASE_URL`

```bash
# Example for different environments
export TEST_BASE_URL="https://your-domain.com"
export TEST_BASE_URL="http://localhost:3000"
export TEST_BASE_URL="https://18.217.174.138"  # Your AWS EC2 instance
```

### Browser Configuration
Tests are configured for **headless Chrome** with:
- Headless mode for CI/CD compatibility
- SSL certificate bypass for HTTPS testing
- Mobile responsive testing capabilities
- Performance optimization settings

## Running Tests

### Run All Tests
```bash
cd backend/tests
python run_tests.py
```

### Run Specific Test Suite
```bash
python run_tests.py test_auth.py        # Authentication tests only
python run_tests.py test_pdf.py         # PDF functionality tests only
python run_tests.py test_integration.py # Integration tests only
```

### Run with pytest directly
```bash
pytest -v --html=test_report.html --self-contained-html
```

### Run Single Test Function
```bash
pytest -v test_auth.py::test_signup_page_load
```

## Test Output

### Console Output
Tests provide detailed console output with:
- ✓ Success indicators for passed tests
- ✗ Error indicators for failed tests
- ? Warning indicators for unclear results
- Detailed debugging information

### HTML Report
An HTML test report is generated: `test_report.html`
- Comprehensive test results
- Screenshots on failures (if configured)
- Execution timing information
- Pass/fail statistics

## Jenkins Integration

The test suite is designed for Jenkins CI/CD pipeline integration:

### Jenkinsfile Configuration
```groovy
stage('Run Selenium Tests') {
    steps {
        script {
            sh '''
                cd backend/tests
                python -m pip install -r requirements.txt
                export TEST_BASE_URL="http://localhost:80"
                python run_tests.py
            '''
        }
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'backend/tests',
                reportFiles: 'test_report.html',
                reportName: 'Selenium Test Report'
            ])
        }
    }
}
```

### AWS EC2 Deployment Testing
For testing on AWS EC2:
```bash
export TEST_BASE_URL="https://your-ec2-public-ip"
python run_tests.py
```

## Troubleshooting

### Common Issues

#### ChromeDriver Not Found
```
Error: ChromeDriver not found at /path/to/chromedriver
```
**Solution**: 
1. Download correct ChromeDriver version
2. Place in `backend/tests/` directory
3. Ensure executable permissions (Linux/Mac)

#### SSL Certificate Errors
```
Error: SSL certificate verification failed
```
**Solution**: Tests include SSL bypass flags, but for custom certificates:
```python
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')
```

#### Element Not Found Errors
```
NoSuchElementException: Unable to locate element
```
**Solution**: 
1. Check element selectors match HTML structure
2. Increase wait times for slow-loading pages
3. Verify page is fully loaded before interaction

#### Timeout Errors
```
TimeoutException: Element not found within timeout
```
**Solution**:
1. Increase timeout values in `conftest.py`
2. Check network connectivity to application
3. Verify application is running and accessible

### Debugging Tips

#### Enable Debug Mode
```python
# In conftest.py, add:
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')
```

#### View Page Source
```python
# Add to test for debugging:
print("Page source:", driver.page_source[:500])
print("Current URL:", driver.current_url)
```

#### Take Screenshots
```python
# Add to test for debugging:
driver.save_screenshot("debug_screenshot.png")
```

## Test Environment Setup

### Local Development
1. Start your application locally
2. Set `TEST_BASE_URL=http://localhost:PORT`
3. Run tests

### Docker Environment
1. Build and start containers
2. Set `TEST_BASE_URL=http://localhost:80`
3. Run tests from host machine

### Production Testing
1. Deploy application to server
2. Set `TEST_BASE_URL=https://your-domain.com`
3. Run tests remotely

## Best Practices

### Test Design
- Each test is independent and can run in isolation
- Tests use unique data to avoid conflicts
- Proper cleanup and error handling
- Comprehensive assertions and validations

### Maintenance
- Update selectors when UI changes
- Keep ChromeDriver version compatible with Chrome
- Regular test execution to catch regressions
- Monitor test execution times

### Reporting
- HTML reports for detailed analysis
- Console output for quick feedback
- Integration with CI/CD pipelines
- Test metrics and trends tracking

## Contributing

When adding new tests:
1. Follow existing naming conventions
2. Include comprehensive documentation
3. Add proper error handling
4. Update this README with new test descriptions
5. Ensure tests work in headless mode for CI/CD

## Support

For issues with the test suite:
1. Check this README for common solutions
2. Review console output for specific errors
3. Verify application is running and accessible
4. Check ChromeDriver compatibility
5. Ensure all dependencies are installed 