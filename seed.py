"""Populate CinemaVault with example movies for local demos.

Run from the project directory:
    python seed.py

Only missing titles are inserted. Existing movie data is never overwritten.
A TMDB API key is optional; when configured, posters are fetched from TMDB.
"""

import os

import requests
from sqlalchemy import select

from main import Movie, TMDB_IMAGE_URL, TMDB_SEARCH_URL, app, db


# Demo ratings/reviews are illustrative, not CinemaVault's official ratings.
SAMPLE_MOVIES = [
    {
        "title": "Interstellar", "year": 2014, "genre": "Adventure, Drama, Science Fiction",
        "rating": 9.2,
        "description": "Explorers journey beyond Earth to search for a future home for humanity.",
        "review": "Sample review: Ambitious and moving science fiction.",
    },
    {
        "title": "Spirited Away", "year": 2001, "genre": "Animation, Family, Fantasy",
        "rating": 9.5,
        "description": "A young girl navigates a mysterious spirit world to rescue her parents.",
        "review": "Sample review: A magical, imaginative adventure.",
    },
    {
        "title": "Knives Out", "year": 2019, "genre": "Comedy, Crime, Mystery",
        "rating": 8.3,
        "description": "A detective investigates a suspicious death in a wealthy family.",
        "review": "Sample review: A clever mystery with sharp humor.",
    },
    {
        "title": "The Dark Knight", "year": 2008, "genre": "Action, Crime, Drama",
        "rating": 9.0,
        "description": "Batman faces a dangerous new adversary who plunges Gotham into chaos.",
        "review": "Sample review: Gripping performances and tense action.",
    },
    {
        "title": "Little Women", "year": 2019, "genre": "Drama, Romance",
        "rating": 8.1,
        "description": "Four sisters pursue their dreams while growing up and growing apart.",
        "review": "Sample review: Warm, thoughtful storytelling.",
    },
    {
        "title": "Get Out", "year": 2017, "genre": "Horror, Mystery, Thriller",
        "rating": 8.6,
        "description": "A weekend visit takes a disturbing turn as unsettling secrets emerge.",
        "review": "Sample review: Suspenseful and inventive.",
    },
    {
        "title": "The Grand Budapest Hotel", "year": 2014, "genre": "Comedy, Drama",
        "rating": 8.4,
        "description": "A concierge and his young colleague become caught up in a wild adventure.",
        "review": "Sample review: Stylish, witty, and visually delightful.",
    },
    {
        "title": "Arrival", "year": 2016, "genre": "Drama, Mystery, Science Fiction",
        "rating": 8.7,
        "description": "A linguist works to communicate with visitors from another world.",
        "review": "Sample review: Reflective science fiction with emotional depth.",
    },
]


def poster_url(title, year):
    """Fetch a poster if an API key is configured; otherwise return an empty URL."""
    key = os.getenv("MOVIE_DB_API_KEY")
    if not key:
        return ""
    try:
        response = requests.get(
            TMDB_SEARCH_URL,
            params={"api_key": key, "query": title, "year": year},
            timeout=8,
        )
        response.raise_for_status()
        matches = response.json().get("results", [])
        matched = next(
            (movie for movie in matches if movie.get("title", "").casefold() == title.casefold()
             and (movie.get("release_date") or "")[:4] == str(year)),
            None,
        )
        if matched and matched.get("poster_path"):
            return f"{TMDB_IMAGE_URL}{matched['poster_path']}"
    except (requests.RequestException, ValueError) as error:
        print(f"  Poster unavailable for {title}: {error}")
    return ""


def seed_movies():
    with app.app_context():
        existing_titles = {
            title.casefold()
            for title in db.session.scalars(select(Movie.title)).all()
        }
        added = 0
        for sample in SAMPLE_MOVIES:
            if sample["title"].casefold() in existing_titles:
                print(f"Skipping existing movie: {sample['title']}")
                continue
            movie = Movie(
                **sample,
                img_url=poster_url(sample["title"], sample["year"]),
            )
            db.session.add(movie)
            existing_titles.add(sample["title"].casefold())
            added += 1
            print(f"Added: {sample['title']}")
        db.session.commit()
        print(f"Done! Added {added} movie(s). Existing movies were not changed.")


if __name__ == "__main__":
    seed_movies()
