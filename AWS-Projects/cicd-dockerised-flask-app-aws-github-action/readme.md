#### Deploy a dockerized Flask app on AWS Using Github Action

We will deploy the dockerized Flask application on AWS EC2 with GitHub Actions. We will follow the Devops core principle — CICD(continuous integration and continuous deployment) to build and deploy the application on every code change.

Whenever we change the Python code, its dependencies, or Dockerfile, GitHub Action workflow will build a new Docker image, push it to AWS ECR, and deploy a new version of the Docker container that we can access using EC2 instances public IP on port 80.


I have discussed all the details about this project in my blog post on Medium.

https://towardsaws.com/continuously-build-deploy-python-web-app-on-aws-with-github-action-a9de1421898c

