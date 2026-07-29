# MiniCRM - Master Engineering Rules

This document serves as the permanent single source of truth for the development, architecture, testing, and deployment of MiniCRM. All engineers and AI systems must strictly adhere to these guidelines.

---

## 1. Project Vision
MiniCRM is a production-ready AI-powered SaaS application helping businesses manage customers, leads, activities, tasks, and communications through a clean, modern web interface. The core design is built to be simple to learn, scalable, and secure, laying the foundation for future AI integrations such as automated summaries and intelligent lead scoring.

## 2. Technology Stack
* **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS, shadcn/ui.
* **Backend**: FastAPI (Python), SQLAlchemy 2.0 (Async).
* **Database**: PostgreSQL 16.
* **Authentication**: Stateless JWT via HttpOnly cookies.
* **Migrations**: Alembic.
* **Orchestration**: Docker & Docker Compose.

## 3. Folder Structure
The repository is split into isolated services:

```
MiniCRM/
├── backend/            # FastAPI python application root
│   ├── app/            # Source package containing app layers
│   │   ├── api/        # REST controllers and routing tables
│   │   ├── core/       # Configurations and security loaders
│   │   ├── db/         # Async engine setup and sessions
│   │   ├── models/     # Database entities (SQLAlchemy)
│   │   ├── schemas/    # Verification payloads (Pydantic)
│   │   ├── services/   # Business processes and integrations
│   │   ├── repositories/# Direct DB queries and CRUDs
│   │   ├── middleware/ # Reserved middleware
│   │   ├── exceptions/ # Reserved custom exceptions
│   │   └── dependencies/# Reserved custom dependencies
│   ├── alembic/        # Migration version configurations
│   └── tests/          # Pytest fixtures and mock tests
│
├── frontend/           # Next.js web application root
│   ├── src/            # Core UI layout source folder
│   │   ├── app/        # App Router dynamic URL layers
│   │   ├── components/ # Generic UI modules
│   │   ├── features/   # Feature-grouped pages and logic
│   │   ├── hooks/      # Shared React state routines
│   │   ├── lib/        # Reusable client driver settings
│   │   ├── services/   # REST endpoint connectors
│   │   ├── types/      # Domain interface files
│   │   ├── utils/      # Utility helpers
│   │   └── styles/     # Theming styles
│   └── public/         # Shared image/font binaries
│
└── docs/               # Technical manual folders
```

## 4. Clean Architecture Principles & Dependency Ordering
The project maintains a strict unidirectional data flow. Visual components never fetch database queries directly; route handlers do not contain business algorithms; and database engines are decoupled from domain models.

To ensure loose coupling, modules follow a strict hierarchy. A module can import layers below it but must never import layers above it:
```
  [Route Endpoint API]
           │
           ▼
     [Service layer]
           │
           ▼
    [Repository layer]
           │
           ▼
    [Database Session]
```
No layer other than repositories should perform database connections or execute query dialects.

## 5. Layer Responsibilities (Backend)
* **`api/`**: Exposes HTTP routes. Parses and validates requests using schemas. Invokes services.
* **`services/`**: Holds core business workflows (e.g. lead calculations, emails). Calls repositories.
* **`repositories/`**: Executes database query selections and transactions.
* **`models/`**: Defines the SQLAlchemy relational mapping tables.
* **`schemas/`**: Pydantic schemas validating API inputs and outputs.
* **`db/`**: Handles database sessions, async engine setups, and dependency injections.
* **`core/`**: Central configs (security keys, CORS headers, environment setups).

## 6. Frontend Structure
* **`app/`**: Route definitions.
* **`components/`**: Feature-independent UI widgets.
* **`features/`**: Feature-scoped components and logic (e.g., `leads/`, `tasks/`).
* **`hooks/`**: Custom React hooks.
* **`lib/`**: SDK setups and client drivers.
* **`services/`**: API fetching logic.
* **`types/`**: TypeScript type declarations.
* **`utils/`**: Helper utilities.
* **`styles/`**: Design styles.

## 7. Naming Conventions
* **Files/Directories**: `snake_case` in Python; `PascalCase` for React components; `camelCase` for hooks/utilities.
* **Variables/Functions**: `snake_case` in Python; `camelCase` in TypeScript.
* **Classes/Types**: `PascalCase` in both Python and TypeScript.

## 8. TypeScript Guidelines
* Enforce strict type checking. Avoid use of `any`.
* Define clear interfaces or types for all component props and API responses.
* Utilize path mappings (`@/*`) for clean import paths.

## 9. Python Guidelines
* Code must comply with PEP 8. Use `Ruff` for formatting and linting.
* Enforce explicit type hints on all function parameters and returns.
* Use async/await patterns for all database actions.

## 10. API Design Standards
* Resource paths must use plural nouns (e.g., `/api/v1/leads`).
* Return descriptive JSON structures and HTTP status codes (200, 201, 400, 401, 403, 404, 422, 500).
* API endpoints must be versioned (prefixed with `/api/v1/`).

## 11. Database Standards
* Tables must use plural snake_case naming (e.g., `leads`).
* Use UUIDs as primary keys for security.
* Explicitly create indexes on all foreign key columns.

## 12. Error Handling Standards
* Backend: Raise HTTPExceptions with structured detail models.
* Frontend: Trap API errors gracefully using error boundaries or toast notifications.

## 13. Logging Standards
* Implement structured logging. Write logs to stdout in JSON format in production.
* Trace execution states using standard levels (`INFO`, `WARNING`, `ERROR`, `CRITICAL`).

## 14. Validation Standards
* Perform input validations at the perimeter: backend routes use Pydantic; frontend forms use React Hook Form + Zod.

## 15. Security Guidelines
* Keep JWT secrets out of git. Store JWTs in HttpOnly, Secure, SameSite cookies.
* Sanitize user entries to prevent XSS and SQL injection.

## 16. Environment Variable Rules
* All config loading must map to settings classes (e.g., Pydantic BaseSettings).
* Commit `.env.example` templates; never commit `.env` files.

## 17. Git Branching Strategy
* Maintain a locked `main` branch. Development happens on `feature/` or `bugfix/` branches.

## 18. Commit Message Convention
* Adhere to Conventional Commits: `type(scope): description`. Valid types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

## 19. Code Review Checklist
* Confirm types are strictly declared.
* Ensure database transactions are closed properly.
* Check that unit tests are included for new logic.

## 20. Testing Strategy
* Write unit tests for services using `pytest` (backend) and `Jest`/`Vitest` (frontend).
* Mock external integrations (like LLMs or mail transfer servers).

## 21. Docker Guidelines
* Use multi-stage Docker builds to reduce final bundle sizes.
* Set non-root users inside production runner environments.

## 22. Performance Guidelines
* Use connection pooling for databases.
* Optimize Next.js bundles using static generation where possible and lazy loading.

## 23. Documentation Rules
* Keep code comments meaningful. Document public APIs using docstrings.
* Maintain up-to-date `.md` architectural guides under `/docs`.

## 24. AI Assistant Rules
* Never modify code styles or formatting setups.
* Do not make sweeping edits; use target file modifiers where appropriate.
* Do not generate placeholder logic.

## 25. Development Workflow
1. Pull latest code from `main`.
2. Create a local branch.
3. Code the feature, adding tests and running lint checks.
4. Run `docker compose up --build` to verify system behavior.
5. Create a Pull Request and merge to `main` upon review.
