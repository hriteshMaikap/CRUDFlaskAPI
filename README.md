# Planetary CRUD API

A Flask based CRUD API for managing planets and users using Flask, SQLAlchemy, and JWT authentication.

## Features
- User Registration, Login, and Password Recovery
- JWT-based Authentication
- CRUD operations for Planets
- Modular and Scalable Code Structure
- Email Integration with Flask-Mail

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/planetary-crud-api.git
    cd planetary-crud-api
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Initialize the database:
    ```bash
    flask db_create
    flask db_seed
    ```

5. Run the application:
    ```bash
    python run.py
    ```

## API Endpoints

### Users
- `POST /api/users/register`: Register a new user.
- `POST /api/users/login`: Authenticate user and return JWT.
- `GET /api/users/forgot_password/<email>`: Send the user's password via email.

### Planets
- `GET /api/planets/`: Retrieve all planets.
- `GET /api/planets/<planet_id>`: Retrieve details of a specific planet.
- `POST /api/planets/`: Add a new planet (requires JWT).
- `PUT /api/planets/<planet_id>`: Update an existing planet (requires JWT).
- `DELETE /api/planets/<planet_id>`: Delete a planet (requires JWT).

