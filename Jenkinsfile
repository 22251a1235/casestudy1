pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/music-playlist-manager'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig'
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
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    // Run container to test if it starts properly
                    sh """
                        docker run -d --name test-container -p 5001:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}
                        sleep 10
                        curl -f http://localhost:5001/health || exit 1
                        docker stop test-container
                        docker rm test-container
                    """
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
            }
        }
        
        stage('Update Kubernetes Manifests') {
            steps {
                echo 'Updating Kubernetes deployment manifests...'
                script {
                    sh """
                        sed -i 's|image: .*|image: ${DOCKER_IMAGE}:${DOCKER_TAG}|g' deployment.yaml
                    """
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                script {
                    withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl apply -f deployment.yaml
                            kubectl apply -f service.yaml
                            kubectl rollout status deployment/music-playlist-manager
                            kubectl get pods -l app=music-playlist-manager
                            kubectl get svc music-playlist-manager-service
                        """
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                script {
                    withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl wait --for=condition=ready pod -l app=music-playlist-manager --timeout=300s
                            echo 'Deployment verified successfully!'
                        """
                    }
                }
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
        }
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f'
        }
    }
}

