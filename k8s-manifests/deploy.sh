#!/bin/bash

echo "=== Deploying PDF Chatbot Application to Kubernetes ==="

# Create namespace
echo "Creating namespace..."
kubectl create namespace pdf-chatbot || echo "Namespace already exists"

# Apply all manifests in the correct order
echo "Applying ConfigMaps..."
kubectl apply -f configmaps.yaml -n pdf-chatbot

echo "Applying Persistent Volume Claim..."
kubectl apply -f mongodb-pvc.yaml -n pdf-chatbot

echo "Applying Database Deployment and Service..."
kubectl apply -f mongodb-deployment.yaml -n pdf-chatbot
kubectl apply -f mongodb-service.yaml -n pdf-chatbot

echo "Waiting for MongoDB to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/mongodb-deployment -n pdf-chatbot

echo "Applying Backend Deployment and Service..."
kubectl apply -f backend-deployment.yaml -n pdf-chatbot
kubectl apply -f backend-service.yaml -n pdf-chatbot

echo "Waiting for Backend to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment -n pdf-chatbot

echo "Applying Frontend Deployment and Service..."
kubectl apply -f frontend-deployment.yaml -n pdf-chatbot
kubectl apply -f frontend-service.yaml -n pdf-chatbot

echo "Waiting for Frontend to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment -n pdf-chatbot

echo "Applying HorizontalPodAutoscaler..."
kubectl apply -f hpa.yaml -n pdf-chatbot

echo "=== Deployment Complete ==="
echo ""
echo "Check the status of your pods:"
echo "kubectl get pods -n pdf-chatbot"
echo ""
echo "Check the services:"
echo "kubectl get services -n pdf-chatbot"
echo ""
echo "Get the LoadBalancer IP for frontend access:"
echo "kubectl get service frontend-service -n pdf-chatbot"
echo ""
echo "Monitor HPA:"
echo "kubectl get hpa -n pdf-chatbot" 