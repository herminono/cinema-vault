import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Float, Integer, String, inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

load_dotenv()

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # TMDB genres stored as comma-separated labels, e.g. "Action, Science Fiction"
    genre: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()
    # Additive migration for older databases created by the tutorial project.
    if "genre" not in {c["name"] for c in inspect(db.engine).get_columns("movie")}:
        with db.engine.begin() as connection:
            connection.execute(text("ALTER TABLE movie ADD COLUMN genre VARCHAR(250)"))


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Search TMDB")


class RateMovieForm(FlaskForm):
    rating = FloatField("Your rating (0–10)", validators=[Optional(), NumberRange(min=0, max=10)])
    review = StringField("Your review", validators=[Optional()])
    genre = StringField("Genres (comma-separated)", validators=[Optional()])
    submit = SubmitField("Save changes")


class DeleteMovieForm(FlaskForm):
    submit = SubmitField("Delete")


def tmdb_get(url, params):
    api_key = os.environ.get("MOVIE_DB_API_KEY")
    if not api_key:
        raise ValueError("Set MOVIE_DB_API_KEY in your .env file.")
    response = requests.get(url, params={"api_key": api_key, **params}, timeout=10)
    response.raise_for_status()
    return response.json()


@app.route("/")
def home():
    all_movies = db.session.scalars(
        db.select(Movie).order_by(Movie.rating.desc().nullslast(), Movie.title)
    ).all()
    genres = sorted({g.strip() for movie in all_movies for g in (movie.genre or "").split(",") if g.strip()})

    selected_genre = request.args.get("genre", "").strip()
    min_raw = request.args.get("min_rating", "").strip()
    max_raw = request.args.get("max_rating", "").strip()
    error = None
    try:
        min_rating = float(min_raw) if min_raw else None
        max_rating = float(max_raw) if max_raw else None
        if (min_rating is not None and not 0 <= min_rating <= 10) or (max_rating is not None and not 0 <= max_rating <= 10):
            raise ValueError
        if min_rating is not None and max_rating is not None and min_rating > max_rating:
            raise ValueError
    except ValueError:
        error = "Enter a valid rating range between 0 and 10 (minimum must not exceed maximum)."
        min_rating = max_rating = None

    movies = []
    for index, movie in enumerate(all_movies, start=1):
        movie.display_rank = index
        movie_genres = [g.strip().casefold() for g in (movie.genre or "").split(",")]
        if selected_genre and selected_genre.casefold() not in movie_genres:
            continue
        if min_rating is not None and (movie.rating is None or movie.rating < min_rating):
            continue
        if max_rating is not None and (movie.rating is None or movie.rating > max_rating):
            continue
        movies.append(movie)

    return render_template("index.html", movies=movies, genres=genres, selected_genre=selected_genre,
                           min_rating=min_raw, max_rating=max_raw, error=error,
                           total=len(all_movies), delete_form=DeleteMovieForm())


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        try:
            data = tmdb_get(TMDB_SEARCH_URL, {"query": form.title.data})
            return render_template("select.html", options=data.get("results", []))
        except (requests.RequestException, ValueError) as exc:
            flash(f"Movie search failed: {exc}", "danger")
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id", type=int)
    if movie_api_id is None:
        return redirect(url_for("add_movie"))
    try:
        data = tmdb_get(f"{TMDB_MOVIE_URL}/{movie_api_id}", {"language": "en-US"})
        title = data.get("title", "")
        existing = db.session.scalar(db.select(Movie).where(Movie.title == title))
        if existing:
            flash("That movie is already in your collection.", "info")
            return redirect(url_for("rate_movie", id=existing.id))
        movie = Movie(
            title=title,
            year=int((data.get("release_date") or "0000").split("-")[0]),
            img_url=f"{TMDB_IMAGE_URL}{data['poster_path']}" if data.get("poster_path") else "",
            description=(data.get("overview") or "No overview available.")[:500],
            genre=", ".join(genre["name"] for genre in data.get("genres", [])),
        )
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("rate_movie", id=movie.id))
    except (requests.RequestException, ValueError, KeyError) as exc:
        flash(f"Could not add movie: {exc}", "danger")
        return redirect(url_for("add_movie"))


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    movie = db.get_or_404(Movie, request.args.get("id", type=int))
    form = RateMovieForm(obj=movie)
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = (form.review.data or "")[:250]
        movie.genre = (form.genre.data or "")[:250]
        db.session.commit()
        flash("Movie updated.", "success")
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete", methods=["POST"])
def delete_movie():
    form = DeleteMovieForm()
    if form.validate_on_submit():
        movie = db.get_or_404(Movie, request.form.get("id", type=int))
        db.session.delete(movie)
        db.session.commit()
        flash("Movie deleted.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
