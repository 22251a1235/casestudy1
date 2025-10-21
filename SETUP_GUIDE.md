# 🚀 Complete Setup Guide - Music Playlist Manager CI/CD Pipeline

This guide will walk you through the complete setup process from scratch.

## 📋 Table of Contents

1. [Prerequisites Installation](#prerequisites-installation)
2. [Docker Setup](#docker-setup)
3. [Kubernetes Setup](#kubernetes-setup)
4. [Jenkins Setup](#jenkins-setup)
5. [Git Repository Setup](#git-repository-setup)
6. [Deployment Steps](#deployment-steps)
7. [Testing the Pipeline](#testing-the-pipeline)

---

## 1. Prerequisites Installation

### Install Docker

**Windows:**
1. Download Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Enable WSL 2 when prompted
4. Restart your computer
5. Verify installation:
   ```cmd
   docker --version
   docker run hello-world
   ```

**Linux:**
```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Verify installation
docker --version
```

### Install Kubernetes (Minikube)

**Windows:**
1. Download Minikube installer from [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)
2. Install kubectl:
   ```powershell
   choco install kubernetes-cli
   # OR download from https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
   ```

**Linux:**
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Install Git

**Windows:**
- Download from [git-scm.com](https://git-scm.com/download/win)

**Linux:**
```bash
sudo apt-get install git
```

### Install Python (for local testing)

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Check "Add to PATH" during installation

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

---

## 2. Docker Setup

### Create Docker Hub Account

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for a free account
3. Verify your email
4. Remember your username (you'll need it later)

### Login to Docker Hub

```bash
docker login
# Enter your Docker Hub username and password
```

### Test Docker Build (Optional)

```bash
# Navigate to project directory
cd casestudy35

# Build the image
docker build -t music-playlist-manager:test .

# Run the container
docker run -d -p 5000:5000 music-playlist-manager:test

# Test in browser
# Open http://localhost:5000

# Stop and remove
docker stop $(docker ps -q --filter ancestor=music-playlist-manager:test)
```

---

## 3. Kubernetes Setup

### Start Minikube

```bash
# Start Minikube cluster
minikube start --driver=docker

# Verify cluster is running
kubectl cluster-info
kubectl get nodes

# Enable metrics (optional)
minikube addons enable metrics-server
```

### Configure kubectl

```bash
# View current context
kubectl config current-context

# Get cluster information
kubectl get all
```

---

## 4. Jenkins Setup

### Option A: Jenkins with Docker (Recommended for Testing)

```bash
# Create a network for Jenkins
docker network create jenkins

# Run Jenkins container
docker run -d ^
  --name jenkins ^
  --restart=on-failure ^
  --network jenkins ^
  -p 8080:8080 -p 50000:50000 ^
  -v jenkins_home:/var/jenkins_home ^
  -v /var/run/docker.sock:/var/run/docker.sock ^
  jenkins/jenkins:lts

# Wait for Jenkins to start (30-60 seconds)

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Option B: Jenkins Installation (Production)

**Windows:**
1. Download Jenkins from [jenkins.io](https://www.jenkins.io/download/)
2. Run the installer
3. Follow setup wizard

**Linux:**
```bash
# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update
sudo apt-get install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Jenkins Initial Configuration

1. **Access Jenkins**: Open `http://localhost:8080`

2. **Unlock Jenkins**: 
   - Paste the initial admin password
   - Click Continue

3. **Install Plugins**:
   - Select "Install suggested plugins"
   - Wait for installation to complete
   - Additionally install:
     * Docker Pipeline
     * Kubernetes CLI Plugin
     * Git Plugin

4. **Create Admin User**:
   - Fill in username, password, email
   - Click "Save and Continue"

5. **Configure Jenkins URL**:
   - Keep default (`http://localhost:8080`)
   - Click "Save and Finish"

### Configure Jenkins Credentials

#### Add Docker Hub Credentials

1. Go to: `Jenkins Dashboard` → `Manage Jenkins` → `Credentials`
2. Click on `(global)` domain
3. Click `Add Credentials`
4. Fill in:
   - Kind: `Username with password`
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password
   - ID: `dockerhub-credentials`
   - Description: `Docker Hub Login`
5. Click `Create`

#### Add Kubeconfig Credentials

```bash
# Get kubeconfig content
kubectl config view --flatten > kubeconfig.txt
```

1. Go to: `Jenkins Dashboard` → `Manage Jenkins` → `Credentials`
2. Click `Add Credentials`
3. Fill in:
   - Kind: `Secret file`
   - File: Upload `kubeconfig.txt`
   - ID: `kubeconfig`
   - Description: `Kubernetes Config`
4. Click `Create`

### Install Docker in Jenkins (if using Docker container)

```bash
# Access Jenkins container
docker exec -it -u root jenkins bash

# Install Docker CLI
apt-get update
apt-get install -y docker.io

# Exit container
exit
```

---

## 5. Git Repository Setup

### Initialize Local Repository

```bash
# Navigate to project directory
cd casestudy35

# Initialize Git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Music Playlist Manager with CI/CD pipeline"
```

### Create Remote Repository

#### Option A: GitHub

1. Go to [github.com](https://github.com)
2. Click `New Repository`
3. Name: `music-playlist-manager-cicd`
4. Keep it Public or Private
5. Don't initialize with README (we already have one)
6. Click `Create Repository`

#### Option B: GitLab

1. Go to [gitlab.com](https://gitlab.com)
2. Click `New Project`
3. Create blank project
4. Follow similar steps

### Push to Remote Repository

```bash
# Add remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/music-playlist-manager-cicd.git

# Push to remote
git branch -M main
git push -u origin main
```

---

## 6. Deployment Steps

### Step 1: Update Configuration Files

1. **Update `deployment.yaml`**:
   ```yaml
   # Change this line:
   image: YOUR_DOCKERHUB_USERNAME/music-playlist-manager:latest
   # To (replace with your username):
   image: yourusername/music-playlist-manager:latest
   ```

2. **Update `Jenkinsfile`**:
   ```groovy
   // Change this line:
   DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/music-playlist-manager'
   // To:
   DOCKER_IMAGE = 'yourusername/music-playlist-manager'
   ```

### Step 2: Create Jenkins Pipeline Job

1. **Create New Item**:
   - Jenkins Dashboard → `New Item`
   - Name: `music-playlist-manager-pipeline`
   - Type: `Pipeline`
   - Click `OK`

2. **Configure General Settings**:
   - Description: `CI/CD Pipeline for Music Playlist Manager`

3. **Configure Build Triggers**:
   - Check: `Poll SCM`
   - Schedule: `H/5 * * * *` (polls every 5 minutes)
   - OR configure webhook for instant triggers

4. **Configure Pipeline**:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: Your Git repository URL
   - Credentials: Add if private repository
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`

5. **Save** the configuration

### Step 3: First Manual Build

1. Click `Build Now`
2. Monitor build progress in `Console Output`
3. Wait for all stages to complete

### Step 4: Verify Deployment

```bash
# Check Kubernetes resources
kubectl get deployments
kubectl get pods
kubectl get services

# Check application is running
kubectl get pods -l app=music-playlist-manager

# Access the application
# For Minikube:
minikube service music-playlist-manager-service

# For local Kubernetes:
# http://localhost:30080
```

---

## 7. Testing the Pipeline

### Test 1: Automatic Build on Code Change

1. **Make a change**:
   ```bash
   # Edit a file, e.g., templates/index.html
   # Change the welcome message
   
   git add .
   git commit -m "Update welcome message"
   git push origin main
   ```

2. **Watch Jenkins**:
   - Jenkins will detect the change within 5 minutes
   - Pipeline will automatically trigger
   - Monitor in Jenkins Dashboard

3. **Verify deployment**:
   ```bash
   kubectl rollout status deployment/music-playlist-manager
   kubectl get pods
   ```

### Test 2: Health Check

```bash
# Get service URL
minikube service music-playlist-manager-service --url

# Test health endpoint
curl http://localhost:30080/health
```

### Test 3: Application Functionality

1. Open browser to application URL
2. Test each page:
   - Home (/)
   - Playlists (/playlists)
   - Create Playlist (/create)
   - Search (/search)
3. Create a playlist
4. Add songs
5. Search for songs

---

## 🐛 Common Issues and Solutions

### Issue 1: Jenkins Can't Build Docker Images

**Solution:**
```bash
# If using Docker Desktop, expose daemon on tcp://localhost:2375
# OR mount Docker socket in Jenkins container
docker run ... -v /var/run/docker.sock:/var/run/docker.sock ...
```

### Issue 2: kubectl Not Working in Jenkins

**Solution:**
- Ensure kubeconfig file is properly uploaded
- Check Jenkins has kubectl installed
- Verify Kubernetes cluster is accessible

### Issue 3: Minikube Not Accessible

**Solution:**
```bash
# Restart Minikube
minikube stop
minikube start

# Check status
minikube status

# Get service URL
minikube service music-playlist-manager-service
```

### Issue 4: Docker Image Not Updating

**Solution:**
```bash
# Force Kubernetes to pull new image
kubectl rollout restart deployment/music-playlist-manager

# Check rollout status
kubectl rollout status deployment/music-playlist-manager
```

### Issue 5: Port Already in Use

**Solution:**
```bash
# Find process using port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux:
lsof -i :5000
kill -9 <PID>
```

---

## 📊 Monitoring Commands

### Jenkins
```bash
# Check Jenkins logs
docker logs jenkins -f
```

### Docker
```bash
# List running containers
docker ps

# Check container logs
docker logs <container-id>

# Check images
docker images
```

### Kubernetes
```bash
# Watch pod status
kubectl get pods -w

# View pod logs
kubectl logs -f <pod-name>

# Describe pod
kubectl describe pod <pod-name>

# Check all resources
kubectl get all
```

---

## ✅ Verification Checklist

- [ ] Docker installed and running
- [ ] Kubernetes cluster running (Minikube)
- [ ] Jenkins installed and accessible
- [ ] Docker Hub account created
- [ ] Git repository created and pushed
- [ ] Jenkins credentials configured
- [ ] Pipeline job created in Jenkins
- [ ] First build completed successfully
- [ ] Application accessible via browser
- [ ] Automatic pipeline trigger working
- [ ] Code changes deploy automatically

---

## 🎯 Next Steps

1. Add database persistence (PostgreSQL)
2. Implement user authentication
3. Add Prometheus monitoring
4. Set up Grafana dashboards
5. Implement automated testing
6. Add Slack/email notifications
7. Implement blue-green deployment
8. Add Helm charts

---

## 📞 Support

If you encounter issues:
1. Check console output in Jenkins
2. Review pod logs in Kubernetes
3. Verify all credentials are correct
4. Ensure all services are running
5. Check firewall/network settings

---

**Congratulations!** 🎉 You now have a fully automated CI/CD pipeline!

