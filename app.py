from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create and connect to SQLite database (it will be created if it doesn't exist)
def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  author TEXT, 
                  title TEXT, 
                  lessons TEXT)''')
    conn.commit()
    conn.close()

# Function to get all books from the database
def get_books():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books ORDER BY id ASC')  # Ordering by ID (ascending)
    books = c.fetchall()
    conn.close()
    return books

# Function to add a book to the database
def add_book_to_db(author, title, lessons):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (author, title, lessons) VALUES (?, ?, ?)', 
              (author, title, lessons))
    conn.commit()
    conn.close()

# Function to delete a book from the database
def delete_book_from_db(book_id):
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        lessons = request.form['lessons']
        
        # Add the book to the database
        add_book_to_db(author, title, lessons)
        
        # After the book is added, redirect to the 'book_entries' page
        return redirect(url_for('book_entries'))
    
    return render_template('add_book.html')

@app.route('/book_entries')
def book_entries():
    books = get_books()  # Get all books to display them
    return render_template('book_entries.html', books=books)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    # Delete the book from the database
    delete_book_from_db(book_id)
    return redirect(url_for('book_entries'))  # Redirect back to the book entries page

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
