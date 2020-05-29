# IMDb_crawler

Crawler that return list of movies given:
- list of genres (optional);
- minimum year;
- minimum average of imdb score and metacritic score (between 0 and 10);
- pages per genre, 200 pages maximum (each pages loads 50 movies);

movies list is saved in the file "found_movies.csv" and it's sorted by average rating

# Run

### Install dependencies

`pip install -r requirements.txt`

### Example of usage

`python imdb_crawler.py comedy sci-fi action 2010 8 5`
