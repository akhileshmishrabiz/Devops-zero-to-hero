from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# postgresql://<user>:<password>@<end point>:5432/<database name>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/mydatabase'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return '<User %r>' % self.username

def create_table():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_data = Data(name=name)
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        data = Data.query.all()
        return render_template('index.html', data=data)

if __name__ == '__main__':
    create_table()
    print("Table created successfully.")
    app.run(host='0.0.0.0', debug=True)
