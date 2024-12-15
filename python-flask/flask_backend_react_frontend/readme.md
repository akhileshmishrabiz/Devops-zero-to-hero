# Backend with flask

## locally running db(postgres) container

docker run --name flask_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=postgres -p 5432:5432 -d postgres

pip install -r requirements.txt

####################################

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



###################################

# Front end with react

-> First, create a new React project using Create React App:

npx create-react-app book-management-frontend

cd book-management-frontend

-> Install the required dependencies:

npm install lucide-react   # For icons

npm install @/components/ui/alert  # For UI components

npm install tailwindcss postcss autoprefixer  # For styling

-> Set up Tailwind CSS:

npx tailwindcss init -p

-> Configure Tailwind CSS by updating tailwind.config.js:

module.exports = {
  content: [

    "./src/**/*.{js,jsx,ts,tsx}",
  ],

  theme: {

    extend: {},

  },

  plugins: [],
}


-> Add Tailwind directives to src/index.css:

@tailwind base;

@tailwind components;

@tailwind utilities;

-> Replace the contents of src/App.js with:

import BookManagement from './components/BookManagement';

function App() {
  return (
    <div className="App">
      <BookManagement />
    </div>
  );
}

export default App;


-> Start the development server:

npm start

book-management-frontend/
├── node_modules/
├── public/
├── src/
│   ├── components/
│   │   └── BookManagement.jsx
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
└── tailwind.config.js