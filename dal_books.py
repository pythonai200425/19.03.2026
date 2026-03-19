import sqlite3

DB_NAME = "books.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

def insert_famous_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    books = [
        ("The Hobbit", "J.R.R. Tolkien", "English", 49.9, 1937),
        ("1984", "George Orwell", "English", 39.9, 1949),
        ("To Kill a Mockingbird", "Harper Lee", "English", 44.9, 1960),
        ("Pride and Prejudice", "Jane Austen", "English", 34.9, 1813),
        ("The Great Gatsby", "F. Scott Fitzgerald", "English", 42.0, 1925),
        ("Moby Dick", "Herman Melville", "English", 45.5, 1851),
        ("War and Peace", "Leo Tolstoy", "Russian", 59.9, 1869),
        ("Crime and Punishment", "Fyodor Dostoevsky", "Russian", 48.0, 1866),
        ("The Catcher in the Rye", "J.D. Salinger", "English", 37.5, 1951),
        ("The Alchemist", "Paulo Coelho", "Portuguese", 41.0, 1988),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "English", 55.0, 1997),
        ("The Lord of the Rings", "J.R.R. Tolkien", "English", 79.9, 1954),
        ("The Da Vinci Code", "Dan Brown", "English", 46.0, 2003),
        ("The Little Prince", "Antoine de Saint-Exupéry", "French", 29.9, 1943),
        ("Don Quixote", "Miguel de Cervantes", "Spanish", 52.0, 1605),
    ]

    query = """
    INSERT INTO books (title, author, language, price, published_year)
    VALUES (?, ?, ?, ?, ?)
    """

    cursor.executemany(query, books)

    conn.commit()
    conn.close()

    print("✅ 15 books inserted successfully!")

def create_table_books():
    query = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        language TEXT,
        price REAL NOT NULL CHECK(price >= 0),
        published_year INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    with get_connection() as conn:
        conn.execute(query)

    insert_famous_books()


def drop_table_books():
    with get_connection() as conn:
        conn.execute("DROP TABLE IF EXISTS books")


def recreate_table_books():
    drop_table_books()
    create_table_books()


def insert_book(title, author, language, price, published_year):
    query = """
    INSERT INTO books (title, author, language, price, published_year)
    VALUES (?, ?, ?, ?, ?)
    """
    with get_connection() as conn:
        cursor = conn.execute(
            query,
            (title, author, language, price, published_year)
        )
        book_id = cursor.lastrowid
    return get_book_by_id(book_id)


def get_all_books():
    query = """
    SELECT id, title, author, language, price, published_year, created_at
    FROM books
    ORDER BY id
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    return [row_to_dict(row) for row in rows]


def get_book_by_id(book_id):
    query = """
    SELECT id, title, author, language, price, published_year, created_at
    FROM books
    WHERE id = ?
    """
    with get_connection() as conn:
        row = conn.execute(query, (book_id,)).fetchone()
    return row_to_dict(row)


def update_book(book_id, title, author, language, price, published_year):
    query = """
    UPDATE books
    SET title = ?,
        author = ?,
        language = ?,
        price = ?,
        published_year = ?
    WHERE id = ?
    """
    with get_connection() as conn:
        cursor = conn.execute(
            query,
            (title, author, language, price, published_year, book_id)
        )
        affected_rows = cursor.rowcount

    if affected_rows == 0:
        return None

    return get_book_by_id(book_id)


def delete_book(book_id):
    existing_book = get_book_by_id(book_id)
    if existing_book is None:
        return None

    with get_connection() as conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))

    return existing_book