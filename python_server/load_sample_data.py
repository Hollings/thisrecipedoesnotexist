"""Utility script to bulk insert a handful of sample recipes for testing."""
from __future__ import annotations

import argparse
from pathlib import Path

from sqlalchemy.exc import SQLAlchemyError

from .database import engine, init_db


def load_recipes(sql_path: Path, limit: int) -> int:
    """Insert up to *limit* recipes found in the SQL dump."""
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    inserted = 0
    init_db()

    with engine.begin() as connection:
        with sql_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or not line.upper().startswith("INSERT INTO"):
                    continue

                statement = line.replace("recipes.recipes", "recipes")
                try:
                    connection.exec_driver_sql(statement)
                except SQLAlchemyError as exc:  # pragma: no cover - ad-hoc script
                    raise RuntimeError(f"Failed to execute: {statement[:80]}...") from exc

                inserted += 1
                if inserted >= limit:
                    break

    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "sql_file",
        type=Path,
        help="Path to the recipes_recipes.sql dump",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of INSERT statements to run (default: 10)",
    )
    args = parser.parse_args()

    inserted = load_recipes(args.sql_file, args.limit)
    print(f"Inserted {inserted} recipes from {args.sql_file}")


if __name__ == "__main__":  # pragma: no cover - script entry point
    main()
