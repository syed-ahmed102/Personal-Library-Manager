import streamlit as st
import json
import os

LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as f:
            return json.load(f)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as f:
        json.dump(library, f, indent=4)

# Display a single book
def display_book(book):
    st.write(f"**Title:** {book['Title']}")
    st.write(f"**Author:** {book['Author']}")
    st.write(f"**Year:** {book['Year']}")
    st.write(f"**Genre:** {book['Genre']}")
    st.write(f"**Read:** {'✅ Yes' if book['Read'] else '❌ No'}")
    st.markdown("---")

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Sidebar menu
menu = st.sidebar.selectbox("Menu", [
    "Add a Book",
    "Remove a Book",
    "Search for a Book",
    "Display All Books",
    "Display Statistics",
    "Exit"
])

st.title("📚 Personal Library Manager")

# --- Menu Actions ---
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=3000, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read it?")
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            new_book = {
                "Title": title,
                "Author": author,
                "Year": int(year),
                "Genre": genre,
                "Read": read
            }
            st.session_state.library.append(new_book)
            save_library(st.session_state.library)
            st.success("Book added successfully!")

elif menu == "Remove a Book":
    st.subheader("❌ Remove a Book")
    titles = [book["Title"] for book in st.session_state.library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove"):
            st.session_state.library = [
                book for book in st.session_state.library if book["Title"] != book_to_remove
            ]
            save_library(st.session_state.library)
            st.success(f"'{book_to_remove}' removed from the library.")
    else:
        st.info("Library is empty.")

elif menu == "Search for a Book":
    st.subheader("🔍 Search for a Book")
    keyword = st.text_input("Enter title or author to search:")
    if keyword:
        found = False
        for book in st.session_state.library:
            if keyword.lower() in book["Title"].lower() or keyword.lower() in book["Author"].lower():
                display_book(book)
                found = True
        if not found:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.subheader("📖 All Books in Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            display_book(book)
    else:
        st.info("No books found in the library.")

elif menu == "Display Statistics":
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
    read_count = sum(book["Read"] for book in st.session_state.library)
    if total == 0:
        st.info("No books to show statistics.")
    else:
        st.write(f"**Total books:** {total}")
        st.write(f"**Books read:** {read_count}")
        st.write(f"**Percentage read:** {read_count / total * 100:.2f}%")

elif menu == "Exit":
    st.balloons()
    st.success("Goodbye! Your library has been saved.")
