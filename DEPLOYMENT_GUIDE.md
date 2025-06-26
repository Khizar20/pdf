# PDF Chatbot Kubernetes Deployment Guide

This guide provides step-by-step instructions for deploying the PDF Chatbot application on a Kubernetes cluster using minikube on an Ubuntu EC2 instance.

## Application Overview

The PDF Chatbot is a web application that allows users to upload PDF documents and interact with them using AI. The application consists of:

- **Frontend**: Static HTML/CSS/JS served by nginx
- **Backend**: FastAPI application with authentication and PDF processing
- **Database**: MongoDB for storing user data and PDF content

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │───▶│   Backend   │───▶│   MongoDB   │
│ (nginx)     │    │ (FastAPI)   │    │ (Database)  │
│ LoadBalancer│    │ ClusterIP   │    │ NodePort    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Prerequisites

### 1. EC2 Instance Setup (Ubuntu)

Launch an Ubuntu EC2 instance with:
- Instance type: t3.medium or larger (2 vCPU, 4GB RAM minimum)
- Security groups allowing ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 30000-32767 (NodePort range)

### 2. Install Required Tools

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Logout and login again for group changes to take effect
exit
```

### 3. Start Minikube

```bash
# Start minikube with sufficient resources
minikube start --driver=docker --cpus=2 --memory=4096 --disk-size=20g

# Enable necessary addons
minikube addons enable metrics-server
minikube addons enable storage-provisioner

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Build and Deploy

### 1. Build Docker Images

First, build the application Docker images:

```bash
# Build backend image
cd backend
docker build -t pdf-chatbot-backend:latest .

# Tag for minikube
docker tag pdf-chatbot-backend:latest pdf-chatbot-backend:latest

# Load image into minikube
minikube image load pdf-chatbot-backend:latest

cd ..
```

### 2. Deploy to Kubernetes

```bash
# Make deployment script executable
chmod +x k8s-manifests/deploy.sh

# Run deployment
cd k8s-manifests
./deploy.sh
```

### 3. Verify Deployment

```bash
# Check all resources
kubectl get all -n pdf-chatbot

# Check persistent volume
kubectl get pv,pvc -n pdf-chatbot

# Check HPA status
kubectl get hpa -n pdf-chatbot

# Get service endpoints
kubectl get services -n pdf-chatbot
```

## Accessing the Application

### Frontend Access (LoadBalancer)

```bash
# Get the external IP for frontend service
kubectl get service frontend-service -n pdf-chatbot

# If using minikube, get the URL
minikube service frontend-service -n pdf-chatbot --url
```

### Database Access (NodePort)

```bash
# Get minikube IP
minikube ip

# MongoDB is accessible at: <minikube-ip>:30017
```

## Kubernetes Resources Deployed

### 1. Database Layer
- **mongodb-pvc.yaml**: Persistent Volume Claim (1Gi storage)
- **mongodb-deployment.yaml**: Single replica MongoDB deployment
- **mongodb-service.yaml**: NodePort service (port 30017)

### 2. Backend Layer
- **backend-deployment.yaml**: 3 replicas FastAPI application
- **backend-service.yaml**: ClusterIP service (internal communication)

### 3. Frontend Layer
- **frontend-deployment.yaml**: 3 replicas nginx web server
- **frontend-service.yaml**: LoadBalancer service (external access)

### 4. Configuration
- **configmaps.yaml**: nginx configuration and frontend content

### 5. Auto-scaling
- **hpa.yaml**: HorizontalPodAutoscaler for both frontend and backend

## Key Features Implemented

✅ **Multiple Replicas**: Frontend and backend have 3 replicas each  
✅ **Single Database**: MongoDB has 1 replica as required  
✅ **Persistent Storage**: MongoDB uses PVC for data persistence  
✅ **LoadBalancer**: Frontend service uses LoadBalancer type  
✅ **NodePort**: Database service uses NodePort type  
✅ **Auto-scaling**: HPA monitors CPU/memory and scales pods  
✅ **Resource Limits**: All containers have resource requests/limits  
✅ **Health Checks**: Liveness and readiness probes configured  

## Monitoring and Management

### View Logs
```bash
# Backend logs
kubectl logs -f deployment/backend-deployment -n pdf-chatbot

# Frontend logs
kubectl logs -f deployment/frontend-deployment -n pdf-chatbot

# Database logs
kubectl logs -f deployment/mongodb-deployment -n pdf-chatbot
```

### Scale Manually
```bash
# Scale backend
kubectl scale deployment backend-deployment --replicas=5 -n pdf-chatbot

# Scale frontend
kubectl scale deployment frontend-deployment --replicas=4 -n pdf-chatbot
```

### Monitor HPA
```bash
# Watch HPA in real-time
kubectl get hpa -n pdf-chatbot -w

# Describe HPA for details
kubectl describe hpa frontend-hpa -n pdf-chatbot
```

## Testing Auto-scaling

To test the HorizontalPodAutoscaler:

```bash
# Generate load on the application
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the container, run:
while true; do wget -q -O- http://frontend-service.pdf-chatbot.svc.cluster.local; done
```

## Cleanup

To remove all deployed resources:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

## Troubleshooting

### Common Issues

1. **Images not found**: Ensure Docker images are built and loaded into minikube
2. **Pods pending**: Check if there are sufficient resources
3. **Service not accessible**: Verify security groups and firewall rules
4. **Database connection issues**: Check MongoDB service and credentials

### Useful Commands

```bash
# Describe problematic resources
kubectl describe pod <pod-name> -n pdf-chatbot

# Check events
kubectl get events -n pdf-chatbot --sort-by='.lastTimestamp'

# Port forward for testing
kubectl port-forward service/frontend-service 8080:80 -n pdf-chatbot
```

## Assignment Requirements Checklist

- [x] Well-indented YAML files for Deployment and Service pairs
- [x] Web server and Database server deployments
- [x] Docker image bundled with application code
- [x] Persistent Volume Claim attached to database
- [x] Multiple replicas for web servers
- [x] Single replica for database server
- [x] LoadBalancer service for web server
- [x] NodePort service for database server
- [x] HorizontalPodAutoscaler for auto-scaling
- [x] Deployment on minikube cluster

## Video Demonstration Points

When creating your demonstration video, make sure to show:

1. Minikube cluster running
2. Deploying the application using kubectl
3. All pods running successfully
4. Persistent volume attached to MongoDB
5. LoadBalancer service working
6. NodePort service accessible
7. HPA scaling pods based on load
8. Application functionality (upload PDF, chat)

## Conclusion

This deployment demonstrates a complete Kubernetes setup with:
- Container orchestration using minikube
- Persistent storage for database
- Load balancing and auto-scaling
- Service discovery and networking
- Resource management and monitoring

The application is production-ready with proper health checks, resource limits, and horizontal scaling capabilities. 