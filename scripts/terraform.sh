#!/bin/bash
#eksctl create cluster --name bchain-cluster --region eu-west-1 --nodegroup-name bchain-node-group --nodes 3 --nodes-min 3 --nodes-max 3 --node-type t2.micro --with-oidc --ssh-access --ssh-public-key aws-myfirstkeypair --managed
cd terraform-working
terraform init
terraform plan -out=tfplan
terraform apply "tfplan"

