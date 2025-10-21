pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'shivani1128/music-playlist-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker Image...'
                bat "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                bat "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }
        
        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }
        
        stage('Push Docker Image to Dockerhub') {
            steps {
                echo 'Pushing Docker images to Docker Hub...'
                bat "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                bat "docker push ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Deploy/Update Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                bat "kubectl apply -f deployment.yaml"
                bat "kubectl apply -f service.yaml"
            }
        }
        
        stage('Restart Deployment') {
            steps {
                echo 'Restarting Kubernetes deployment...'
                bat "kubectl rollout restart deployment/music-playlist-manager"
                bat "kubectl rollout status deployment/music-playlist-manager"
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                bat "kubectl get pods -l app=music-playlist-manager"
                bat "kubectl get svc music-playlist-manager-service"
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
            echo "Application deployed with image: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo 'Pipeline failed!'
            echo 'Please check the logs above for errors.'
        }
        always {
            echo 'Cleaning up...'
            bat 'docker logout'
        }
    }
}
