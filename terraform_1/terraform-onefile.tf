provider "aws" {
   region = var.region
   version = "~> 2.7"
   access_key = var.access_key
   secret_key = var.secret_key
}
#######################
##
###  VPC
##
#######################

variable "eks_cluster_name" {
    type        = string
    description = "The name of the EKS Cluster"
    default = "bchain-cluster"
}

variable "region" {
    type        = string
    description = "The name of the EKS Cluster"
    default = "eu-west-1"
}

variable "access_key" {
}

variable "secret_key" {
}

data "aws_availability_zones" "availability_zones" {
    state = "available"
}

resource "aws_vpc" "app_vpc" {
    cidr_block              = "10.0.0.0/16"
    enable_dns_hostnames    = true
}

resource "aws_internet_gateway" "app_internet_gateway" {
    vpc_id = aws_vpc.app_vpc.id
}

locals {
    number_to_create = length(data.aws_availability_zones.availability_zones.names)
}

resource "aws_subnet" "app_subnets" {
    count                   = local.number_to_create
    map_public_ip_on_launch = true
    availability_zone       = data.aws_availability_zones.availability_zones.names[count.index]
    cidr_block              = cidrsubnet(aws_vpc.app_vpc.cidr_block, 8, count.index + 1)
    vpc_id                  = aws_vpc.app_vpc.id

    tags = {
        "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    }
}

resource "aws_route_table" "app_route_tables" {
    count  = local.number_to_create
    vpc_id = aws_vpc.app_vpc.id
    

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.app_internet_gateway.id
    }

    tags = {
        Name = "app_route_table_${count.index + 1}"
    }
}

resource "aws_route_table_association" "route_table_association" {
    count           = local.number_to_create
    route_table_id  = aws_route_table.app_route_tables[count.index].id
    subnet_id       = aws_subnet.app_subnets[count.index].id
}

output "subnet_ids" {
    value = aws_subnet.app_subnets[*].id
}

output "availability_zones" {
    value = data.aws_availability_zones.availability_zones
}

#######################
##
### EKS Cluster
##
#######################

resource "aws_eks_cluster" "bchain_cluster" {
    name        = "bchain-cluster"
    role_arn    = aws_iam_role.eks_cluster_role.arn
    
    vpc_config  {
        #subnet_ids = data.terraform_remote_state.app_vpc.outputs.subnet_ids
        subnet_ids = [aws_subnet.app_subnets[0].id,aws_subnet.app_subnets[1].id,aws_subnet.app_subnets[2].id] #data.terraform_remote_state.vpc_main.outputs.subnet_ids
    }
}

resource "aws_iam_role" "eks_cluster_role" {
    name = "eks-cluster-role"

    assume_role_policy = <<POLICY
{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "eks.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    POLICY
}

resource "aws_iam_role_policy_attachment" "AmazonEKSClusterPolicy" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
    role        = aws_iam_role.eks_cluster_role.name
}

resource "aws_iam_role_policy_attachment" "AmazonEKSServicePolicy" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSServicePolicy"
    role        = aws_iam_role.eks_cluster_role.name
}


#######################
##
### EKS Worker Node Group
##
#######################


resource "aws_eks_node_group" "bchain_node_group" {
    cluster_name    = "bchain-cluster"
    node_group_name = "bchain-node-group"
    node_role_arn   = aws_iam_role.eks_worker_node_group_role.arn
    subnet_ids      = [aws_subnet.app_subnets[0].id,aws_subnet.app_subnets[1].id,aws_subnet.app_subnets[2].id] #data.terraform_remote_state.app_network.outputs.subnet_ids

    scaling_config {
        desired_size    = 2
        max_size        = 2
        min_size        = 2
    }
}

resource "aws_iam_role" "eks_worker_node_group_role" {
    name = "eks_worker_node_group_role"

    assume_role_policy = jsonencode({
        Statement = [
            {
                Action = "sts:AssumeRole",
                Effect = "Allow",
                Principal = {
                    Service = "ec2.amazonaws.com"
                }
            }
        ]
        Version = "2012-10-17"
    })
}

resource "aws_iam_role_policy_attachment" "AmazonEKSWorkerNodePolicy" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
    role        = aws_iam_role.eks_worker_node_group_role.name
}

resource "aws_iam_role_policy_attachment" "AmazonEKS_CNI_Policy" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
    role        = aws_iam_role.eks_worker_node_group_role.name
}

resource "aws_iam_role_policy_attachment" "AmazonEC2ContainerRegistryReadOnly" {
    policy_arn  = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
    role        = aws_iam_role.eks_worker_node_group_role.name
}
