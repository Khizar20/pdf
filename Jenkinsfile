pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_PROJECT = 'pdf-chatbot-cicd'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub
                checkout scm
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