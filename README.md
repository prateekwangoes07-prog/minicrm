# MiniCRM

MiniCRM is a production-ready, AI-powered customer relationship management SaaS application designed to help businesses manage customer data, leads, activities, tasks, and communications efficiently.

## Repository Architecture

This project is built using a clean, decoupled architecture:

```
MiniCRM/
├── backend/            # FastAPI backend service
│   ├── app/            # Main application package
│   │   ├── api/        # REST route definitions (grouped by version)
│   │   ├── core/       # Configurations, database session setup, security
│   │   ├── db/         # SQLAlchemy async engine, session makers, and get_db dependencies
│   │   ├── models/     # SQLAlchemy database models
│   │   ├── schemas/    # Pydantic validation schemas
│   │   ├── services/   # Business logic / domain services
│   │   └── repositories/# Direct database queries/operations
│   ├── alembic/        # Alembic database migrations
│   ├── tests/          # Pytest fixtures and backend test files
│   ├── Dockerfile      # Backend environment setup
│   └── requirements.txt# Core Python packages
│
├── frontend/           # Next.js frontend application
│   ├── src/            # Next.js source code
│   │   ├── app/        # App Router routing directories
│   │   ├── components/ # Reusable UI widgets
│   │   ├── features/   # Feature-sliced modules (e.g. leads/, tasks/)
│   │   ├── hooks/      # Reusable React hooks
│   │   ├── lib/        # Third-party client initializations (e.g., API client)
│   │   ├── services/   # API calling functions
│   │   ├── types/      # Shared TypeScript interfaces
│   │   ├── utils/      # Stateless helper utilities
│   │   └── styles/     # Global theme-level styling assets
│   ├── public/         # Static assets (images, fonts, etc.)
│   ├── Dockerfile      # Frontend container configuration
│   └── tsconfig.json   # TypeScript configurations
│
├── docs/               # Architecture, UI, API and Database guidelines
└── docker-compose.yml  # Local multi-container orchestrator
```

### Folder Purposes

* **`backend/`**: Serves as the REST API engine. Built on FastAPI for rapid async performance.
  * `core/`: Application settings, security routines, database engine creation.
  * `db/`: Async engine sessions and database connection pooling.
  * `models/`: Translates database schemas into SQLAlchemy objects.
  * `schemas/`: Houses structural input/output definitions using Pydantic.
  * `repositories/`: Encapsulates database actions to enforce decoupled DB queries.
  * `services/`: Coordinates transactions, third-party connections, and AI logic.
  * `alembic/`: Handles incremental, version-controlled database schema updates.
  * `tests/`: Holds testing suites containing async DB and client fixtures.
* **`frontend/`**: The visual layer built on Next.js 15, React 19, and Tailwind CSS.
* **`docs/`**: Standard engineering manuals outlining project rules, UI patterns, API requirements, and DB conventions.
* **`docker-compose.yml`**: Ties the system together locally, spinning up a PostgreSQL database alongside the frontend and backend microservices with automatic volume mounts for real-time code reloading.

---

## Local Development Setup

To initialize the project environment, make sure you have [Docker](https://www.docker.com/) installed and running.

### 1. Copy Environment Configurations

Create local configuration files from the templates:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Start all Services

In the project root directory, spin up the containers:

```bash
docker compose up --build
```

This starts:
- PostgreSQL at `localhost:5432`
- FastAPI Server at `localhost:8000` (Docs available at `http://localhost:8000/docs`)
- Next.js Web App at `localhost:3000`

### 3. Service Verification

Once all containers are running successfully:
- **API Health Check**: Access `http://localhost:8000/health` to confirm the API connection is active.
- **Frontend Check**: Open `http://localhost:3000` to inspect the UI dashboard.

---

## Database Migrations (Alembic)

Whenever database models change, execute migrations:

```bash
# Generate a new migration script
docker compose exec backend alembic revision --autogenerate -m "describe your changes"

# Apply migrations
docker compose exec backend alembic upgrade head
```

---

## Running Tests

To execute backend tests:

```bash
docker compose exec backend pytest
```

