cd kubernetes
#eksctl create cluster --name bchain-cluster --region eu-west-1 --nodegroup-name bchain-node-group --nodes 4 --nodes-min 4 --nodes-max 5 --node-type t2.micro --with-oidc --ssh-access --ssh-public-key aws-myfirstkeypair --managed
aws eks --region eu-west-1 update-kubeconfig --name eks-cluster #bchain-cluster
kubectl apply -f wordlist_reader.yaml
kubectl apply -f wordlist_parser.yaml
kubectl apply -f username_generator.yaml
kubectl apply -f password_generator.yaml
kubectl apply -f seedphrase_generator.yaml
kubectl apply -f pandas_jsonreader.yaml
kubectl apply -f database.yaml
kubectl apply -f frontend_login.yaml
kubectl apply -f ./nginx/service.yaml
kubectl apply -f ./nginx/deployment.yaml
kubectl apply -f ./nginx/configmap.yaml
kubectl get pods
kubectl get services
