# ⚡ Quick Command Reference

A cheat sheet for common commands used in this project.

## 🐳 Docker Commands

```bash
# Build image
docker build -t music-playlist-manager .

# Run container
docker run -d -p 5000:5000 music-playlist-manager

# View running containers
docker ps

# View all containers
docker ps -a

# Stop container
docker stop <container-id>

# Remove container
docker rm <container-id>

# View logs
docker logs <container-id>
docker logs -f <container-id>  # Follow logs

# Login to Docker Hub
docker login

# Tag image
docker tag music-playlist-manager:latest yourusername/music-playlist-manager:latest

# Push to Docker Hub
docker push yourusername/music-playlist-manager:latest

# Pull from Docker Hub
docker pull yourusername/music-playlist-manager:latest

# Remove image
docker rmi <image-id>

# Clean up
docker system prune -a  # Remove all unused containers, images
```

## ☸️ Kubernetes Commands

```bash
# Start Minikube
minikube start

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Check cluster info
kubectl cluster-info

# Get nodes
kubectl get nodes

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Get all resources
kubectl get all

# Get deployments
kubectl get deployments
kubectl get deploy  # Short form

# Get pods
kubectl get pods
kubectl get po  # Short form

# Get services
kubectl get services
kubectl get svc  # Short form

# Describe resources
kubectl describe deployment music-playlist-manager
kubectl describe pod <pod-name>
kubectl describe service music-playlist-manager-service

# View pod logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
kubectl logs -l app=music-playlist-manager  # All pods with label

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash
kubectl exec <pod-name> -- curl localhost:5000/health

# Scale deployment
kubectl scale deployment music-playlist-manager --replicas=3

# Update deployment
kubectl set image deployment/music-playlist-manager music-playlist-manager=yourusername/music-playlist-manager:v2

# Rollout commands
kubectl rollout status deployment/music-playlist-manager
kubectl rollout history deployment/music-playlist-manager
kubectl rollout undo deployment/music-playlist-manager
kubectl rollout restart deployment/music-playlist-manager

# Delete resources
kubectl delete deployment music-playlist-manager
kubectl delete service music-playlist-manager-service
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml

# Port forward
kubectl port-forward service/music-playlist-manager-service 8080:80

# Get service URL (Minikube)
minikube service music-playlist-manager-service
minikube service music-playlist-manager-service --url

# Watch resources
kubectl get pods -w

# Get events
kubectl get events
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource usage
kubectl top nodes
kubectl top pods

# Get YAML of running resource
kubectl get deployment music-playlist-manager -o yaml
kubectl get service music-playlist-manager-service -o yaml

# Edit resource directly
kubectl edit deployment music-playlist-manager

# Create from literal
kubectl create deployment test --image=nginx
```

## 🔧 Git Commands

```bash
# Initialize repository
git init

# Check status
git status

# Add files
git add .
git add <file-name>

# Commit changes
git commit -m "Your message"

# View commit history
git log
git log --oneline

# Add remote
git remote add origin <url>

# View remotes
git remote -v

# Push to remote
git push origin main
git push -u origin main  # Set upstream

# Pull from remote
git pull origin main

# Create branch
git branch <branch-name>

# Switch branch
git checkout <branch-name>
git switch <branch-name>  # New way

# Create and switch
git checkout -b <branch-name>

# View branches
git branch
git branch -a  # Including remote

# Merge branch
git merge <branch-name>

# View differences
git diff
git diff <file-name>

# Discard changes
git restore <file-name>
git restore .

# Remove file
git rm <file-name>

# Rename file
git mv <old-name> <new-name>

# View file history
git log <file-name>

# Stash changes
git stash
git stash pop
git stash list

# Tag version
git tag v1.0.0
git push origin v1.0.0
```

## 🔨 Jenkins Commands

```bash
# Start Jenkins (if installed locally)
sudo systemctl start jenkins
sudo systemctl stop jenkins
sudo systemctl restart jenkins
sudo systemctl status jenkins

# Jenkins in Docker
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts

# Get initial admin password (Docker)
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# View Jenkins logs (Docker)
docker logs jenkins
docker logs -f jenkins

# Access Jenkins container
docker exec -it jenkins bash

# Backup Jenkins home
docker cp jenkins:/var/jenkins_home ./jenkins-backup

# Restore Jenkins home
docker cp ./jenkins-backup jenkins:/var/jenkins_home
```

## 🐍 Python/Flask Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Run with debug mode
export FLASK_DEBUG=1  # Linux/Mac
set FLASK_DEBUG=1     # Windows
python app.py

# Install specific package
pip install flask

# Update package
pip install --upgrade flask

# Generate requirements.txt
pip freeze > requirements.txt

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate
```

## 🌐 Network/Testing Commands

```bash
# Check port usage
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux/Mac

# Kill process by port
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>

# Test HTTP endpoint
curl http://localhost:5000
curl http://localhost:5000/health

# Test with headers
curl -H "Content-Type: application/json" http://localhost:5000

# POST request
curl -X POST -d "name=test" http://localhost:5000/create

# Save response
curl http://localhost:5000 -o output.html

# Follow redirects
curl -L http://localhost:5000

# Performance test (requires Apache Bench)
ab -n 100 -c 10 http://localhost:5000/
```

## 🔍 Troubleshooting Commands

```bash
# Check if service is running
# Docker
docker ps | grep music-playlist

# Kubernetes
kubectl get pods | grep music-playlist

# Check logs for errors
# Docker
docker logs <container-id> | grep -i error

# Kubernetes
kubectl logs <pod-name> | grep -i error

# Check resource limits
kubectl describe pod <pod-name> | grep -A 5 "Limits"

# Check events for issues
kubectl get events --field-selector type!=Normal

# Verify connectivity
kubectl run test-pod --rm -it --image=busybox -- /bin/sh
# Then inside pod:
wget -O- http://music-playlist-manager-service/health

# DNS check in Kubernetes
kubectl run test-pod --rm -it --image=busybox -- nslookup music-playlist-manager-service

# Check disk space
df -h

# Check memory usage
free -m

# Check CPU usage
top
htop
```

## 📦 Complete Deployment Flow

```bash
# 1. Build and test locally
python app.py
# Test in browser

# 2. Build Docker image
docker build -t yourusername/music-playlist-manager:latest .

# 3. Test Docker container
docker run -d -p 5000:5000 yourusername/music-playlist-manager:latest
curl http://localhost:5000/health
docker stop <container-id>

# 4. Push to Docker Hub
docker login
docker push yourusername/music-playlist-manager:latest

# 5. Deploy to Kubernetes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 6. Verify deployment
kubectl get pods
kubectl rollout status deployment/music-playlist-manager

# 7. Access application
minikube service music-playlist-manager-service

# 8. Commit changes
git add .
git commit -m "Deploy version 1.0"
git push origin main

# 9. Watch Jenkins pipeline
# Open http://localhost:8080
```

## 🔄 Update Application Flow

```bash
# 1. Make code changes
# Edit files...

# 2. Test locally
python app.py

# 3. Commit and push
git add .
git commit -m "Update: description of changes"
git push origin main

# 4. Jenkins automatically:
#    - Detects change
#    - Builds new image
#    - Pushes to Docker Hub
#    - Deploys to Kubernetes

# 5. Verify deployment
kubectl rollout status deployment/music-playlist-manager
kubectl get pods

# 6. Check application
minikube service music-playlist-manager-service
```

## 🚨 Emergency Commands

```bash
# Rollback Kubernetes deployment
kubectl rollout undo deployment/music-playlist-manager

# Restart all pods
kubectl rollout restart deployment/music-playlist-manager

# Force delete pod
kubectl delete pod <pod-name> --force --grace-period=0

# Remove all resources
kubectl delete all --all

# Stop all Docker containers
docker stop $(docker ps -q)

# Remove all Docker containers
docker rm $(docker ps -aq)

# Restart Minikube
minikube stop && minikube start

# Reset Jenkins build history
# Navigate to job > Configure > Build History > Discard old builds
```

## 📊 Monitoring Commands

```bash
# Watch pod status continuously
watch kubectl get pods

# Monitor logs in real-time
kubectl logs -f <pod-name>

# Monitor all pods logs
kubectl logs -f -l app=music-playlist-manager

# Resource usage
kubectl top pods --all-namespaces
kubectl top nodes

# Get pod metrics
kubectl get --raw /apis/metrics.k8s.io/v1beta1/pods

# Port forward for local access
kubectl port-forward <pod-name> 8080:5000
```

---

## 💡 Pro Tips

1. **Use aliases for common commands:**
   ```bash
   alias k='kubectl'
   alias kgp='kubectl get pods'
   alias kgs='kubectl get services'
   alias kgd='kubectl get deployments'
   ```

2. **Enable kubectl autocomplete:**
   ```bash
   # Bash
   source <(kubectl completion bash)
   
   # Zsh
   source <(kubectl completion zsh)
   ```

3. **Watch multiple resources:**
   ```bash
   watch 'kubectl get pods && kubectl get svc && kubectl get deploy'
   ```

4. **Quick pod logs:**
   ```bash
   kubectl logs -l app=music-playlist-manager --tail=50
   ```

5. **Export resources for backup:**
   ```bash
   kubectl get all -o yaml > backup.yaml
   ```

---

**Save this file for quick reference during development and deployment!** 📚

