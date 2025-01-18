export DATABASE_URL='localhost'


# run db locally
docker run --name flask_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -p 5432:5432 -d postgres