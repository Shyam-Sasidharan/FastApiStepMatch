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

Start the development server:

```powershell
uvicorn app.main:app --reload
```

Open the API documentation at `http://127.0.0.1:8000/docs`.

Run tests:

```powershell
pytest
```
