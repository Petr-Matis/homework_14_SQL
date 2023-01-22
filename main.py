from flask import Flask, jsonify
from utils import get_one, get_all

app = Flask(__name__)


@app.get('/movie/<title>')
def get_by_title(title):
    query = f"""
    SELECT * FROM netflix
    WHERE title = '{title}'
    ORDER BY date_added desc
    """

    query_result = get_one(query)

    if query_result is None:
        return jsonify(status=404)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'description': query_result['description'],
    }

    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_by_year(year1, year2):
    query = f"""
    SELECT * FROM netflix
    WHERE release_year BETWEEN {year1} and {year2}    
    LIMIT 100
    
    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'release_year': item['release_year'],
            }
        )
    return jsonify(result)


@app.get('/rating/<rating>')
def get_movie_by_rating(rating):
    if rating == 'children':
        query = f"""
            SELECT * FROM netflix
            WHERE rating = 'G'   
            LIMIT 100
            """

    elif rating == 'family':
        query = f"""
        SELECT * FROM netflix
        WHERE rating = 'G'  or  rating = 'PG' or rating = 'PG-13'
        LIMIT 100
        """

    elif rating == 'adult':
        query = f"""
        SELECT * FROM netflix
        WHERE rating = 'R'  or  rating = 'NC-17' 
        LIMIT 100
        """
    else:
        return jsonify(status=404)

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'rating': item['rating'],
                'description': item['description'],
            }
        )
    return jsonify(result)


@app.get('/genre/<genre>')
def get_movie_by_genre(genre):
    query = f"""
    SELECT * FROM netflix
    WHERE listed_in = '{genre}'    
    LIMIT 10

    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )
        print(str(genre))
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
