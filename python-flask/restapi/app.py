# Rest api blog: https://medium.com/@akhilesh-mishra/a-beginners-guide-to-rest-apis-build-your-first-crud-app-31b4cfacf128
# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Our Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Create the database tables
with app.app_context():
    db.create_all()
# base route
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# CREATE - Add a new book
@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['title', 'author', 'price']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_book = Book(
            title=data['title'],
            author=data['author'],
            price=data['price']
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book created successfully',
            'book': new_book.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# READ - Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# READ - Get a specific book
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())

# UPDATE - Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'price' in data:
            book.price = data['price']
            
        db.session.commit()
        return jsonify({
            'message': 'Book updated successfully',
            'book': book.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# DELETE - Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Add this to your existing app.py

# Bulk Create - Add multiple books
@app.route('/books/bulk', methods=['POST'])
def create_multiple_books():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of books'}), 400
        
        created_books = []
        
        for book_data in data:
            # Validate each book
            if not all(key in book_data for key in ['title', 'author', 'price']):
                return jsonify({'error': f'Missing required fields in book: {book_data}'}), 400
            
            new_book = Book(
                title=book_data['title'],
                author=book_data['author'],
                price=book_data['price']
            )
            
            db.session.add(new_book)
            created_books.append(new_book)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully created {len(created_books)} books',
            'books': [book.to_dict() for book in created_books]
        }), 201
        
    except Exception as e:
        db.session.rollback()  # Rollback on error
        return jsonify({'error': str(e)}), 400

# Bulk Update - Update multiple books
@app.route('/books/bulk-update', methods=['PUT'])
def update_multiple_books():
    try:
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({'error': 'Expected a list of book updates'}), 400
        
        updated_books = []
        
        for book_update in data:
            if 'id' not in book_update:
                return jsonify({'error': 'Each book update must include an id'}), 400
                
            book = Book.query.get(book_update['id'])
            if not book:
                return jsonify({'error': f'Book not found with id: {book_update["id"]}'}), 404
            
            # Update fields if provided
            if 'title' in book_update:
                book.title = book_update['title']
            if 'author' in book_update:
                book.author = book_update['author']
            if 'price' in book_update:
                book.price = book_update['price']
                
            updated_books.append(book)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully updated {len(updated_books)} books',
            'books': [book.to_dict() for book in updated_books]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)