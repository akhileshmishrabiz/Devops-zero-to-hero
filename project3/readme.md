
We will use github actions to deploy a docker based application on aws ec2  machine.
We will use aws ecr repo to store docker images.
github action workflow will have 2 jobs
  job1: build the image with each commit, and push the image to ecr
  job2: will pull the lastes docker image to ec2 and create a new instance of docker app and remove the old docker.
