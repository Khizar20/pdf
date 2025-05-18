pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_PROJECT = 'pdf-chatbot-cicd'
        GITHUB_URL = 'https://github.com/Khizar20/chatbot.git'  // Replace with your actual GitHub URL
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                git url: "${GITHUB_URL}", branch: 'master'
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t pdf-chatbot-backend:latest .'
                }
            }
        }
        
        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t pdf-chatbot-frontend:latest .'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                // Run docker-compose with the specified project name
                sh "docker-compose -p ${DOCKER_COMPOSE_PROJECT} -f docker-compose.yml up -d"
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
} 