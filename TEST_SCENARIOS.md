# 🧪 Testing Scenarios for Music Playlist Manager CI/CD Pipeline

This document provides comprehensive testing scenarios to validate the entire CI/CD pipeline.

## Test Scenario 1: Local Application Testing

### Objective
Verify the Flask application runs correctly on local machine.

### Steps
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
python app.py

# 3. Access application
# Open browser: http://localhost:5000
```

### Expected Results
- ✅ Application starts without errors
- ✅ Home page loads successfully
- ✅ All navigation links work
- ✅ Can create playlists
- ✅ Can add songs to playlists
- ✅ Search functionality works
- ✅ Health endpoint returns 200 status

### Test Checklist
- [ ] Home page displays total playlists and songs
- [ ] "My Playlists" page shows empty state message
- [ ] Can create a playlist with name, genre, description
- [ ] Created playlist appears in list
- [ ] Can add songs to playlist
- [ ] Songs display correctly in playlist view
- [ ] Search returns correct results
- [ ] Can delete playlists
- [ ] Responsive design works on mobile

---

## Test Scenario 2: Docker Containerization

### Objective
Verify the application can be containerized and run in Docker.

### Steps
```bash
# 1. Build Docker image
docker build -t music-playlist-test .

# 2. Run container
docker run -d -p 5000:5000 --name test-app music-playlist-test

# 3. Check container status
docker ps

# 4. Test application
curl http://localhost:5000/health

# 5. View logs
docker logs test-app

# 6. Stop and remove
docker stop test-app
docker rm test-app
```

### Expected Results
- ✅ Docker image builds without errors
- ✅ Container starts successfully
- ✅ Application accessible on port 5000
- ✅ Health check returns healthy status
- ✅ No errors in container logs

### Test Checklist
- [ ] Dockerfile syntax is valid
- [ ] Image size is reasonable (<500MB)
- [ ] Container starts in <10 seconds
- [ ] All dependencies installed correctly
- [ ] Application responds to HTTP requests
- [ ] Environment variables set correctly
- [ ] Health check passes

---

## Test Scenario 3: Kubernetes Deployment

### Objective
Verify the application deploys correctly to Kubernetes cluster.

### Prerequisites
```bash
# Start Minikube
minikube start
```

### Steps
```bash
# 1. Update deployment.yaml with your Docker Hub username
# Replace: YOUR_DOCKERHUB_USERNAME

# 2. Build and push image to Docker Hub
docker build -t yourusername/music-playlist-manager:latest .
docker push yourusername/music-playlist-manager:latest

# 3. Apply Kubernetes manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 4. Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# 5. Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=music-playlist-manager --timeout=300s

# 6. Access application
minikube service music-playlist-manager-service

# 7. Test from command line
kubectl get svc music-playlist-manager-service
# Note the NodePort (default: 30080)
curl http://localhost:30080/health
```

### Expected Results
- ✅ Deployment created successfully
- ✅ 2 replicas running (as configured)
- ✅ All pods in Running state
- ✅ Service created with NodePort
- ✅ Application accessible via service URL
- ✅ Load balancing works across pods

### Test Checklist
- [ ] Deployment shows READY 2/2
- [ ] All pods STATUS is Running
- [ ] No CrashLoopBackOff errors
- [ ] Service has external endpoint
- [ ] Can access app via NodePort (30080)
- [ ] Health check passes
- [ ] Multiple pods handle requests
- [ ] Persistent volume claim bound (if using)

### Validation Commands
```bash
# Check pod logs
kubectl logs -l app=music-playlist-manager

# Describe deployment
kubectl describe deployment music-playlist-manager

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Test load balancing
for i in {1..10}; do curl http://localhost:30080/health; done

# Check resource usage
kubectl top pods
```

---

## Test Scenario 4: Jenkins Pipeline Execution

### Objective
Verify the Jenkins CI/CD pipeline executes all stages successfully.

### Prerequisites
1. Jenkins server running
2. Docker Hub credentials configured in Jenkins
3. Kubeconfig credentials configured in Jenkins
4. Git repository accessible

### Steps

#### A. Manual Pipeline Trigger
```bash
# 1. Open Jenkins: http://localhost:8080
# 2. Navigate to pipeline job
# 3. Click "Build Now"
# 4. Monitor "Console Output"
```

#### B. Verify Each Stage
1. **Checkout Stage**
   - ✅ Code pulled from Git repository
   - ✅ Latest commit checked out

2. **Build Docker Image Stage**
   - ✅ Docker image built successfully
   - ✅ Image tagged with build number
   - ✅ Latest tag applied

3. **Test Stage**
   - ✅ Container started for testing
   - ✅ Health check passed
   - ✅ Test container cleaned up

4. **Push to Docker Hub Stage**
   - ✅ Login to Docker Hub successful
   - ✅ Image pushed with build number tag
   - ✅ Image pushed with latest tag

5. **Update Kubernetes Manifests Stage**
   - ✅ deployment.yaml updated with new image tag

6. **Deploy to Kubernetes Stage**
   - ✅ Kubernetes deployment updated
   - ✅ Kubernetes service applied
   - ✅ Rollout completed successfully
   - ✅ Pods listed

7. **Verify Deployment Stage**
   - ✅ Pods reach ready state
   - ✅ Verification successful

### Expected Results
- ✅ All pipeline stages complete successfully
- ✅ Build shows SUCCESS status
- ✅ No errors in console output
- ✅ Application deployed to Kubernetes
- ✅ New pods running with updated image

### Test Checklist
- [ ] Pipeline triggered successfully
- [ ] All 7 stages show green checkmarks
- [ ] Build duration under 5 minutes
- [ ] No warnings or errors in output
- [ ] Docker image pushed to registry
- [ ] Kubernetes deployment updated
- [ ] Application accessible after deployment

---

## Test Scenario 5: Automated Pipeline Trigger

### Objective
Verify the pipeline triggers automatically on code push.

### Steps
```bash
# 1. Make a code change
# Edit templates/index.html
# Change "Welcome to Your Music Playlist Manager" to something else

# 2. Commit and push
git add templates/index.html
git commit -m "Test: Update welcome message"
git push origin main

# 3. Wait for Jenkins to detect change (up to 5 minutes)

# 4. Monitor Jenkins dashboard
# Watch for new build to start automatically

# 5. Wait for build to complete

# 6. Verify deployment
kubectl get pods
kubectl rollout status deployment/music-playlist-manager

# 7. Access application and verify change
minikube service music-playlist-manager-service
# Check if welcome message updated
```

### Expected Results
- ✅ Jenkins detects code change within 5 minutes
- ✅ Pipeline triggers automatically
- ✅ Build completes successfully
- ✅ New version deployed to Kubernetes
- ✅ Changes visible in application

### Test Checklist
- [ ] Git push successful
- [ ] Jenkins shows new build after push
- [ ] Build triggered without manual intervention
- [ ] All stages complete successfully
- [ ] New Docker image created
- [ ] Kubernetes pods updated
- [ ] Application shows new changes

---

## Test Scenario 6: Application Functionality Test

### Objective
Comprehensive testing of all application features.

### Test Case 6.1: Create Playlist
```
1. Navigate to "Create Playlist"
2. Enter Name: "Morning Motivation"
3. Select Genre: "Pop"
4. Enter Description: "Uplifting songs to start the day"
5. Click "Create Playlist"

Expected: 
- Success message appears
- Redirected to playlists page
- New playlist visible in list
```

### Test Case 6.2: Add Songs to Playlist
```
1. Click on "Morning Motivation" playlist
2. Scroll to "Add New Song" section
3. Enter Song Title: "Happy"
4. Enter Artist: "Pharrell Williams"
5. Enter Duration: "3:53"
6. Click "Add Song"

Expected:
- Success message appears
- Song appears in playlist
- Song count updates
```

### Test Case 6.3: Search Functionality
```
1. Navigate to "Search"
2. Enter search query: "Happy"
3. Click "Search"

Expected:
- "Morning Motivation" playlist appears in results
- Search shows correct number of results
```

### Test Case 6.4: Delete Playlist
```
1. Navigate to "My Playlists"
2. Find "Morning Motivation"
3. Click "Delete"
4. Confirm deletion

Expected:
- Confirmation dialog appears
- Playlist removed from list
- Success message displayed
```

### Test Case 6.5: Multiple Playlists
```
1. Create 5 different playlists
2. Add 3 songs to each
3. View all playlists

Expected:
- Home shows "5 Total Playlists"
- Home shows "15 Total Songs"
- All playlists display correctly
```

---

## Test Scenario 7: Rollback Test

### Objective
Verify ability to rollback to previous version.

### Steps
```bash
# 1. Note current application state
kubectl get pods
kubectl rollout history deployment/music-playlist-manager

# 2. Make a breaking change (intentionally)
# Edit app.py and introduce syntax error

# 3. Commit and push
git add app.py
git commit -m "Test: Breaking change"
git push origin main

# 4. Wait for pipeline to fail or deploy broken version

# 5. Rollback deployment
kubectl rollout undo deployment/music-playlist-manager

# 6. Verify rollback
kubectl rollout status deployment/music-playlist-manager
kubectl get pods

# 7. Fix the code
# Correct the syntax error

# 8. Commit and push fix
git add app.py
git commit -m "Fix: Correct syntax error"
git push origin main
```

### Expected Results
- ✅ Rollback command executes successfully
- ✅ Previous version restored
- ✅ Application functional again
- ✅ Fix deployed successfully

---

## Test Scenario 8: Scale Test

### Objective
Test Kubernetes scaling capabilities.

### Steps
```bash
# 1. Check current replicas
kubectl get deployment music-playlist-manager

# 2. Scale up to 5 replicas
kubectl scale deployment music-playlist-manager --replicas=5

# 3. Watch pods being created
kubectl get pods -w

# 4. Verify all pods running
kubectl get pods

# 5. Test load distribution
for i in {1..20}; do curl http://localhost:30080/health; echo ""; done

# 6. Scale down to 2 replicas
kubectl scale deployment music-playlist-manager --replicas=2

# 7. Watch pods being terminated
kubectl get pods -w
```

### Expected Results
- ✅ Deployment scales up to 5 pods
- ✅ All pods reach Running state
- ✅ Load distributed across pods
- ✅ Deployment scales down to 2 pods
- ✅ Application remains available during scaling

---

## Test Scenario 9: Data Persistence Test

### Objective
Verify data persists across pod restarts.

### Steps
```bash
# 1. Create a playlist in the application

# 2. Add some songs

# 3. Note the pod name
kubectl get pods

# 4. Delete the pod
kubectl delete pod <pod-name>

# 5. Wait for new pod to start
kubectl get pods -w

# 6. Access application again

# 7. Check if playlist still exists
```

### Expected Results
- ✅ New pod created automatically
- ✅ Application accessible
- ⚠️ Data lost (expected - no persistent volume attached by default)

### To Enable Persistence
```yaml
# Add to deployment.yaml:
volumeMounts:
- name: data
  mountPath: /app/data
volumes:
- name: data
  persistentVolumeClaim:
    claimName: music-playlist-data
```

---

## Test Scenario 10: Performance Test

### Objective
Basic performance testing.

### Steps
```bash
# Install Apache Bench (if not installed)
# Windows: Download from Apache website
# Linux: sudo apt-get install apache2-utils

# Test with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:30080/

# Test health endpoint
ab -n 1000 -c 50 http://localhost:30080/health

# Monitor resource usage
kubectl top pods
kubectl top nodes
```

### Expected Results
- ✅ Handles 100 requests successfully
- ✅ Average response time <500ms
- ✅ No failed requests
- ✅ CPU/Memory within limits

---

## Test Report Template

After running all tests, document results:

```
Test Execution Report
Date: [DATE]
Tester: [NAME]
Environment: [Local/Dev/Staging]

| Scenario | Status | Issues | Notes |
|----------|--------|--------|-------|
| 1. Local App | ✅ PASS | None | All features working |
| 2. Docker | ✅ PASS | None | Container runs smoothly |
| 3. Kubernetes | ✅ PASS | None | Deployment successful |
| 4. Jenkins Pipeline | ✅ PASS | None | All stages passed |
| 5. Auto Trigger | ✅ PASS | None | Detected in 3 mins |
| 6. Application | ✅ PASS | None | All features tested |
| 7. Rollback | ✅ PASS | None | Rollback successful |
| 8. Scaling | ✅ PASS | None | Scaled to 5 pods |
| 9. Persistence | ⚠️ PARTIAL | Data loss | Need PV setup |
| 10. Performance | ✅ PASS | None | Good response times |

Overall Status: ✅ READY FOR PRODUCTION

Recommendations:
1. Add persistent volume for data storage
2. Implement database instead of JSON file
3. Add monitoring and alerts
4. Configure horizontal pod autoscaling
```

---

## Continuous Testing Checklist

### Daily Checks
- [ ] Jenkins server running
- [ ] Kubernetes cluster healthy
- [ ] All pods running
- [ ] Application accessible
- [ ] No errors in logs

### After Each Deployment
- [ ] All pipeline stages passed
- [ ] Health check returns 200
- [ ] UI loads correctly
- [ ] Core features working
- [ ] No console errors

### Weekly Checks
- [ ] Review Jenkins build history
- [ ] Check resource usage trends
- [ ] Update dependencies
- [ ] Backup configurations
- [ ] Review security updates

---

**Remember:** Thorough testing ensures a reliable CI/CD pipeline! 🧪✅

