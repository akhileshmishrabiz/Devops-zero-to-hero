from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_docker():
    return 'Hello, World today is sat - this is second run at 7 pm and this is automated third code change'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')