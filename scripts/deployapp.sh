cd kubernetes
aws eks --region eu-west-2 update-kubeconfig --name eks_cluster_final_project
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml
kubectl apply -f ./nginx/service.yaml
kubectl apply -f ./nginx/deployment.yaml
kubectl apply -f ./nginx/configmap.yaml
kubectl get pods
kubectl get services
