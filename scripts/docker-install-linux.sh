#!/bin/bash
sudo apt-get update
sudo apt install curl -y
curl https://get.docker.com | sudo bash && sudo usermod -aG docker $(whoami)
docker --version