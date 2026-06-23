# FastAPI Blog

A blog application built with FastAPI, SQLAlchemy, and PostgreSQL.

## Setup

1. Start PostgreSQL with Docker:
   ```bash
   docker-compose up -d
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run migrations:
   ```bash
   uv run alembic upgrade head
   ```

4. Start the app:
   ```bash
   uv run uvicorn main:app --reload
   ```

## Database Management

### Docker & PostgreSQL

Start PostgreSQL container:
```bash
docker-compose up -d
```

Connect to the database:
```bash
docker-compose exec postgres psql -U bloguser -d blog
```

Stop PostgreSQL:
```bash
docker-compose down
```

Remove data and restart clean:
```bash
docker-compose down -v
docker-compose up -d
```

### Alembic Migrations

Create a new migration (auto-detects model changes):
```bash
uv run alembic revision --autogenerate -m "add likes to posts"
```

Apply migrations to the database:
```bash
uv run alembic upgrade head
```

Check current migration version:
```bash
uv run alembic current
```

Rollback to previous migration:
```bash
uv run alembic downgrade -1
```

View migration history:
```bash
uv run alembic history
```

## Useful SQL Queries

```sql
-- List all tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- List columns in a table
\d table_name

-- View table structure
\d+ posts
```
