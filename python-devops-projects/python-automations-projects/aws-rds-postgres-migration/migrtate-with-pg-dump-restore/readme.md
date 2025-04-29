# RDS Database Configuration Script
This script provides functionalities to manage Amazon RDS (Relational Database Service) instances, including tasks such as migrating databases, evaluating database status, and performing various administrative actions.

Features
Database Migration: The script can clone an existing RDS database instance with a new storage size, restore data to the new instance, and swap the old and new instances to ensure a seamless transition.

Database Evaluation: It can provide information about the storage usage and availability of an RDS instance.

Prerequisites
Python 3.x

AWS CLI configured with necessary permissions

Required Python packages installed (listed in requirements.txt)

apt install python3-pip  # install pip

sudo apt  install awscli -y # install aws cli

# Installation
Clone the repository to your local machine:

git clone https://github.com/akhileshmishrabiz/rds-migration.git

cd migrtate-with-pg-dump-restore

# Install the required Python packages:
pip install -r requirements.txt

Configure AWS CLI with appropriate credentials and permissions.

Usage
Running the Script

To run the script, execute main.py with the desired action and arguments. Available actions are:

migrate: Migrate an RDS database with a new storage size.

evaluate: Evaluate the status of an RDS database.

# Example usage:

python main.py migrate my-rds-instance-name 100  # Migrate 'my-rds-instance-name' with a new storage size of 100GB

python main.py evaluate my-rds-instance-name     # Evaluate the status of 'my-rds-instance-name'

# Script Arguments
action: Specify the action to perform. Choose between migrate or evaluate.

dbname: Name of the RDS database instance.

size: (Only for migrate action) New storage size for the RDS database.

Environment Variables

DEBUG: Set to true to enable debug mode for more detailed logging.


# testing requirements 

Run this cli from an EC2 instance running on same VPC as your RDS inatcnes.

This Script is tested with RDS instacne with postgres db v.16 and higher. I used EC2 with ubuntu latest image to test this.

I have used postgres utilities pg_dump, and pg_restore to backup and restore the databases

# Use below commands to install dependencies.

sudo apt-get update

sudo apt-get install wget ca-certificates

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

sudo apt-get install postgresql-client -y

pg_dump --version

psql --version





