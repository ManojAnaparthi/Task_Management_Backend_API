# Task Management System - Backend API

A production-ready FastAPI backend with JWT authentication, refresh token rotation, and role-based access control.

## Features

- ✅ User registration and authentication
- ✅ JWT access & refresh tokens with rotation
- ✅ Secure token storage and revocation
- ✅ Role-based authorization (user/admin)
- ✅ Protected CRUD operations for tasks
- ✅ Pagination and filtering
- ✅ PostgreSQL database with Alembic migrations

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 12+

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update:
   - `DATABASE_URL` - Your PostgreSQL connection string
   - `SECRET_KEY` - Generate with: `openssl rand -hex 32`

5. Create the database:
   ```bash
   python create_db.py
   ```

6. Run migrations:
   ```bash
   alembic upgrade head
   ```

7. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Revoke refresh token

### Tasks (Protected)
- `GET /tasks` - List tasks (with pagination & filtering)
- `POST /tasks` - Create task
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Query Parameters
- `limit` (1-100) - Results per page
- `offset` (0+) - Skip results
- `status` (todo/in_progress/done) - Filter by status

## Security

- Passwords hashed with bcrypt
- JWT tokens with expiration
- Refresh token rotation (prevents reuse)
- Database-backed token revocation
- Environment-based configuration

## Production Deployment

1. Set strong `SECRET_KEY` in production
2. Use managed PostgreSQL service
3. Enable HTTPS
4. Set appropriate token expiration times
5. Configure CORS if needed
6. Use environment variables for all secrets
7. Never commit `.env` file

## Development

Run tests:
```bash
python test_day4.py  # Task CRUD tests
python test_day5.py  # Auth & token rotation tests
```

## Project Structure

```
app/
├── api/
│   ├── dependencies.py    # Auth dependencies
│   └── routes/           # API endpoints
├── core/
│   ├── config.py         # Settings
│   └── security.py       # Auth utilities
├── db/
│   ├── base.py           # SQLAlchemy base
│   └── session.py        # Database session
├── models/               # Database models
├── schemas/              # Pydantic schemas
├── services/             # Business logic
└── main.py               # FastAPI app
```
