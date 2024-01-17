#!/bin/bash
sudo yum update -y
sudo yum install awscli -y
echo "setup.sh script ran " > /tmp/log.txt