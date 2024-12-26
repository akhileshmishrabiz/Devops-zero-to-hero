## Blog post

[https://medium.com/gitconnected/a-beginners-guide-to-rest-apis-build-your-first-crud-app-31b4cfacf128]

# -> Write a simple flask app using crud. for tsting it will use a postgres container running locally.
docker run --name flask_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -p 5432:5432 -d postgres
-> build the DB URI that flask app will use to connect 

# SQLALCHEMY_DATABASE_URI = f'postgresql://{postgres_username}:{postgres_password}@{db_host}:{db_port}/{db_name}'

mkdir app.py requirements.txt 
requirements.txt -> dependencies here
app.py -> flask app code here. 
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/postgres'

Install the dependencies  and copy the code to app.py

1. make a post request to the app.
curl -X POST http://127.0.0.1:5000/books \
-H "Content-Type: application/json" \
-d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 9.99}'

curl -X POST http://127.0.0.1:5000/books \
-H "Content-Type: application/json" \
-d '{ "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 11.99 }'


2. List all the books
curl http://127.0.0.1:5000/books

3. List specfic book
curl http://127.0.0.1:5000/books/1

4. update the book entry
curl -X PUT http://127.0.0.1:5000/books/1 \
-H "Content-Type: application/json" \
-d '{"price": 14.99}'

5. Delete
curl -X DELETE http://127.0.0.1:5000/books/3

6. bulk create
curl -X POST http://127.0.0.1:5000/books/bulk \
-H "Content-Type: application/json" \
-d '[
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "price": 9.99
  },
  {
    "title": "1984",
    "author": "George Orwell",
    "price": 12.99
  },
  {
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "price": 11.99
  }
]'

7. Bulk update
curl -X PUT http://127.0.0.1:5000/books/bulk-update \
-H "Content-Type: application/json" \
-d '[
  {
    "id": 5,
    "price": 14.99
  },
  {
    "id": 6,
    "price": 15.99,
    "author": "George Orwell (Updated)"
  }
]'
