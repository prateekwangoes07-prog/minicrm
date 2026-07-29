# MiniCRM - Database Layout & Migration Rules

This document details database tables, key styles, index choices, and Alembic versioning. For general coding policies, read [MASTER_RULES.md](file:///c:/Users/User/OneDrive/Desktop/MiniCRM/docs/MASTER_RULES.md).

---

## 1. Primary & Foreign Keys

* **Primary Keys**:
  * Standardize on UUID fields for user-facing tables.
  * Name primary keys simply `id`.
* **Foreign Keys**:
  * Reference field names should append `_id` (e.g. `customer_id` references `customers.id`).
  * Enforce referential constraints at the database engine level (e.g., `ondelete="CASCADE"`).

---

## 2. Index Placement Rules

* Create indexes on all Foreign Keys to prevent table scan locks on joins.
* Place indexes on query columns present in filters or sorts:
  * E-mail lookups: `email`
  * Creation dates: `created_at`
  * Status parameters: `status`

---

## 3. Alembic CLI Protocols

All database schema modifications must run through Alembic. Never use `metadata.create_all()` in production code.

### Commands reference:

* **Generate Revision**:
  ```bash
  docker compose exec backend alembic revision --autogenerate -m "add index to emails"
  ```
* **Apply Migration**:
  ```bash
  docker compose exec backend alembic upgrade head
  ```
* **Revert Migration**:
  ```bash
  docker compose exec backend alembic downgrade -1
  ```
