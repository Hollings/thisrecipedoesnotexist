"""SQLAlchemy models mirroring the original Laravel data structures."""
from __future__ import annotations

import json
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class TimestampMixin:
    """Mixin that provides created/updated timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    directions: Mapped[str] = mapped_column(Text, nullable=False)
    save: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    temp: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan"
    )
    queued_recipe: Mapped["QueuedRecipe"] = relationship(
        back_populates="recipe", uselist=False
    )

    @staticmethod
    def _loads(value: str) -> List[str]:
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return []

    @property
    def ingredient_list(self) -> List[str]:
        return self._loads(self.ingredients)

    @property
    def direction_list(self) -> List[str]:
        return self._loads(self.directions)


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)

    recipe: Mapped[Recipe] = relationship(back_populates="comments")


class QueuedRecipe(Base, TimestampMixin):
    __tablename__ = "queued_recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[int | None] = mapped_column(ForeignKey("recipes.id"), nullable=True)
    requested_by_name: Mapped[str] = mapped_column(String(255), nullable=False)
    requested_by_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mention_id: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)

    recipe: Mapped[Recipe | None] = relationship(back_populates="queued_recipe")
