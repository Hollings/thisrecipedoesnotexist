"""Flask application that replaces the original Laravel backend."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from .database import SessionLocal, engine, init_db, session_scope
from .models import Comment, QueuedRecipe, Recipe
from .utils import (
    anonymise_username,
    humanize_timespan,
    is_search_bot,
    verify_password,
)


def _random_clause():
    """Return the appropriate SQL random function for the active dialect."""
    dialect = engine.dialect.name.lower()
    if dialect == "mysql":
        return func.rand()
    return func.random()


def _serialise_recipe(
    recipe: Recipe, *, include_comments: bool = False, include_queue: bool = False
) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "id": recipe.id,
        "title": recipe.title,
        "ingredients": recipe.ingredient_list,
        "directions": recipe.direction_list,
        "views": recipe.views,
        "temp": recipe.temp,
        "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
        "created_at_display": recipe.created_at.strftime("%Y-%m-%d %H:%M:%S")
        if recipe.created_at
        else "",
        "created_at_human": humanize_timespan(recipe.created_at),
    }
    if include_comments:
        data["comments"] = [_serialise_comment(c) for c in recipe.comments]
    if include_queue and recipe.queued_recipe:
        data["queued_recipe"] = _serialise_queue(recipe.queued_recipe)
    return data


def _serialise_comment(comment: Comment, *, include_recipe: bool = False) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "id": comment.id,
        "username": comment.username,
        "rating": int(round(comment.rating)),
        "body": comment.body,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
        "created_at_human": humanize_timespan(comment.created_at),
    }
    if include_recipe and comment.recipe:
        data["recipe"] = {
            "id": comment.recipe.id,
            "title": comment.recipe.title,
        }
    return data


def _serialise_queue(queue: QueuedRecipe) -> Dict[str, Any]:
    return {
        "id": queue.id,
        "recipe_id": queue.recipe_id,
        "requested_by_name": queue.requested_by_name,
        "requested_by_id": queue.requested_by_id,
        "mention_id": queue.mention_id,
        "title": queue.title,
        "status": queue.status,
        "created_at": queue.created_at.isoformat() if queue.created_at else None,
        "created_at_human": humanize_timespan(queue.created_at),
    }


def _extract_payload() -> Dict[str, Any]:
    payload = request.get_json(silent=True)
    if payload is None:
        payload = request.form.to_dict()
    return payload or {}


def _ensure_password(payload: Dict[str, Any]) -> bool:
    password = payload.get("password", "")
    return isinstance(password, str) and verify_password(password)


def _to_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_json_field(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value)


def create_app() -> Flask:
    init_db()

    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["JSON_SORT_KEYS"] = False

    @app.teardown_appcontext
    def remove_session(_: Optional[BaseException]) -> None:  # pragma: no cover - flask hook
        SessionLocal.remove()

    @app.route("/")
    def index():
        user_agent = request.headers.get("User-Agent")
        with session_scope() as session:
            recipe = (
                session.query(Recipe)
                .options(joinedload(Recipe.comments))
                .filter(Recipe.views == 0)
                .order_by(Recipe.created_at.asc())
                .first()
            )
            if recipe is None:
                recipe = (
                    session.query(Recipe)
                    .options(joinedload(Recipe.comments))
                    .order_by(_random_clause())
                    .first()
                )
            if recipe is None:
                return render_template(
                    "home.html",
                    r=None,
                    total=0,
                    recent=[],
                    freshRecipeCount=0,
                    recentComments=[],
                    dark_mode_enabled=bool(request.cookies.get("darkmode")),
                )

            if not is_search_bot(user_agent):
                recipe.views += 1

            total = session.query(func.count(Recipe.id)).scalar() or 0
            fresh_count = (
                session.query(func.count(Recipe.id))
                .filter(Recipe.views == 0)
                .scalar()
                or 0
            )
            recent_recipes = (
                session.query(Recipe)
                .order_by(_random_clause())
                .limit(5)
                .all()
            )
            recent_comments = (
                session.query(Comment)
                .options(joinedload(Comment.recipe))
                .order_by(_random_clause())
                .limit(5)
                .all()
            )

            recipe_payload = _serialise_recipe(recipe, include_comments=True)
            recent_payload = [
                {**_serialise_recipe(r), "timeAgo": humanize_timespan(r.created_at)}
                for r in recent_recipes
            ]
            comment_payload = [
                _serialise_comment(comment, include_recipe=True)
                for comment in recent_comments
            ]

        return render_template(
            "home.html",
            r=recipe_payload,
            total=total,
            recent=recent_payload,
            freshRecipeCount=fresh_count,
            recentComments=comment_payload,
            dark_mode_enabled=bool(request.cookies.get("darkmode")),
        )

    @app.route("/<int:recipe_id>")
    def view_recipe(recipe_id: int):
        user_agent = request.headers.get("User-Agent")
        with session_scope() as session:
            recipe = (
                session.query(Recipe)
                .options(joinedload(Recipe.comments))
                .filter(Recipe.id == recipe_id)
                .first()
            )
            if recipe is None:
                abort(404)

            if not is_search_bot(user_agent):
                recipe.views += 1

            total = session.query(func.count(Recipe.id)).scalar() or 0
            fresh_count = (
                session.query(func.count(Recipe.id))
                .filter(Recipe.views == 0)
                .scalar()
                or 0
            )
            recent_recipes = (
                session.query(Recipe)
                .order_by(_random_clause())
                .limit(5)
                .all()
            )
            recent_comments = (
                session.query(Comment)
                .options(joinedload(Comment.recipe))
                .order_by(_random_clause())
                .limit(5)
                .all()
            )

            recipe_payload = _serialise_recipe(recipe, include_comments=True)
            recent_payload = [
                {**_serialise_recipe(r), "timeAgo": humanize_timespan(r.created_at)}
                for r in recent_recipes
            ]
            comment_payload = [
                _serialise_comment(comment, include_recipe=True)
                for comment in recent_comments
            ]

        return render_template(
            "home.html",
            r=recipe_payload,
            total=total,
            recent=recent_payload,
            freshRecipeCount=fresh_count,
            recentComments=comment_payload,
            dark_mode_enabled=bool(request.cookies.get("darkmode")),
        )

    @app.route("/darkmode")
    def toggle_darkmode():
        response = make_response(redirect(request.referrer or url_for("index")))
        if request.cookies.get("darkmode"):
            response.delete_cookie("darkmode")
        else:
            max_age = 60 * 60 * 24 * 365 * 5
            response.set_cookie("darkmode", "1", max_age=max_age, samesite="Lax")
        return response

    @app.route("/favicon.ico")
    def favicon():
        return app.send_static_file("favicon.ico")

    @app.route("/robots.txt")
    def robots_txt():
        return app.send_static_file("robots.txt")

    @app.route("/create/<string:title>")
    def queue_recipe_from_title(title: str):
        payload: Dict[str, Any]
        with session_scope() as session:
            queued = QueuedRecipe(
                title=title,
                status="queued",
                requested_by_name="site",
                requested_by_id="0",
                mention_id="0",
            )
            session.add(queued)
            session.flush()
            payload = _serialise_queue(queued)
        return jsonify(payload)

    @app.route("/api/add", methods=["POST"])
    def add_recipe():
        payload = _extract_payload()
        if not _ensure_password(payload):
            return "failed"

        title = payload.get("title")
        directions = payload.get("directions")
        ingredients = payload.get("ingredients")
        if not title or not directions or not ingredients:
            return jsonify({"error": "Missing required fields"}), 400

        temp = payload.get("temp", 1.0)
        queue_id = payload.get("queue_id")

        with session_scope() as session:
            recipe = Recipe(
                title=title,
                directions=_parse_json_field(directions),
                ingredients=_parse_json_field(ingredients),
                temp=_to_float(temp, 1.0),
            )
            session.add(recipe)
            session.flush()

            queue_id_int = _to_int(queue_id)
            if queue_id_int is not None:
                queue = (
                    session.query(QueuedRecipe)
                    .filter(QueuedRecipe.id == queue_id_int)
                    .first()
                )
                if queue:
                    queue.status = "generated"
                    queue.recipe_id = recipe.id

            recipe_id = recipe.id

        return str(recipe_id)

    @app.route("/api/comment/add", methods=["POST"])
    def add_comment():
        payload = _extract_payload()
        if not _ensure_password(payload):
            return "Invalid Pass"

        username = payload.get("username", "Anonymous")
        rating = _to_float(payload.get("rating"), 0.0)
        body = payload.get("body")
        recipe_id = payload.get("recipe_id")

        if not body:
            return jsonify({"error": "Comment body is required"}), 400

        with session_scope() as session:
            recipe: Optional[Recipe]
            recipe_id_int = _to_int(recipe_id)
            if recipe_id_int is not None:
                recipe = (
                    session.query(Recipe)
                    .filter(Recipe.id == recipe_id_int)
                    .first()
                )
            else:
                recipe = (
                    session.query(Recipe)
                    .order_by(_random_clause())
                    .first()
                )

            if recipe is None:
                return jsonify({"error": "Recipe not found"}), 404

            comment = Comment(
                username=anonymise_username(username),
                rating=rating,
                body=body,
                recipe=recipe,
            )
            session.add(comment)
            session.flush()
            comment_payload = _serialise_comment(comment, include_recipe=True)

        return jsonify(comment_payload)

    @app.route("/api/queue", methods=["POST"])
    def queue_recipe():
        payload = _extract_payload()
        mention_id = payload.get("mention_id")
        if not mention_id:
            return jsonify({"error": "mention_id is required"}), 400

        with session_scope() as session:
            existing = (
                session.query(QueuedRecipe)
                .filter(QueuedRecipe.mention_id == str(mention_id))
                .first()
            )
            if existing:
                return str(existing.id)

            recipe_id_int = _to_int(payload.get("recipe_id"))
            queue = QueuedRecipe(
                title=payload.get("title", "Untitled"),
                status=payload.get("status", "queued"),
                requested_by_name=payload.get("requested_by_name", "unknown"),
                requested_by_id=str(payload.get("requested_by_id", "0")),
                mention_id=str(mention_id),
                recipe_id=recipe_id_int,
            )
            session.add(queue)
            session.flush()
            new_id = queue.id

        return str(new_id)

    @app.route("/api/queue", methods=["GET"])
    def next_queue_item():
        with session_scope() as session:
            queue = (
                session.query(QueuedRecipe)
                .filter(QueuedRecipe.status == "queued")
                .order_by(QueuedRecipe.created_at.asc())
                .first()
            )
            if queue is None:
                return jsonify({})
            payload = _serialise_queue(queue)
        return jsonify(payload)

    @app.route("/api/recipe", methods=["GET"])
    def get_recipe_raw():
        with session_scope() as session:
            recipe = (
                session.query(Recipe)
                .join(QueuedRecipe, Recipe.id == QueuedRecipe.recipe_id)
                .options(joinedload(Recipe.queued_recipe))
                .filter(QueuedRecipe.status == "generated")
                .filter(QueuedRecipe.requested_by_name != "site")
                .first()
            )

            if recipe is not None and recipe.queued_recipe is not None:
                recipe.queued_recipe.status = "complete"
                payload = _serialise_recipe(recipe, include_queue=True)
            else:
                recipe = (
                    session.query(Recipe)
                    .options(joinedload(Recipe.queued_recipe))
                    .order_by(_random_clause())
                    .first()
                )
                if recipe is None:
                    return jsonify({})
                payload = _serialise_recipe(recipe, include_queue=True)

        return jsonify(payload)

    @app.route("/api/search", methods=["GET"])
    def search_recipes():
        query = request.args.get("query", "").strip()
        if not query:
            return jsonify([])

        like_pattern = f"%{query}%"
        with session_scope() as session:
            results = (
                session.query(Recipe.id, Recipe.title)
                .filter(Recipe.title.ilike(like_pattern))
                .order_by(Recipe.title.asc())
                .limit(20)
                .all()
            )
        return jsonify([{"id": rid, "title": title} for rid, title in results])

    return app


# Allow `python -m python_server.app` to run the development server easily
if __name__ == "__main__":  # pragma: no cover - convenience entry point
    app = create_app()
    app.run(debug=True)
