import sqlite3


def get_one(query: str):
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def get_all(query: str):
    with sqlite3.connect('netflix.db') as conn:
        conn.row_factory = sqlite3.Row

        result = []

        for item in conn.execute(query).fetchall():
            result.append(dict(item))

        return result


def get_movie_by_criteria(type_movie, release_year, listed_in):
    query = f"""
    SELECT title, description FROM netflix
    WHERE "type" = '{type_movie}'
    AND release_year = '{release_year}'
    AND listed_in LIKE '%{listed_in}%'
    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )

    return result


# print(get_movie_by_criteria('Movie', 2016, 'Thrillers'))

def get_actor_by_criteria(actor_1, actor_2):
    query = f"""
    SELECT "cast" FROM netflix
    WHERE "cast" LIKE '%{actor_1}%'    
    AND "cast" LIKE '%{actor_2}%'
    """

    result = []
    intersection = []
    names = []
    suitable_name = []

    for item in get_all(query):
        result.append(
            {
                'cast': item['cast'],
            }
        )

    for i in result:
        intersection.append(i['cast'].split(', '))

    for group in intersection:
        for name in group:
            names.append(name)

    for name in names:
        if names.count(name) > 2 and name not in suitable_name:
            suitable_name.append(name)

    return suitable_name


# print(get_actor_by_criteria('Rose McIver', 'Ben Lamb'))
