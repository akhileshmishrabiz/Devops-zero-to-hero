import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, X, Check } from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const BookManagement = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingBookId, setEditingBookId] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    price: ''
  });

  // Fetch books
  const fetchBooks = async () => {
    try {
      const response = await fetch('http://localhost:5000/books');
      if (!response.ok) throw new Error('Failed to fetch books');
      const data = await response.json();
      setBooks(data);
      setError(null);
    } catch (err) {
      setError('Failed to load books. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  // Add new book
  const handleAddBook = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          price: parseFloat(formData.price)
        }),
      });
      
      if (!response.ok) throw new Error('Failed to add book');
      
      await fetchBooks();
      setShowAddForm(false);
      setFormData({ title: '', author: '', price: '' });
    } catch (err) {
      setError('Failed to add book. Please try again.');
    }
  };

  // Update book
  const handleUpdateBook = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/books/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          price: parseFloat(formData.price)
        }),
      });
      
      if (!response.ok) throw new Error('Failed to update book');
      
      await fetchBooks();
      setEditingBookId(null);
      setFormData({ title: '', author: '', price: '' });
    } catch (err) {
      setError('Failed to update book. Please try again.');
    }
  };

  // Delete book
  const handleDeleteBook = async (id) => {
    if (!window.confirm('Are you sure you want to delete this book?')) return;
    
    try {
      const response = await fetch(`http://localhost:5000/books/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) throw new Error('Failed to delete book');
      
      await fetchBooks();
    } catch (err) {
      setError('Failed to delete book. Please try again.');
    }
  };

  const startEditing = (book) => {
    setEditingBookId(book.id);
    setFormData({
      title: book.title,
      author: book.author,
      price: book.price.toString()
    });
  };

  if (loading) return <div className="flex justify-center p-8">Loading books...</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Book Management System</h1>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          <Plus size={20} /> Add Book
        </button>
      </div>

      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Add Book Form */}
      {showAddForm && (
        <div className="mb-6 p-4 border rounded-lg bg-gray-50">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Add New Book</h2>
            <button onClick={() => setShowAddForm(false)} className="text-gray-500 hover:text-gray-700">
              <X size={20} />
            </button>
          </div>
          <form onSubmit={handleAddBook} className="space-y-4">
            <input
              type="text"
              placeholder="Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="text"
              placeholder="Author"
              value={formData.author}
              onChange={(e) => setFormData({ ...formData, author: e.target.value })}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="number"
              placeholder="Price"
              value={formData.price}
              onChange={(e) => setFormData({ ...formData, price: e.target.value })}
              className="w-full p-2 border rounded"
              required
              step="0.01"
              min="0"
            />
            <button type="submit" className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600">
              Add Book
            </button>
          </form>
        </div>
      )}

      {/* Books Table */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse table-auto">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2 text-left">Title</th>
              <th className="border p-2 text-left">Author</th>
              <th className="border p-2 text-left">Price</th>
              <th className="border p-2 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book.id} className="hover:bg-gray-50">
                <td className="border p-2">
                  {editingBookId === book.id ? (
                    <input
                      type="text"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      className="w-full p-1 border rounded"
                    />
                  ) : (
                    book.title
                  )}
                </td>
                <td className="border p-2">
                  {editingBookId === book.id ? (
                    <input
                      type="text"
                      value={formData.author}
                      onChange={(e) => setFormData({ ...formData, author: e.target.value })}
                      className="w-full p-1 border rounded"
                    />
                  ) : (
                    book.author
                  )}
                </td>
                <td className="border p-2">
                  {editingBookId === book.id ? (
                    <input
                      type="number"
                      value={formData.price}
                      onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                      className="w-full p-1 border rounded"
                      step="0.01"
                      min="0"
                    />
                  ) : (
                    `$${book.price.toFixed(2)}`
                  )}
                </td>
                <td className="border p-2">
                  <div className="flex justify-center gap-2">
                    {editingBookId === book.id ? (
                      <>
                        <button
                          onClick={() => handleUpdateBook(book.id)}
                          className="p-1 text-green-600 hover:text-green-800"
                        >
                          <Check size={20} />
                        </button>
                        <button
                          onClick={() => {
                            setEditingBookId(null);
                            setFormData({ title: '', author: '', price: '' });
                          }}
                          className="p-1 text-gray-600 hover:text-gray-800"
                        >
                          <X size={20} />
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          onClick={() => startEditing(book)}
                          className="p-1 text-blue-600 hover:text-blue-800"
                        >
                          <Edit2 size={20} />
                        </button>
                        <button
                          onClick={() => handleDeleteBook(book.id)}
                          className="p-1 text-red-600 hover:text-red-800"
                        >
                          <Trash2 size={20} />
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BookManagement;
