# 🎬 Movie Ranking Web App

A movie collection and ranking web application built with **Python, Flask, SQLAlchemy, and SQLite**. Search for movies using **The Movie Database (TMDB) API**, add them to a personal list, rate and review them, and display a ranking based on ratings.

## Features

- Search for movies by title using the TMDB API
- Choose a movie from search results and retrieve its details
- Save movie information in a local SQLite database
- Add ratings and written reviews
- Automatically rank saved movies by rating
- Update ratings and reviews or remove movies from the collection
- View the movie collection in a Flask-rendered web interface

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, Flask-SQLAlchemy / SQLAlchemy
- **Forms:** Flask-WTF, WTForms
- **Frontend:** HTML templates, Bootstrap (via Flask-Bootstrap)
- **External API:** [The Movie Database (TMDB)](https://developer.themoviedb.org/docs/getting-started)
- **HTTP client:** `requests`
- **Configuration:** `python-dotenv`

## Project Structure

```text
movie-ranking-app/
├── main.py
├── templates/
│   ├── index.html
│   ├── add.html
│   ├── select.html
│   └── edit.html
├── static/               
├── requirements.txt      
└── README.md
```

## How It Works

1. **Browse saved movies:** The home page loads movies from SQLite and calculates their rankings based on rating.
2. **Search:** The add-movie form sends a movie title to TMDB's search endpoint.
3. **Select:** The app displays matching movies so you can choose the intended title.
4. **Save:** It retrieves the selected movie's details from TMDB and creates a database record.
5. **Rate and review:** You can enter or edit your own rating and review.
6. **Update ranking:** The home page recalculates positions based on ratings.
7. **Delete:** You can remove a movie from the database.

## Routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Show saved movies and rankings |
| GET, POST | `/add` | Display the search form and search TMDB |
| GET | `/find?id=<tmdb_id>` | Retrieve and save a selected movie |
| GET, POST | `/edit?id=<movie_id>` | Display and submit rating/review edits |
| POST | `/delete?id=<movie_id>` | Delete a saved movie |

## Database Model

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String | Unique movie title |
| `year` | Integer | Release year |
| `description` | String | Movie overview |
| `rating` | Float, nullable | Personal rating |
| `ranking` | Integer, nullable | Calculated ranking |
| `review` | String, nullable | Personal review |
| `img_url` | String | Poster image URL |


## Acknowledgments

Movie metadata is provided by [TMDB](https://www.themoviedb.org/). This project is not endorsed or certified by TMDB.

## License

This repository is shared for educational and portfolio purposes.
