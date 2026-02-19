# python-api-integration-samples

Portfolio project that demonstrates a clean Python integration with a real API (Todoist API v1), including:

- API client with typed methods
- CLI with subcommands
- Error handling (timeouts, network, HTTP errors)
- Unit tests with request mocking

## Requirements

- Python 3.10+
- Todoist API token

## Project structure

```text
README.md
requirements.txt
.env.example
.gitignore
cli.py
clients/
  __init__.py
  todoist_client.py
tests/
  test_todoist_client.py
```

## Setup (Windows PowerShell)

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create `.env` from template:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set your token:

```env
TODOIST_API_TOKEN=YOUR_REAL_TOKEN
```

## Optional: virtual environment

If your Python installation supports `venv` correctly:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If `venv` fails on your machine, you can run this project without activation using `python ...` commands.

## CLI usage

List tasks:

```powershell
python cli.py list --filter "today | overdue" --limit 10
```

Add a task:

```powershell
python cli.py add "Prepare API demo" --due "tomorrow at 10am"
```

Close a task:

```powershell
python cli.py close 1234567890
```

Note: use a real numeric/alphanumeric id. Do not type `<task_id>` literally in PowerShell.

## Run tests

```powershell
python -m pytest -q
```

## Troubleshooting

- `Missing or placeholder TODOIST_API_TOKEN`:
  - Ensure `.env` exists in the same folder as `cli.py`.
  - Ensure the value is real (not `REPLACE_...`).
- `HTTP 401 Unauthorized`:
  - Token is invalid/revoked/wrong account. Generate a new token and update `.env`.
- `HTTP 410 deprecated endpoint`:
  - This repo already uses Todoist API v1 (`https://api.todoist.com/api/v1`).

## References

- Todoist API docs (v1): https://developer.todoist.com/api/v1/
- Find your API token: https://www.todoist.com/help/articles/find-your-api-token-Jpzx9IIlB
