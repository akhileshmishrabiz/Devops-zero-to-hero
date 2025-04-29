# Devops learning platform with React, Flask and postgres

Frontend: React

Backend: Flask

Database: Postgres


## Build and start the containers( given docker and docker-compose are instaled)

docker-compose up --build

## Initialize the database (first time only) In a new terminal

docker-compose exec backend flask db upgrade

docker-compose exec backend python seed_data.py

## Stop the application:

docker-compose down

## start the application 

docker-compose down

route53-policy.json



Akhilesh-cluster

