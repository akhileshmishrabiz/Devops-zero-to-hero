# Docker composes to run a web application with Flask and Postgres.

In this example, we will run a multi-container web application using Flask and Postgres.

- The first container will be running a Postgres database

- The second container will run the Flask-based web application to talk to the database container.


I have gone through the complete deployment in my blog post:

https://medium.com/@akhilesh-mishra/devops-zero-to-hero-5-docker-compose-to-run-multi-container-docker-applications-f8e51db47f22


# Install docker-compose on Amazon Linux2 

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
