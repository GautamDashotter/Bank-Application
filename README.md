# Simple Bank API — With DB (Day 2, MongoDB Atlas)

Same REST API and business rules as Day 1, now backed by **MongoDB Atlas**
(a cloud-hosted, document-based NoSQL database) instead of in-memory storage.

## Architecture

```
Client → Controller (FastAPI routes) → Service Layer (business logic) → Repository Layer → MongoDB Atlas
```

- **`app/main.py`** — Controller layer: REST API routes
- **`app/service.py`** — Service layer: business rules (unchanged from the SQL version)
- **`app/repository.py`** — Repository layer: all direct MongoDB queries
- **`app/models.py`** — Pydantic request/response models
- **`app/database.py`** — MongoDB connection setup
- **`app/counters.py`** — helper to simulate auto-incrementing integer IDs

## Why MongoDB looks different from a SQL setup

- **No tables, no schema enforcement.** Data is stored as flexible JSON-like documents in "collections" (Mongo's equivalent of tables). There's no `CREATE TABLE` step — collections are created automatically the first time you insert into them.
- **No foreign keys / JOINs.** Relationships aren't enforced by the database. We handle this by storing (embedding) the account holder's name directly on each account document, rather than looking it up from a separate `users` collection every time.
- **No auto-increment by default.** MongoDB normally uses random `ObjectId`s as primary keys. To keep the API's `account_id`/`txn_id` as simple sequential integers (matching the original project spec), a small `counters` collection tracks the next ID for each entity type — see `app/counters.py`.

## Setup

1. **Create a MongoDB Atlas cluster** (free tier is fine): [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. In Atlas, go to **Database Access** and create a database user (username/password).
3. Go to **Network Access** and allow your IP (or `0.0.0.0/0` for open access during development).
4. Go to **Connect → Drivers**, copy the connection string.
5. Copy `.env.example` to `.env` and paste your connection string in:
   ```bash
   cp .env.example .env
   ```
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
   DB_NAME=simple_bank
   ```
6. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Run

```bash
uvicorn app.main:app --reload
```

API available at `http://127.0.0.1:8000`
Swagger docs at `http://127.0.0.1:8000/docs`

Collections (`users`, `accounts`, `transactions`, `counters`) are created automatically in Atlas the first time you create an account.

## Endpoints

Identical contract to the earlier versions — this matters, since it means the React frontend (Day 3) doesn't need to know or care which database is underneath:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts` | Create a new account |
| GET | `/api/accounts/{id}` | Get account details |
| POST | `/api/accounts/{id}/deposit` | Deposit money |
| POST | `/api/accounts/{id}/withdraw` | Withdraw money |
| GET | `/api/accounts/{id}/transactions` | View transaction history |

## Notes

- Don't commit your real `.env` — it contains your Atlas password (already excluded via `.gitignore`).
- Account documents store `user_name` directly (denormalized) to avoid a lookup on every read — if a user's name changes, you'd need to update it in both the `users` collection and any of their `accounts` documents.
