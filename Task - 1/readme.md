# Task 1 - FastAPI Starter API

## Internship Context
This project is part of my internship work with Swynex. It represents the first assigned task in the internship, where I was expected to build a basic FastAPI application and understand the fundamentals of backend development using Python.

## Overview
This project is a simple FastAPI application that exposes a basic REST API with a root endpoint and a health-check endpoint. It is designed as a beginner-friendly backend task to demonstrate how to set up and run a FastAPI service in Python.

## Project Objective
The goal of this task is to:
- create a minimal FastAPI application
- expose HTTP endpoints
- verify the application runs successfully
- understand the basic structure of a FastAPI project
- complete the first internship assignment from Swynex

## Tech Stack
- Python
- FastAPI
- Uvicorn

## Project Structure
```text
Task - 1/
├── main.py
├── readme.md
└── .venv/   (optional, if created locally)
```

## Application Endpoints
### 1. Root Endpoint
- Method: GET
- Route: `/`
- Description: Returns a welcome message.

Example response:
```json
{
  "message": "Hello World"
}
```

### 2. Health Check Endpoint
- Method: GET
- Route: `/health`
- Description: Returns the status of the application.

Example response:
```json
{
  "Status": "Healthy"
}
```

## Prerequisites
Before running this project, ensure you have:
- Python 3.8 or higher installed
- pip installed
- internet access to install dependencies

## Setup Instructions
1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

For Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

For macOS/Linux:
```bash
source .venv/bin/activate
```

3. Install the required packages:

```bash
pip install fastapi uvicorn
```

## Run the Application
Start the FastAPI server with either of the following commands:

```bash
uvicorn main:app --reload
```
or

```bash
uv run fastapi dev
```

Once the server is running, open the browser or API client and visit:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health

## API Documentation
FastAPI automatically provides interactive API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Notes
This is a basic starter backend and can be extended with:
- user authentication
- database integration
- CRUD operations
- environment configuration
- deployment setup

## Summary
This task demonstrates a minimal FastAPI backend with a working hello endpoint and a health check. It serves as a foundation for building more advanced APIs in future tasks and marks my first assignment as part of the Swynex internship.
