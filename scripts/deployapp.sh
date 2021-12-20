cd kubernetes
eksctl create cluster --name bchain-cluster --region eu-west-2 --nodegroup-name bchain-node-group --nodes 3 --nodes-min 3 --nodes-max 3 --node-type t2.micro --with-oidc --ssh-access --ssh-public-key aws_thirdkeypair --managed
# eksctl create cluster --name DemoCluster --region eu-west-2 --nodegroup-name DemoNodes --nodes 4 --nodes-min 4 --nodes-max 5 --node-type t2.micro --with-oidc --ssh-access --ssh-public-key aws_thirdkeypair --managed
#aws eks --region eu-west-2 update-kubeconfig --name eks_cluster_bchain_project
kubectl apply -f frontend.yaml
kubectl apply -f blockchain-engine.yaml
kubectl apply -f credentials.yaml
kubectl apply -f keypair-generator.yaml
kubectl apply -f ./nginx/service.yaml
kubectl apply -f ./nginx/deployment.yaml
kubectl apply -f ./nginx/configmap.yaml
kubectl get pods
kubectl get services