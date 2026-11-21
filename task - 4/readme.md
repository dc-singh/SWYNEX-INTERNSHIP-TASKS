# Task 4 - Swynex Users API

## Repository
- GitHub repository: https://github.com/dc-singh/SWYNEX-INTERNSHIP-TASKS
- Live service URL: Not deployed yet

## Overview
Task 4 completes the internship Users API as a production-ready FastAPI service. It supports authenticated, permission-based CRUD operations for users and uses an atomic JSON-file data store.

## Features
- REST CRUD endpoints for users
- Read/write permission checks using request headers
- JSON sample data
- Search filtering
- Automatic Swagger UI and ReDoc documentation
- Consistent JSON error responses
- CORS middleware
- Docker and Render deployment support

## Run locally

```powershell
cd "task - 4"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
- API root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication
Send both headers for every `/api/users` request:

```text
X-User-Id: 1
X-User-Name: Nakul
```

Users aged 18 or older have read and write permissions. Younger users have read-only access.

## Sample users
The initial data is in `data/data.json`:

```json
[
  {"id": 1, "name": "Nakul", "age": 21},
  {"id": 2, "name": "John", "age": 25},
  {"id": 3, "name": "Alice", "age": 30},
  {"id": 4, "name": "Bob", "age": 35}
]
```

## API examples

Authenticate:

```bash
curl -X POST http://127.0.0.1:8000/api/authenticate \
  -H "X-User-Id: 1" \
  -H "X-User-Name: Nakul"
```

List users:

```bash
curl "http://127.0.0.1:8000/api/users?search=al" \
  -H "X-User-Id: 1" \
  -H "X-User-Name: Nakul"
```

Create a user:

```bash
curl -X POST http://127.0.0.1:8000/api/users \
  -H "X-User-Id: 1" \
  -H "X-User-Name: Nakul" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Priya\",\"age\":24}"
```

Update a user:

```bash
curl -X PATCH http://127.0.0.1:8000/api/users/1 \
  -H "X-User-Id: 1" \
  -H "X-User-Name: Nakul" \
  -H "Content-Type: application/json" \
  -d "{\"age\":22}"
```

Delete a user:

```bash
curl -X DELETE http://127.0.0.1:8000/api/users/4 \
  -H "X-User-Id: 1" \
  -H "X-User-Name: Nakul"
```

## Docker deployment

```powershell
docker build -t swynex-users-api .
docker run --rm -p 8000:8000 swynex-users-api
```

## Render deployment
1. Push this repository to GitHub.
2. In Render, create a **New > Blueprint** service.
3. Select this repository and accept `task - 4/render.yaml`.
4. Set the service root directory to `task - 4`.
5. Deploy. The API will be available at the Render-generated HTTPS URL.

For an existing writable data store on a hosted platform, set `DATA_FILE` to a mounted persistent JSON-file path.
