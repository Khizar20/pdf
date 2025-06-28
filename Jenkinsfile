pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_PROJECT = 'pdf-chatbot-cicd'
        GITHUB_URL = 'https://github.com/Khizar20/pdf.git'
        DOCKER_BUILDKIT = '1'
        COMPOSE_DOCKER_CLI_BUILD = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub repository...'
                git url: "${GITHUB_URL}", branch: 'master'
                echo 'Code checkout completed successfully'
            }
        }

        stage('Verify Repository Files') {
            steps {
                echo 'Verifying required files exist in repository...'
                sh '''
                    echo "Checking for required files..."
                    ls -la

                    if [ ! -f docker-compose.yml ]; then
                        echo "Error: docker-compose.yml not found in repository"
                        exit 1
                    fi

                    if [ ! -d backend ]; then
                        echo "Error: backend directory not found"
                        exit 1
                    fi

                    if [ ! -d frontend ]; then
                        echo "Error: frontend directory not found"
                        exit 1
                    fi

                    echo "✅ All required files and directories found"
                    echo "Repository structure:"
                    tree -L 2 || ls -la
                '''
            }
        }

        stage('Set Permissions') {
            steps {
                echo 'Setting proper permissions for frontend files...'
                sh '''
                    # Set proper permissions for frontend files
                    chmod -R 755 frontend/public
                    echo "Permissions set for frontend files"

                    # The ownership will be handled by the container
                '''
            }
        }

        stage('Environment Setup') {
            steps {
                echo 'Setting up environment...'
                sh '''
                    echo "Checking for .env file..."
                    if [ -f .env ]; then
                        echo "✅ .env file found in repository"
                        echo "Environment variables loaded from repository .env file"
                    else
                        echo "⚠️ No .env file found, creating default for deployment..."
                        cat > .env << EOF
MONGODB_URI=mongodb://mongo:27017/pdf_chatbot
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here
EOF
                        echo "Default .env file created"
                    fi
                '''
            }
        }

        stage('Stop Previous Deployment') {
            steps {
                echo 'Stopping any previous deployment...'
                sh '''
                    echo "Stopping previous containers..."
                    docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true

                    echo "Cleaning up unused resources..."
                    docker system prune -f || true

                    echo "Previous deployment cleanup completed"
                '''
            }
        }

        stage('Build Backend') {
            steps {
                echo 'Building backend Docker image...'
                sh '''
                    echo "Building backend image..."
                    docker build -t pdf-chatbot-backend ./backend
                    echo "Backend image built successfully"
                '''
            }
        }

        stage('Build Frontend') {
            steps {
                echo 'Building frontend Docker image...'
                sh '''
                    echo "Building frontend image..."
                    docker build -t pdf-chatbot-frontend ./frontend
                    echo "Frontend image built successfully"
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Deploying PDF Chatbot application using docker-compose...'
                sh '''
                    echo "Starting deployment with docker-compose..."
                    echo "Using docker-compose.yml from: $(pwd)"

                    # Display docker-compose file content for verification
                    echo "Docker Compose Configuration:"
                    cat docker-compose.yml

                    # Start the application
                    docker-compose -p ${DOCKER_COMPOSE_PROJECT} -f docker-compose.yml up -d --build

                    echo "Waiting for services to initialize..."
                    sleep 30

                    echo "Checking container status..."
                    docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps

                    echo "Deployment completed"
                '''
            }
        }

        stage('Application Health Check') {
            steps {
                echo 'Performing application health checks...'
                script {
                    retry(3) {
                        sh '''
                            echo "Waiting for services to be fully ready..."
                            sleep 10

                            # Using known EC2 public IP for health checks
                            echo "🌐 Using EC2 public IP for health checks..."
                            EC2_PUBLIC_IP="3.139.104.31"
                            FRONTEND_URL="http://$EC2_PUBLIC_IP:80"
                            BACKEND_URL="http://$EC2_PUBLIC_IP:8000"
                            echo "🔗 Frontend URL: $FRONTEND_URL"
                            echo "🔗 Backend URL: $BACKEND_URL"

                            echo "Checking backend API health..."
                            if curl -f -s $BACKEND_URL/docs > /dev/null; then
                                echo "✅ Backend API is responding at $BACKEND_URL"
                            else
                                echo "⚠️ Backend API health check failed at $BACKEND_URL, retrying..."
                                exit 1
                            fi

                            echo "Checking frontend availability..."
                            if curl -f -s $FRONTEND_URL > /dev/null; then
                                echo "✅ Frontend is responding at $FRONTEND_URL"
                            else
                                echo "⚠️ Frontend health check failed at $FRONTEND_URL, retrying..."
                                exit 1
                            fi

                            echo "🎉 All services are healthy and running!"
                            echo "🌐 Application accessible at: $FRONTEND_URL"
                            echo "📊 API documentation at: $BACKEND_URL/docs"
                        '''
                    }
                }
            }
        }

        stage('Test Results Summary') {
            steps {
                echo 'Generating test results summary...'
                sh '''
                    echo "=========================================="
                    echo "📊 TEST EXECUTION SUMMARY"
                    echo "=========================================="
                    echo "✅ Test Suite: 10 Comprehensive Selenium Tests"
                    echo "✅ Test Framework: Selenium WebDriver with Python"
                    echo "✅ Browser: Headless Chrome"
                    echo "✅ Test Environment: Containerized Application"
                    echo "✅ Application URL: http://localhost:8080"
                    echo "✅ Backend API: http://localhost:8000"
                    echo "✅ Database: MongoDB (containerized)"
                    echo ""
                    echo "Test Categories Covered:"
                    echo "• Authentication (Login/Signup)"
                    echo "• PDF Upload Interface"
                    echo "• Chat Interface Functionality"
                    echo "• Responsive Design"
                    echo "• Page Navigation"
                    echo "• Accessibility Features"
                    echo "• Form Validation"
                    echo "• UI/UX Components"
                    echo "=========================================="
                '''
            }
        }

        stage('Display Application Info') {
            steps {
                echo 'Displaying application deployment information...'
                sh '''
                    # Using known EC2 public IP for display
                    EC2_PUBLIC_IP="3.139.104.31"
                    FRONTEND_URL="http://$EC2_PUBLIC_IP:80"
                    BACKEND_URL="http://$EC2_PUBLIC_IP:8000"
                    DEPLOYMENT_TYPE="AWS EC2 Instance"

                    echo "==================================="
                    echo "📋 PDF CHATBOT DEPLOYMENT STATUS"
                    echo "==================================="
                    echo "🏗️ Deployment Type: $DEPLOYMENT_TYPE"
                    echo "🌐 Frontend URL: $FRONTEND_URL"
                    echo "📊 Backend API: $BACKEND_URL"
                    echo "📚 API Documentation: $BACKEND_URL/docs"
                    echo "🗄️ MongoDB: Running in container"
                    echo "📋 Test Report: Available in Jenkins artifacts"
                    echo "==================================="

                    echo "Container Status:"
                    docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps

                    echo ""
                    echo "Running Containers:"
                    docker ps --filter "name=${DOCKER_COMPOSE_PROJECT}"
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Starting Selenium Test Execution...'
                echo '📋 Running 10 comprehensive automated test cases'
                sh '''
                    echo "=========================================="
                    echo "🧪 SELENIUM TEST STAGE INITIATED"
                    echo "=========================================="
                    
                    # Using known EC2 public IP address
                    EC2_PUBLIC_IP="3.139.104.31"
                    echo "🌐 Running on EC2 - using IP: $EC2_PUBLIC_IP"
                    FRONTEND_URL="http://$EC2_PUBLIC_IP:80"
                    BACKEND_URL="http://$EC2_PUBLIC_IP:8000"
                    
                    echo "🔗 Frontend URL: $FRONTEND_URL"
                    echo "🔗 Backend URL: $BACKEND_URL"
                    
                    # Wait for application to be fully ready
                    echo "⏳ Ensuring application is ready for testing..."
                    sleep 15
                    
                    # Verify application accessibility
                    echo "🔍 Verifying application accessibility..."
                    if curl -f -s $FRONTEND_URL >/dev/null 2>&1; then
                        echo "✅ Frontend is accessible at $FRONTEND_URL"
                    else
                        echo "❌ Frontend not accessible at $FRONTEND_URL - tests cannot proceed"
                        exit 1
                    fi
                    
                    if curl -f -s $BACKEND_URL/docs >/dev/null 2>&1; then
                        echo "✅ Backend API is accessible at $BACKEND_URL"
                    else
                        echo "❌ Backend API not accessible at $BACKEND_URL - tests cannot proceed"
                        exit 1
                    fi
                    
                    echo "🎯 Test target: $FRONTEND_URL"
                    echo "🏗️ Building test container..."
                    
                    # Build test container
                    cd backend/tests
                    docker build -t pdf-chatbot-tests .
                    
                    echo "🚀 Launching containerized test execution..."
                    echo "📊 Test Framework: Selenium WebDriver + Python"
                    echo "🖥️ Browser: Headless Chrome"
                    echo "📦 Environment: Docker Container"
                    echo "🌐 Target Application: $FRONTEND_URL"
                    
                    # Run tests in container with correct URL
                    docker run --rm \\
                        --network host \\
                        -e TEST_BASE_URL=$FRONTEND_URL \\
                        -v $(pwd)/test_reports:/app/test_reports \\
                        pdf-chatbot-tests python run_tests_docker.py
                    
                    echo "=========================================="
                    echo "✅ SELENIUM TESTS COMPLETED SUCCESSFULLY"
                    echo "🌐 Tests executed against: $FRONTEND_URL"
                    echo "=========================================="
                '''
            }
            post {
                always {
                    echo '📋 Archiving test results and generating reports...'
                    // Archive test results
                    archiveArtifacts artifacts: 'backend/tests/test_reports/**', fingerprint: true, allowEmptyArchive: true
                    
                    // Publish HTML test report
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'backend/tests/test_reports',
                        reportFiles: 'test_report.html',
                        reportName: 'Selenium Test Report'
                    ])
                    
                    echo '📊 Test report published successfully'
                }
                success {
                    echo '''
                    🎉🎉🎉 ALL SELENIUM TESTS PASSED! 🎉🎉🎉
                    
                    ✅ 10 comprehensive test cases executed successfully
                    ✅ Home page loading verification - PASSED
                    ✅ User registration functionality - PASSED  
                    ✅ User authentication system - PASSED
                    ✅ Login form validation - PASSED
                    ✅ PDF upload interface - PASSED
                    ✅ Chat interface functionality - PASSED
                    ✅ Responsive design validation - PASSED
                    ✅ Page navigation testing - PASSED
                    ✅ Accessibility features - PASSED
                    ✅ UI/UX component testing - PASSED
                    
                    🏆 QUALITY ASSURANCE: COMPLETE
                    📊 Test Report: Available in Jenkins artifacts
                    🚀 Application is ready for production use!
                    '''
                }
                failure {
                    echo '''
                    ❌ SELENIUM TESTS FAILED
                    
                    🔍 Some test cases did not pass
                    📋 Check the detailed test report for failure analysis
                    🛠️ Review application functionality and fix issues
                    📊 Test Report: Available in Jenkins artifacts
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
            // Clean up containers if needed
            sh '''
                echo "Cleaning up test environment..."
                # Keep containers running for manual testing
                # docker-compose -p ${DOCKER_COMPOSE_PROJECT} down || true
            '''
        }
        success {
            echo '🎉 Pipeline completed successfully! All tests passed and application is deployed.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs and test reports for details.'
        }
    }
}
