# 🎵 Music Playlist Manager - CI/CD Pipeline Project

A fully automated CI/CD pipeline for deploying a Python Flask Music Playlist Manager application using Docker, Kubernetes, and Jenkins.

## 📋 Project Overview

This project demonstrates a complete DevOps workflow with:
- **Application**: Python Flask web application for managing music playlists
- **Containerization**: Docker for packaging the application
- **Orchestration**: Kubernetes for deployment and scaling
- **CI/CD**: Jenkins for automated build, test, and deployment
- **Version Control**: Git for source code management

## ✨ Application Features

The Music Playlist Manager allows users to:
- 🏠 **Home Dashboard**: View statistics about playlists and songs
- 📋 **View Playlists**: Browse all created playlists with details
- ➕ **Create Playlists**: Add new playlists with name, genre, and description
- 🎵 **Manage Songs**: Add songs to playlists with title, artist, and duration
- 🔍 **Search**: Search across playlists, songs, and artists
- 🗑️ **Delete**: Remove unwanted playlists

## 🚀 Quick Start Guide

### Prerequisites

- Docker installed
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- Jenkins server configured
- Git installed
- Docker Hub account

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd casestudy35
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open browser: `http://localhost:5000`

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t music-playlist-manager:latest .
```

### Run Docker Container

```bash
docker run -d -p 5000:5000 --name playlist-manager music-playlist-manager:latest
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag music-playlist-manager:latest YOUR_DOCKERHUB_USERNAME/music-playlist-manager:latest

# Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/music-playlist-manager:latest
```

## ☸️ Kubernetes Deployment

### Update Kubernetes Manifests

Before deploying, update `deployment.yaml`:
- Replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username

### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Apply service
kubectl apply -f service.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

### Access the Application

```bash
# Get service details
kubectl get svc music-playlist-manager-service

# Access via NodePort (default: 30080)
# Local: http://localhost:30080
# Minikube: minikube service music-playlist-manager-service
```

## 🔧 Jenkins CI/CD Pipeline

### Jenkins Prerequisites

1. **Install required plugins**:
   - Docker Pipeline
   - Kubernetes CLI
   - Git
   - Pipeline

2. **Configure credentials**:
   - Docker Hub credentials (ID: `dockerhub-credentials`)
   - Kubeconfig file (ID: `kubeconfig`)

### Pipeline Setup

1. **Create new Pipeline job in Jenkins**

2. **Configure SCM**:
   - Repository URL: Your Git repository
   - Branch: `main` or `master`

3. **Build Triggers**:
   - Enable "GitHub hook trigger for GITScm polling" or
   - Enable "Poll SCM" with schedule: `H/5 * * * *`

4. **Pipeline Script**:
   - Select "Pipeline script from SCM"
   - SCM: Git
   - Script Path: `Jenkinsfile`

### Update Jenkinsfile

Replace `YOUR_DOCKERHUB_USERNAME` in `Jenkinsfile` with your Docker Hub username.

### Pipeline Stages

1. **Checkout**: Pull latest code from repository
2. **Build**: Create Docker image
3. **Test**: Run health check tests
4. **Push**: Upload image to Docker Hub
5. **Update Manifests**: Update Kubernetes configurations
6. **Deploy**: Apply changes to Kubernetes cluster
7. **Verify**: Confirm deployment success

## 📁 Project Structure

```
casestudy35/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── deployment.yaml        # Kubernetes deployment manifest
├── service.yaml          # Kubernetes service manifest
├── Jenkinsfile           # Jenkins pipeline configuration
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    ├── playlists.html
    ├── create.html
    ├── view_playlist.html
    └── search.html
```

## 🔄 CI/CD Workflow

1. Developer pushes code to Git repository
2. Jenkins detects the change (webhook or polling)
3. Jenkins pipeline automatically:
   - Pulls latest code
   - Builds Docker image
   - Runs tests
   - Pushes image to Docker Hub
   - Updates Kubernetes manifests
   - Deploys to Kubernetes cluster
4. Application is updated with zero downtime

## 🧪 Testing the Pipeline

1. **Make a change to the application**:
   ```bash
   # Edit any file, e.g., templates/index.html
   git add .
   git commit -m "Update home page design"
   git push origin main
   ```

2. **Monitor Jenkins**:
   - Watch the pipeline execute automatically
   - Check console output for each stage

3. **Verify Deployment**:
   ```bash
   kubectl get pods
   kubectl rollout status deployment/music-playlist-manager
   ```

4. **Access Updated Application**:
   - Visit the application URL
   - Verify changes are live

## 🛠️ Troubleshooting

### Docker Issues

```bash
# Check container logs
docker logs <container-id>

# Inspect container
docker inspect <container-id>
```

### Kubernetes Issues

```bash
# Check pod logs
kubectl logs <pod-name>

# Describe pod
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Jenkins Issues

- Check Jenkins console output for specific errors
- Verify credentials are configured correctly
- Ensure Jenkins has access to Docker and kubectl

## 📊 Monitoring

### Application Health Check

```bash
# Direct health check
curl http://localhost:5000/health

# Kubernetes health check
kubectl exec <pod-name> -- curl localhost:5000/health
```

### Pod Status

```bash
# Watch pod status
kubectl get pods -w

# Check resource usage
kubectl top pods
```

## 🔐 Security Notes

- Never commit sensitive data (passwords, keys) to Git
- Use Kubernetes secrets for sensitive information
- Regularly update dependencies for security patches
- Use non-root user in Docker containers (production)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)

## 👨‍💻 Author

DevOps CI/CD Pipeline Case Study Project - 2025

## 📄 License

This project is for educational purposes as part of a DevOps case study.

## 🎯 Learning Outcomes

This project demonstrates:
- ✅ Python Flask web development
- ✅ Docker containerization
- ✅ Kubernetes orchestration
- ✅ Jenkins CI/CD automation
- ✅ Git version control
- ✅ DevOps best practices
- ✅ Infrastructure as Code (IaC)

---

**Note**: Remember to replace `YOUR_DOCKERHUB_USERNAME` in configuration files with your actual Docker Hub username before deploying.

