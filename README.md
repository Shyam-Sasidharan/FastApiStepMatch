# FastAPI Login API

## Development setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update the database credentials:

```powershell
Copy-Item .env.example .env
```

The MySQL connection value uses this format:

```text
mysql+pymysql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```

For a default local XAMPP installation with the database `fastapi_db`:

```env
FASTAPI_DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/fastapi_db
```

Change `fastapi_db` to the database selected in phpMyAdmin. If the MySQL
account has a password, place it after `root:`. URL-encode special characters
in usernames and passwords.

Start the development server:

```powershell
uvicorn app.main:app --reload
```

Open the API documentation at `http://127.0.0.1:8000/docs`.

Verify the database connection at:

```text
http://127.0.0.1:8000/api/v1/health/database
```

A successful connection returns:

```json
{"status": "ok", "database": "connected"}
```

## Authentication

Log in with an email address or username:

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "Password@123"
}
```

Send the returned access token to protected endpoints:

```http
GET /api/v1/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The access token expires after the number of minutes configured by
`FASTAPI_ACCESS_TOKEN_EXPIRE_MINUTES`.

Run tests:

```powershell
pytest
```
