# Backend with flask
locally running db(postgres) container



# Front end with react
Add below to flask app before going forward
To use this frontend, you'll need to:

Make sure your Flask backend is running on port 5000
Enable CORS on your Flask backend by adding:


from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # Add this line after creating the Flask app

Install dependencies

pip install flask-cors  # For backend

Why we need cors

CORS (Cross-Origin Resource Sharing) is needed because of the browser's Same-Origin Policy, which is a critical security feature. Let me explain step by step:

In our current setup:

Frontend is running on http://localhost:3000 (React's default port)

Backend is running on http://localhost:5000 (Flask's default port)

Even though both are on 'localhost', they're considered different origins because of different ports


The Same-Origin Policy:

By default, browsers block web pages from making requests to a different domain/origin

This protects users from malicious websites trying to access APIs on other domains

Without CORS, our frontend couldn't make API calls to our backend

We're telling the server to add specific headers to its responses:

- Access-Control-Allow-Origin: * (allows requests from any origin)

- Access-Control-Allow-Methods: GET, POST, PUT, DELETE

- Access-Control-Allow-Headers: Content-Type



# -> In production 

You typically want to restrict CORS to specific origins rather than using *

You can configure it like this:

CORS(app, origins=['https://your-frontend-domain.com'])


