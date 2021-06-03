# BChain: A basic blockchain project

##### blockchain application with the following features complete:
1. A homepage at '/' or 'home'
2. A signup page with field to add alias to account (with a uniqueness constraint)
3. A keypair and mnemonic generator for accoutn credentials
4. A blockchain engine with routes to view, mine and check validity
5. A data-persistence mechanism (write to local csv)
6. A page to view registerred addresses and their associated alias

##### the following features are yet to be completed:
1. A landing page for accounts after login
2. Token minting for mining rewards
3. Wallet balances associated with accounts
4. Add transaction data to blocks
5. Add transaction signature requirement

##### application deployment steps complete:
1. Scripts written to automate installation of docker, docker-compose, AWS cli, terraform, ansible and EKS
2. Dockerfiles and docker-compose.yaml are written (nginx is currently containerised and acting as reverse proxy)
3. A terraform script is largely written, requisitioning the various AWS infrastructure to host the application
4. GitHub repository for codebase management is setup

##### application deployment steps to be completed:
1. Kubernetes scripts need updating to reflect the current codebase
2. A Jenkinsfile should be written to automate Jenkins pipeline execution
3. A Docker Hub registry should be setup for the container images of the application microservices
4. Explore the value of writing an Ansible playbok to automate the deployment of the EKS cluster on the infrastructure setup by terraform


### Installation and Setup
##### Linux (Ubuntu 18.04 and later) installation of dependencies
1. sh scripts/docker-install-linux.sh              # install docker
2. sh scripts/docker-compose-install-linux.sh      # install docker-compose
3. sh scripts/ansible-install.sh                   # install ansible
4. sh scripts/awsconfigure.sh                      # install aws cli
5. sh scripts/terraform-install.sh                 # install terraform
6. sh scripts/eksctl.sh                            # install elastic kubernetes

##### Build images and containerise with Docker
1. docker-compose build 
2. docker-compose up -d

##### Requisition AWS infrastructure (Networking and EKS)
1. sh scripts/terraform.sh
2. sh scripts/deployapp.sh