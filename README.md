# BChain: A basic blockchain project

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