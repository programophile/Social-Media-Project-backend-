# FastAPI Course Project

A FastAPI application for managing users, posts, and post votes. The project uses PostgreSQL for persistence, SQLAlchemy for database access, Alembic for migrations, and JWT bearer tokens for authentication.

## Features

- User registration and lookup
- JWT-based login and protected routes
- Create, list, search, update, and delete posts
- Add and remove votes on posts
- PostgreSQL database integration
- Alembic database migrations
- Pytest tests for the calculation and bank account examples

## Project Structure

```text
app/
  main.py              FastAPI application entry point
  config.py            Environment-based application settings
  database.py          SQLAlchemy engine and database session
  models.py            Database models
  schemas.py           Pydantic request and response schemas
  utils.py             Password hashing and verification helpers
  routers/             Authentication, user, post, and vote routes
alembic/               Database migration configuration and revisions
test/                  Pytest tests
Dockerfile             FastAPI container image definition
docker-compose-dev.yml Local development stack
docker-compose-prod.yml Production-oriented stack
```

## Requirements

- Python 3.11 or newer
- PostgreSQL 15 or newer
- Docker and Docker Compose are optional for containerized development

## Configuration

Create a `.env` file in the project root with the following values:

```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your-postgres-password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_TIME=30
```

Do not commit real passwords or secret keys. `ACCESS_TOKEN_EXPIRE_TIME` is measured in minutes.

## Local Development

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start PostgreSQL and create the configured database, then apply the migrations:

```powershell
alembic upgrade head
```

Start the API from the project root:

```powershell
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`.

## Docker Development

The development Compose file starts both the FastAPI service and PostgreSQL:

```powershell
docker compose -f docker-compose-dev.yml up --build
```

The API is available at `http://localhost:8000`. To stop the services:

```powershell
docker compose -f docker-compose-dev.yml down
```

The PostgreSQL data is stored in the `postgres_data` Docker volume. Run migrations from the application container when needed:

```powershell
docker compose -f docker-compose-dev.yml exec fastapi alembic upgrade head
```

## Database Migrations

Create a migration after changing the SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe the change"
```

Apply migrations:

```powershell
alembic upgrade head
```

Rollback the latest migration:

```powershell
alembic downgrade -1
```

## API Documentation

With the server running, FastAPI provides interactive documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

| Method   | Path          | Authentication | Description                |
| -------- | ------------- | -------------- | -------------------------- |
| `GET`    | `/`           | No             | Health-style root response |
| `POST`   | `/users/`     | No             | Create a user              |
| `GET`    | `/users/{id}` | No             | Get a user                 |
| `POST`   | `/login`      | No             | Obtain a JWT access token  |
| `GET`    | `/posts/`     | Bearer token   | List and search posts      |
| `POST`   | `/posts/`     | Bearer token   | Create a post              |
| `GET`    | `/posts/{id}` | Bearer token   | Get a post and vote count  |
| `PUT`    | `/posts/{id}` | Bearer token   | Update an owned post       |
| `DELETE` | `/posts/{id}` | Bearer token   | Delete an owned post       |
| `POST`   | `/vote/`      | Bearer token   | Add or remove a post vote  |

For `/login`, send form data using `username` for the user's email and `password` for the user's password. Use the returned token in subsequent requests:

```text
Authorization: Bearer <access_token>
```

## Running Tests

Run the test suite from the project root:

```powershell
pytest -v
```

## Production Compose

The production Compose file uses the published `programophile/fastapi:latest` image and reads its settings from environment variables. Set the required variables before starting it:

```powershell
docker compose -f docker-compose-prod.yml up -d
```

Review the production Compose configuration before deployment and provide production-grade database credentials and JWT secrets.
