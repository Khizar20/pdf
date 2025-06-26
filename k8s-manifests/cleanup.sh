#!/bin/bash

echo "=== Cleaning up PDF Chatbot Application from Kubernetes ==="

echo "Removing HorizontalPodAutoscaler..."
kubectl delete -f hpa.yaml -n pdf-chatbot || echo "HPA not found"

echo "Removing Frontend..."
kubectl delete -f frontend-service.yaml -n pdf-chatbot || echo "Frontend service not found"
kubectl delete -f frontend-deployment.yaml -n pdf-chatbot || echo "Frontend deployment not found"

echo "Removing Backend..."
kubectl delete -f backend-service.yaml -n pdf-chatbot || echo "Backend service not found"
kubectl delete -f backend-deployment.yaml -n pdf-chatbot || echo "Backend deployment not found"

echo "Removing Database..."
kubectl delete -f mongodb-service.yaml -n pdf-chatbot || echo "MongoDB service not found"
kubectl delete -f mongodb-deployment.yaml -n pdf-chatbot || echo "MongoDB deployment not found"

echo "Removing PVC..."
kubectl delete -f mongodb-pvc.yaml -n pdf-chatbot || echo "PVC not found"

echo "Removing ConfigMaps..."
kubectl delete -f configmaps.yaml -n pdf-chatbot || echo "ConfigMaps not found"

echo "Removing namespace..."
kubectl delete namespace pdf-chatbot || echo "Namespace not found"

echo "=== Cleanup Complete ===" 