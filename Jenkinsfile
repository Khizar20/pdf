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

        stage('Build Frontend Image') {
            steps {
                echo 'Building frontend Docker image...'
                sh '''
                    echo "Building frontend image..."
                    docker build -t pdf-chatbot-frontend ./frontend
                    echo "Frontend image built successfully"
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo 'Deploying PDF Chatbot application using docker-compose...'
                sh '''
                    echo "Starting deployment with docker-compose from repository..."
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

        stage('Health Check') {
            steps {
                echo 'Performing application health checks...'
                script {
                    retry(3) {
                        sh '''
                            echo "Waiting for services to be fully ready..."
                            sleep 15

                            echo "Checking backend API health..."
                            if curl -f -s http://localhost:8000/docs > /dev/null; then
                                echo "✅ Backend API is responding"
                            else
                                echo "⚠️ Backend API health check failed, retrying..."
                                exit 1
                            fi

                            echo "Checking frontend availability..."
                            if curl -f -s http://localhost:80 > /dev/null; then
                                echo "✅ Frontend is responding"
                            else
                                echo "⚠️ Frontend health check failed, retrying..."
                                exit 1
                            fi

                            echo "🎉 All services are healthy and running!"
                        '''
                    }
                }
            }
        }

        stage('Display Application Info') {
            steps {
                echo 'Displaying application deployment information...'
                sh '''
                    echo "==================================="
                    echo "📋 PDF CHATBOT DEPLOYMENT STATUS"
                    echo "==================================="
                    echo "🌐 Frontend URL: http://localhost:80"
                    echo "📊 Backend API: http://localhost:8000"
                    echo "📚 API Documentation: http://localhost:8000/docs"
                    echo "==================================="

                    echo "Container Status:"
                    docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps

                    echo ""
                    echo "Running Containers:"
                    docker ps --filter "name=${DOCKER_COMPOSE_PROJECT}"
                '''
            }
        }
    }

    post {
        always {
            echo 'Performing cleanup...'
            sh '''
                # Clean up unused images to save space
                docker image prune -f || true
                echo "Cleanup completed"
            '''
            cleanWs()
        }

        success {
            echo '''
            🎉 DEPLOYMENT SUCCESSFUL! 🎉

            ✅ PDF Chatbot application is now running
            🌐 Frontend: http://localhost:80
            📊 Backend API: http://localhost:8000/docs
            🗄️ MongoDB: Running as part of the stack

            📋 To view logs: docker-compose -p pdf-chatbot-cicd logs
            🔄 To restart: docker-compose -p pdf-chatbot-cicd restart
            🛑 To stop: docker-compose -p pdf-chatbot-cicd down
            '''
        }

        failure {
            echo '''
            ❌ DEPLOYMENT FAILED!

            📋 Troubleshooting steps:
            1. Check Jenkins logs above for specific errors
            2. Verify Docker is running on the Jenkins agent
            3. Check if ports 80 and 8000 are available
            4. Verify .env file contains correct values

            🔍 Debug commands:
            - docker-compose -p pdf-chatbot-cicd logs
            - docker-compose -p pdf-chatbot-cicd ps
            - docker ps -a
            '''
            sh '''
                echo "=== FAILURE DEBUG INFORMATION ==="
                echo "Container status:"
                docker-compose -p ${DOCKER_COMPOSE_PROJECT} ps || true

                echo ""
                echo "Container logs:"
                docker-compose -p ${DOCKER_COMPOSE_PROJECT} logs || true

                echo ""
                echo "System status:"
                docker ps -a || true
            '''
        }

        unstable {
            echo '⚠️ Pipeline completed with warnings. Check the logs for details.'
        }
    }
}
