# Resort POS API

A FastAPI-based Point of Sale (POS) backend for a resort environment.

The system currently supports:

* User authentication
* JWT-based authentication
* Product management
* Category management
* Customer management
* Sales processing
* Room charges
* Stock management
* Sales validation
* Automated testing with Pytest
* SQLite database for isolated tests
* Continuous Integration with GitHub Actions

## Project Structure

```text
resort-pos/
├── app/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_sales.py
│   ├── test_sales_atomicity.py
│   ├── test_sales_multiple_items.py
│   └── test_room_charge.py
├── .github/
│   └── workflows/
├── requirements.txt
└── README.md
```

## Running the Application

Activate the virtual environment:

```bash
source env/bin/activate
```

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Running the Tests

The project uses **Pytest** and an isolated **SQLite test database** so that tests do not use the normal development database.

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the complete test suite:

```bash
pytest -v
```

The tests cover important application functionality including:

* Authentication
* Successful sales
* Multiple-item sales
* Room charges
* Customer-related sales
* Missing products
* Insufficient stock
* Atomicity of multi-item sales
* Validation and failure scenarios

## Test Database

Tests use SQLite independently from the normal application database.

The test database is configured in:

```text
tests/conftest.py
```

This keeps automated tests isolated from the development PostgreSQL database.

## Continuous Integration

GitHub Actions is configured to run the automated test suite when:

* Code is pushed to the repository
* A Pull Request is opened or updated

The workflow:

1. Checks out the repository
2. Sets up Python
3. Installs the dependencies
4. Runs the complete Pytest suite

A failed test causes the GitHub Actions workflow to fail.

## Example Test Result

```text
26 passed
```

## API Health Check

The API provides a health endpoint:

```text
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

## Development

This project is developed using:

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite for automated tests
* PostgreSQL for development
* Pytest

