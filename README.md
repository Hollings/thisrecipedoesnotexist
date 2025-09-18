This Recipe Does Not Exist is an AI powered recipe site and twitter bot

https://thisrecipedoesnotexist.com/ | https://twitter.com/DoesRecipe


![Screenshot 2021-05-11 125032](https://user-images.githubusercontent.com/3793509/117869012-82b91a80-b257-11eb-9efe-5a273b7a0828.png)

GPT-2 model was trained using scraped data from various recipe websites, recipes are generated using python and GPT-2, Twitter bot posts every three hours from a python script.

## Backend

The original Laravel backend has been replaced with a lightweight Python service that keeps the existing routes and behaviour used by the site and automation scripts.

### Running the server locally

1. Install dependencies: `pip install -r python_server/requirements.txt`
2. (Optional) Point the app at an existing database by setting `DATABASE_URL`. If omitted the server will create `python_server/app.db` (SQLite).
3. Create the tables (only required for brand new databases): `python3 -c "from python_server.database import init_db; init_db()"`
4. Start the development server: `flask --app python_server.app run --debug` (or `python3 -m python_server.app`).

Environment variables:

- `DATABASE_URL` – SQLAlchemy connection string. Supports SQLite/MySQL/PostgreSQL (requires matching driver).
- `TRDNE_ADMIN_PASSWORD_HASH` – override the default bcrypt hash used to authenticate the recipe/comment ingestion scripts.

Static assets and templates now live under `python_server/static` and `python_server/templates` respectively.

#### Loading sample data

To import the first 10 recipes from `recipes_recipes.sql` into your configured database run:

```
python3 -m python_server.load_sample_data recipes_recipes.sql --limit 10
```

Adjust `--limit` as needed. The command runs against whichever database `DATABASE_URL` points to (defaults to the bundled SQLite database).

### Docker Compose

1. Build and start the container: `docker compose up --build`
2. Visit the site at `http://localhost:8000`
3. To run migrations on a fresh database, exec into the container: `docker compose exec web python3 -c "from python_server.database import init_db; init_db()"`
4. To seed sample recipes in the container: `docker compose cp recipes_recipes.sql web:/app/recipes_recipes.sql` then `docker compose exec web python3 -m python_server.load_sample_data /app/recipes_recipes.sql --limit 10`

Compose environment variables (can be configured in a `.env` file next to `docker-compose.yml`):

- `DATABASE_URL` – defaults to `sqlite:////data/app.db`
- `TRDNE_ADMIN_PASSWORD_HASH` – optional bcrypt hash override

A named volume (`recipe-data`) stores the SQLite database at `/data/app.db` inside the container so data persists between restarts.
