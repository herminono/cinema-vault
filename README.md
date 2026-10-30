# cinema-vault
This is a personal movie collection web application built  using Flask. It allows users to discover, rate, and review their favourite movies, and also organize their collection with genre and rating-based filters.
This application integrates with The Movie Database (TMDB) API to retrieve movie information, including titles, release dates, descriptions, genres, and posters.

Features:
1. Search for movies using the TMDB API.
2. Add and manage your favourite movies.
3. Rate movies on a scale of 0 to 10.
4. Write and edit personal movie reviews.
5. Filter movies by genre.
6. Display movies within a specified minimum and maximum rating.
7. Search using both genre and rating criteria simultaneousely.
8. Sort movies based on their ratings.
9. Update ratings and delete movies.
10. A vintage cinema-inspired design using a dark maroon, cream, and sage colour palette.
11. Populate the database with example movies using seed.py

Technologies Used:
1. Python > Backend programming
2. Flask > Web framework
3. Flask-SQLAlchemy > Database integration
4. SQLite > Database management
5. Flask-WTF > Form handling and validation
6. HTML, Jinja > Dynamic page rendering
7. CSS > User interface styling
8. Bootstrap 5 > Responsive UI components
9. TMDB API > Movie data retrieval
## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholder URL with your repository's URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies used in the app:

```bash
pip install flask flask-bootstrap flask-sqlalchemy flask-wtf wtforms python-dotenv requests
```

You can then generate a requirements file with `pip freeze > requirements.txt` after verifying your environment contains only the project's required packages.

### 4. Configure the TMDB API key

Get an API key from [TMDB](https://www.themoviedb.org/settings/api) and create a `.env` file in the project root:

```dotenv
MOVIE_DB_API_KEY=your_tmdb_api_key
```

The code uses `load_dotenv()` and reads `MOVIE_DB_API_KEY` from the environment.

**Security note:** The shared version of `main.py` hardcodes Flask's `SECRET_KEY`. Before publishing or deploying, replace it with an environment variable, for example:

```python
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
```

Then add `FLASK_SECRET_KEY` to your private `.env` file.

### 5. Run the app

```bash
python main.py
```

Open **http://127.0.0.1:5000/** in your browser.

On startup, the app creates missing database tables with `db.create_all()`. A fresh database will initially have no saved movies.

How it works:
1. Movie discovery
Users can search for a movie by entering its title. CinemaVault sends a request to the TMDB API and displays matching results. After selecting a movie, the application retrieves its details and saves them to the SQLite database.
2. Rating and reviews
Users can assign a personal rating between 0 and 10 and write a review for each movie. Saved ratings  determine the order in which movies appear in the collection.
3. Genre and rating filter
CinemaVault supports two filtering methods:
a. Genre Filtering > Users can select a genre to display movies belonging to that category.
b. Rating Range Filtering > Users can specify minimum and maximum ratings to display movies within that interval.
#both filters can be applied simultaneously.

Database:
CinemaVault uses SQLite through Flask-SQLAlchemy.
The database is created automatically when the application starts.

Project Origin & Acknowledgements:
CinemaVault was initially developed by following a Python web development tutorial, which introduced the fundamentals of Flask, SQLAlchemy, database management, and external API integration.
The original project was then subsequently extended and customized with additional features and improvements, including:
1. added the ability to filter movies based on their genres.
2. implemented minimum and maximum rating filters to allow more specific searches.
3. extended the database model to store movie genres retrieved from the TMDB API.
4. added a seed.py script to populate the database with example movies.
5. redesign the frontend with AI assistance, introducing a vintage cinema-inspired aesthetic, responsive layouts, and improved navigation.

License
This project is intended for educational and portfolio purposes.
