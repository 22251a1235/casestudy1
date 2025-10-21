# 🏗️ Architecture Documentation - Music Playlist Manager CI/CD Pipeline

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Developer Workflow                           │
│                                                                      │
│  Developer → Code Change → Git Commit → Git Push → Remote Repo     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ Webhook/Poll
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Jenkins CI/CD Pipeline                       │
│                                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │ Checkout │ → │  Build   │ → │   Test   │ → │   Push   │        │
│  │   Code   │   │  Docker  │   │  Docker  │   │  Docker  │        │
│  │          │   │  Image   │   │  Image   │   │   Hub    │        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│                                                      │               │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐       │               │
│  │  Verify  │ ← │  Deploy  │ ← │  Update  │ ←─────┘               │
│  │Deployment│   │    to    │   │   K8s    │                       │
│  │          │   │   K8s    │   │ Manifest │                       │
│  └──────────┘   └──────────┘   └──────────┘                       │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                        Deployment                           │   │
│  │                                                             │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │   │
│  │  │   Pod 1      │  │   Pod 2      │  │   Pod 3      │    │   │
│  │  │              │  │              │  │              │    │   │
│  │  │  Container   │  │  Container   │  │  Container   │    │   │
│  │  │   Flask      │  │   Flask      │  │   Flask      │    │   │
│  │  │   App        │  │   App        │  │   App        │    │   │
│  │  │  :5000       │  │  :5000       │  │  :5000       │    │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
│                             │                                       │
│  ┌──────────────────────────┴──────────────────────────────────┐   │
│  │                         Service                              │   │
│  │                  (LoadBalancer/NodePort)                     │   │
│  │                      Port: 30080                             │   │
│  └──────────────────────────┬──────────────────────────────────┘   │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            End Users                                 │
│                      http://localhost:30080                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Application Layer (Flask)

```
┌─────────────────────────────────────────┐
│         Flask Application               │
├─────────────────────────────────────────┤
│                                         │
│  ├─ app.py (Main Application)          │
│  │   ├─ Routes                          │
│  │   │   ├─ / (Home)                    │
│  │   │   ├─ /playlists                  │
│  │   │   ├─ /create                     │
│  │   │   ├─ /playlist/<id>              │
│  │   │   ├─ /search                     │
│  │   │   └─ /health                     │
│  │   │                                  │
│  │   ├─ Business Logic                  │
│  │   │   ├─ load_playlists()            │
│  │   │   ├─ save_playlists()            │
│  │   │   └─ playlist management         │
│  │   │                                  │
│  │   └─ Data Storage                    │
│  │       └─ playlists.json              │
│  │                                      │
│  └─ templates/ (HTML Templates)         │
│      ├─ base.html                       │
│      ├─ index.html                      │
│      ├─ playlists.html                  │
│      ├─ create.html                     │
│      ├─ view_playlist.html              │
│      └─ search.html                     │
│                                         │
└─────────────────────────────────────────┘
```

### 2. Containerization Layer (Docker)

```
┌─────────────────────────────────────────┐
│         Docker Container                │
├─────────────────────────────────────────┤
│                                         │
│  Base Image: python:3.11-slim           │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Application Files                │ │
│  │  ├─ app.py                        │ │
│  │  ├─ templates/                    │ │
│  │  ├─ requirements.txt              │ │
│  │  └─ playlists.json                │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Python Dependencies              │ │
│  │  ├─ Flask 3.0.0                   │ │
│  │  └─ Werkzeug 3.0.1                │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Exposed Port: 5000                     │
│  Health Check: /health endpoint         │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Orchestration Layer (Kubernetes)

```
┌─────────────────────────────────────────────────────────────┐
│                  Kubernetes Resources                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Deployment: music-playlist-manager                │   │
│  ├────────────────────────────────────────────────────┤   │
│  │  Replicas: 2                                       │   │
│  │  Strategy: RollingUpdate                           │   │
│  │  Image: yourusername/music-playlist-manager:latest │   │
│  │                                                     │   │
│  │  Resources:                                        │   │
│  │    Requests: 128Mi memory, 100m CPU                │   │
│  │    Limits: 256Mi memory, 500m CPU                  │   │
│  │                                                     │   │
│  │  Probes:                                           │   │
│  │    Liveness: GET /health (30s interval)            │   │
│  │    Readiness: GET /health (10s interval)           │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Service: music-playlist-manager-service           │   │
│  ├────────────────────────────────────────────────────┤   │
│  │  Type: NodePort                                    │   │
│  │  Port: 80                                          │   │
│  │  TargetPort: 5000                                  │   │
│  │  NodePort: 30080                                   │   │
│  │  Selector: app=music-playlist-manager              │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │  PersistentVolumeClaim (Optional)                  │   │
│  ├────────────────────────────────────────────────────┤   │
│  │  Name: music-playlist-data                         │   │
│  │  Storage: 1Gi                                      │   │
│  │  AccessMode: ReadWriteOnce                         │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. CI/CD Pipeline (Jenkins)

```
┌─────────────────────────────────────────────────────────────┐
│                   Jenkins Pipeline Stages                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Stage 1: Checkout                                          │
│  ├─ Pull latest code from Git repository                   │
│  └─ Checkout specified branch (main)                       │
│                                                             │
│  Stage 2: Build Docker Image                               │
│  ├─ Execute: docker build                                  │
│  ├─ Tag: BUILD_NUMBER                                      │
│  └─ Tag: latest                                            │
│                                                             │
│  Stage 3: Test                                             │
│  ├─ Run container                                          │
│  ├─ Test /health endpoint                                  │
│  └─ Stop and remove test container                         │
│                                                             │
│  Stage 4: Push to Docker Hub                               │
│  ├─ Authenticate with Docker Hub                           │
│  ├─ Push image with build number tag                       │
│  └─ Push image with latest tag                             │
│                                                             │
│  Stage 5: Update Kubernetes Manifests                      │
│  ├─ Update deployment.yaml                                 │
│  └─ Set new image tag                                      │
│                                                             │
│  Stage 6: Deploy to Kubernetes                             │
│  ├─ Apply deployment.yaml                                  │
│  ├─ Apply service.yaml                                     │
│  ├─ Wait for rollout completion                            │
│  └─ Display pod and service status                         │
│                                                             │
│  Stage 7: Verify Deployment                                │
│  ├─ Wait for pods to be ready                              │
│  └─ Confirm deployment success                             │
│                                                             │
│  Post-Build Actions:                                       │
│  ├─ Success: Log completion message                        │
│  ├─ Failure: Log error details                             │
│  └─ Always: Clean up Docker images                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Request Flow

```
User Browser
     │
     │ HTTP Request (http://localhost:30080)
     ▼
Kubernetes Service (NodePort 30080)
     │
     │ Load Balance
     ▼
Pod Selection (Round-robin)
     │
     │ Forward to Port 5000
     ▼
Flask Application Container
     │
     │ Process Request
     ├─ Route Matching
     ├─ Business Logic
     └─ Data Access (playlists.json)
     │
     │ Render Template
     ▼
HTML Response
     │
     │ HTTP Response
     ▼
User Browser (Display)
```

### CI/CD Data Flow

```
Developer
     │
     │ git push
     ▼
Git Repository (GitHub/GitLab)
     │
     │ Webhook/Poll Trigger
     ▼
Jenkins Server
     │
     ├─ Clone Repository
     │      │
     │      ▼
     │  Docker Build
     │      │
     │      ▼
     │  Docker Registry (Docker Hub)
     │      │
     │      ▼
     │  Kubernetes Cluster
     │      │
     │      ├─ Pull Image
     │      ├─ Create/Update Pods
     │      └─ Update Service
     │
     ▼
Application Deployed
```

## Technology Stack

### Development
- **Language**: Python 3.11
- **Framework**: Flask 3.0.0
- **Template Engine**: Jinja2 (Flask built-in)
- **Data Storage**: JSON file (playlists.json)

### Containerization
- **Container Runtime**: Docker
- **Base Image**: python:3.11-slim
- **Registry**: Docker Hub

### Orchestration
- **Platform**: Kubernetes
- **Local Environment**: Minikube
- **Service Type**: NodePort
- **Deployment Strategy**: RollingUpdate

### CI/CD
- **Automation**: Jenkins
- **Pipeline**: Declarative Pipeline
- **Version Control**: Git
- **Build Trigger**: SCM Polling / Webhook

### Infrastructure
- **Host OS**: Windows/Linux
- **Networking**: Docker Bridge, Kubernetes CNI
- **Storage**: Local filesystem, Kubernetes PV/PVC

## Security Considerations

### Application Security
```
┌─────────────────────────────────────────┐
│  Security Layer                         │
├─────────────────────────────────────────┤
│  ├─ Flask Secret Key                    │
│  ├─ Input Validation                    │
│  ├─ XSS Protection (Template Escaping)  │
│  └─ Session Management                  │
└─────────────────────────────────────────┘
```

### Container Security
```
┌─────────────────────────────────────────┐
│  Container Security                     │
├─────────────────────────────────────────┤
│  ├─ Minimal Base Image (slim)           │
│  ├─ Non-root User (recommended)         │
│  ├─ No Hardcoded Secrets                │
│  ├─ Health Checks                       │
│  └─ Resource Limits                     │
└─────────────────────────────────────────┘
```

### Kubernetes Security
```
┌─────────────────────────────────────────┐
│  Kubernetes Security                    │
├─────────────────────────────────────────┤
│  ├─ Resource Quotas                     │
│  ├─ Network Policies                    │
│  ├─ RBAC (Role-Based Access Control)    │
│  ├─ Secrets Management                  │
│  └─ Pod Security Policies               │
└─────────────────────────────────────────┘
```

### Jenkins Security
```
┌─────────────────────────────────────────┐
│  Jenkins Security                       │
├─────────────────────────────────────────┤
│  ├─ Credentials Store (Encrypted)       │
│  ├─ Authentication & Authorization      │
│  ├─ Audit Logs                          │
│  └─ Secure Pipeline Scripts             │
└─────────────────────────────────────────┘
```

## Scalability & High Availability

### Horizontal Pod Autoscaling (Future Enhancement)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: music-playlist-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: music-playlist-manager
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Load Distribution
```
                    Users
                      │
                      ▼
              Kubernetes Service
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
       Pod 1        Pod 2        Pod 3
      (33.3%)      (33.3%)      (33.3%)
```

## Monitoring & Logging

### Monitoring Architecture (Recommended)
```
┌─────────────────────────────────────────────────────────┐
│                   Monitoring Stack                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │  Prometheus  │ ←─ │   Metrics    │ ←─ │   Pods   │ │
│  │  (Metrics)   │    │   Server     │    │          │ │
│  └──────┬───────┘    └──────────────┘    └──────────┘ │
│         │                                               │
│         │ Query                                         │
│         ▼                                               │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │   Grafana    │    │  AlertManager│                 │
│  │ (Dashboard)  │    │  (Alerts)    │                 │
│  └──────────────┘    └──────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Logging Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Logging Stack                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Pods → Stdout/Stderr → Container Runtime → kubectl    │
│                              │                           │
│                              ▼                           │
│                    ┌──────────────────┐                 │
│                    │  Log Aggregator  │                 │
│                    │  (ELK/Loki)      │                 │
│                    └──────────────────┘                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Network Layers                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  External Network                                            │
│         │                                                    │
│         │ Port 30080                                         │
│         ▼                                                    │
│  ┌────────────────┐                                         │
│  │  NodePort      │                                         │
│  │  Service       │                                         │
│  └────────┬───────┘                                         │
│           │                                                  │
│           │ Port 80                                          │
│           ▼                                                  │
│  ┌────────────────┐                                         │
│  │  ClusterIP     │                                         │
│  │  (Internal LB) │                                         │
│  └────────┬───────┘                                         │
│           │                                                  │
│           │ Port 5000                                        │
│           ▼                                                  │
│  ┌─────────────────────────────────────┐                   │
│  │            Pod Network               │                   │
│  │  ┌──────┐  ┌──────┐  ┌──────┐      │                   │
│  │  │ Pod1 │  │ Pod2 │  │ Pod3 │      │                   │
│  │  │:5000 │  │:5000 │  │:5000 │      │                   │
│  │  └──────┘  └──────┘  └──────┘      │                   │
│  └─────────────────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Strategies

### Current: Rolling Update
```
Step 1: Initial State          Step 2: Create New Pod
┌─────┐ ┌─────┐               ┌─────┐ ┌─────┐ ┌─────┐
│ v1  │ │ v1  │               │ v1  │ │ v1  │ │ v2  │
└─────┘ └─────┘               └─────┘ └─────┘ └─────┘

Step 3: Remove Old Pod         Step 4: Complete
┌─────┐ ┌─────┐               ┌─────┐ ┌─────┐
│ v1  │ │ v2  │               │ v2  │ │ v2  │
└─────┘ └─────┘               └─────┘ └─────┘
```

### Alternative: Blue-Green (Future)
```
Blue Environment (v1)          Green Environment (v2)
┌─────┐ ┌─────┐               ┌─────┐ ┌─────┐
│ v1  │ │ v1  │               │ v2  │ │ v2  │
└─────┘ └─────┘               └─────┘ └─────┘
    ▲                              │
    │                              │
    │         Switch Traffic       │
    └──────────────────────────────┘
```

## File Structure

```
casestudy35/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── .dockerignore              # Docker ignore patterns
├── deployment.yaml            # Kubernetes deployment
├── service.yaml               # Kubernetes service
├── Jenkinsfile                # CI/CD pipeline
├── .gitignore                 # Git ignore patterns
├── README.md                  # Project documentation
├── SETUP_GUIDE.md             # Detailed setup instructions
├── TEST_SCENARIOS.md          # Testing documentation
├── QUICK_COMMANDS.md          # Command reference
├── ARCHITECTURE.md            # This file
├── templates/                 # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── playlists.html
│   ├── create.html
│   ├── view_playlist.html
│   └── search.html
└── playlists.json             # Data storage (runtime)
```

---

**This architecture ensures:**
- ✅ Automated deployments
- ✅ High availability
- ✅ Scalability
- ✅ Easy rollbacks
- ✅ Continuous integration
- ✅ Infrastructure as code

