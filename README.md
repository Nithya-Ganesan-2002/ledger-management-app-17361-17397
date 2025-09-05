# Ledger Management App

BackendServiceContainer (FastAPI) provides:
- JWT-based authentication with role-based access control
- Transaction processing endpoints
- Reporting stubs
- Async SQLAlchemy DB integration

Run locally:
1) Create and set environment variables (copy BackendServiceContainer/.env.example to .env and adjust).
2) Install dependencies: `pip install -r BackendServiceContainer/requirements.txt`
3) Start API:
   - Seed and run: `python -m ledger-management-app-17361-17397.BackendServiceContainer.src.api.run`
   - Or via uvicorn: `uvicorn ledger-management-app-17361-17397.BackendServiceContainer.src.api.main:app --host 0.0.0.0 --port 8000`

Default seeded admin:
- username: admin
- password: admin

Auth:
- POST /auth/login -> { "token": "<JWT>" }

Transactions:
- Use Authorization: Bearer <token>
- POST /transactions
- GET /transactions

Docs:
- /docs
- /openapi.json