import requests
import io
from random import randint

BASE_URL = "http://localhost:8000/api/v1/books"

def test_create_book_successfully():
    print("\n--- Test Start: Book Creation ---")

    # 1. Arrange: Prepare unique data
    unique_id = randint(1, 10000)
    book_name = f"My E2E Book N{unique_id}"
    file_name = f"book_{unique_id}.txt"  # <--- KEY CHANGE

    book_data = {
        "name": book_name,
        "author": "The Tester",
        "date_published": "2025-07-11",
        "genre": "Testing"
    }

    file_content = b"This is the content of a uniquely named test book."
    files_to_upload = {
        'file': (file_name, io.BytesIO(file_content), 'text/plain')
    }

    print(f"Sending POST request to {BASE_URL}/ with the following data:")
    print(f"  Form data: {book_data}")
    print(f"  File: {files_to_upload['file'][0]}")

    # 2. Act: Send request
    response = requests.post(BASE_URL + "/", data=book_data, files=files_to_upload)

    # 3. Assert: Check response
    print(f"Response received. Status code: {response.status_code}")

    assert response.status_code == 201, f"Error! Server responded with code {response.status_code}. Response body: {response.text}"

    created_book = response.json()
    print("Server response (JSON):", created_book)

    assert created_book["name"] == book_data["name"]
    assert "id" in created_book

    print("--- Test passed successfully! ---")

def test_creation_and_download_workflow():
    """
    Tests the creation of a book, verifies its presence in the list, and confirms download functionality.
    """
    # --- Step 1: Create a unique book ---
    print("\n--- Step 1: Creating a unique book ---")
    unique_id = randint(1, 10000)
    book_name = f"Lifecycle Test Book N{unique_id}"
    file_name = f"lifecycle_{unique_id}.txt"
    file_content = f"Content of book {unique_id}".encode('utf-8')

    book_data = {
        "name": book_name, "author": "Workflow Tester", "date_published": "2025-01-15", "genre": "E2E"
    }
    files_to_upload = {'file': (file_name, io.BytesIO(file_content), 'text/plain')}

    create_response = requests.post(BASE_URL + "/", data=book_data, files=files_to_upload)
    assert create_response.status_code == 201, f"Failed to create book: {create_response.text}"
    created_book = create_response.json()
    book_id = created_book["id"]
    print(f"Book '{book_name}' successfully created with ID: {book_id}")

    # --- Step 2: Check the book is listed ---
    print("\n--- Step 2: Verifying presence in the list ---")
    get_all_response = requests.get(BASE_URL + "/")
    assert get_all_response.status_code == 200
    all_books = get_all_response.json()
    # Check that the created book is in the list by ID
    assert any(book['id'] == book_id for book in all_books), f"Created book with ID {book_id} not found in list"
    print("Book successfully found in the list.")

    # --- Step 3: Download the file of the created book ---
    print("\n--- Step 3: Verifying file download ---")
    download_response = requests.get(f"{BASE_URL}/{book_id}/download")
    assert download_response.status_code == 200
    assert download_response.content == file_content
    print("Book file successfully downloaded and content matches.")

    print("\n--- Full lifecycle test (create and download) passed successfully! ---")
