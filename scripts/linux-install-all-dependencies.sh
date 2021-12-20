#! /bin/bash

sudo apt update

if [ "$(aws --version)" != "" ] 
then echo "$(aws --version)"
else sh BChain_Project/scripts/awsconfigure.sh && echo "aws cli installed"
fi

if [ "$(docker --version)" != "" ] 
then echo "$(docker --version)"
else sh BChain_Project/scripts/docker-install-linux.sh && echo "docker installed"
fi

if [ "$(docker-compose --version)" != "" ] 
then echo "$(docker-compose --version)"
else sh BChain_Project/scripts/docker-compose-install-linux.sh && echo "docker-compose installed"
fi

if [ "$(terraform version)" != "" ] 
then echo "$(terraform --version)"
else sh BChain_Project/scripts/terraform-install.sh && echo "terraform installed"
fi

if [ "$(eksctl version)" != "" && "$(kubectl version --client)" != ""] 
then echo "$(eksctl version)" && echo "$(kubectl version --client)"
else sh BChain_Project/scripts/eksctl.sh && echo "kubernetes and kubectl installed"
fi
