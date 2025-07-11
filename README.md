# Book Service API

A simple and robust RESTful API service built with Python and FastAPI for managing and providing access to literary works. The project is fully containerized using Docker, includes database migrations with Alembic, and has an End-to-End test suite.

## Features

-   **Upload Books**: Upload book files (`.txt`) with associated metadata (name, author, etc.).
-   **List & Filter**: Retrieve a list of all books with powerful filtering capabilities.
-   **Download Books**: Download a book's file by its unique ID.
-   **Denylist Functionality**: Block specific books or authors from being downloaded by uploading a simple `.xlsx` file.
-   **Online Viewer**: A simple server-rendered HTML page to view a book's content directly in the browser.
-   **Containerized**: Fully containerized with Docker and Docker Compose for easy setup and consistent deployment.
-   **Database Migrations**: Uses Alembic to reliably manage database schema changes.
-   **Tested**: Includes an E2E test suite using Pytest to ensure the API works as expected.

## Technology Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **Containerization**: Docker, Docker Compose

## Prerequisites

Before you begin, ensure you have the following installed on your system:
-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to get the application running locally in just a few minutes.

### 1. Clone the Repository

```bash
git clone https://github.com/Mrhetsko/my_book_library.git
cd my_book_library
```

### 2. Build and Run the Application

```bash
docker compose up --build -d
```

## 🛠 Notes

📁 The .env file is included in the repository for demonstration purposes only — it's not recommended to include .env files in production repositories. Typically, it should be added to .gitignore, and a .env.example file should be used as a template instead.
