import streamlit as st
import sqlite3

# Database Setup
def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')
    conn.commit()
    conn.close()

# Insert Book
def add_book(title, author, year):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    conn.close()

# Fetch Books
def get_books():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

# Delete Book
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

# Custom CSS
def apply_custom_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Arial', sans-serif;
            }
            .stTextInput, .stNumberInput, .stButton {
                border-radius: 10px;
                border: 2px solid #4CAF50;
                padding: 10px;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                padding: 10px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Streamlit UI
st.title("📚 Personal Library Manager")
apply_custom_css()
init_db()

# Input Fields
title = st.text_input("Book Title")
author = st.text_input("Author")
year = st.number_input("Year", min_value=1000, max_value=2100, step=1)

if st.button("Add Book"):
    if title and author and year:
        add_book(title, author, year)
        st.success(f"'{title}' added to library!")
    else:
        st.error("Please fill all fields")

# Display Books
st.subheader("📖 Library Collection")
books = get_books()
if books:
    for book in books:
        st.write(f"**{book[1]}** by {book[2]} ({book[3]})")
        if st.button(f"Delete {book[1]}", key=book[0]):
            delete_book(book[0])
            st.experimental_rerun()
else:
    st.info("No books added yet.")
