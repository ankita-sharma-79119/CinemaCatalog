import datetime
import functools
import re
from movie_library.src.api.imdb import get_imdb_data
from movie_library.src.api. routes import get_genre_ids

from flask import (
    Blueprint, 
    current_app, 
    redirect, 
    render_template,
    request,
    url_for,
    session
)

movie_route = Blueprint("movie_route", __name__, static_folder='static', template_folder='templates')

# Define a login required method
def login_required(movie_route):
    @functools.wraps(movie_route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for('user_route.login'))
        else:
            return movie_route(*args, **kwargs)
    return route_wrapper

# View a movie details
@movie_route.get("/movie/<string:id>")
def movie(id: str):
    movie_data = get_imdb_data("https://api.themoviedb.org/3/movie/"+id)
    genre = list()

    for gen in movie_data.get('genres'):
        genre.append(gen.get('name'))

    reviews = list()
    directors = list()
    producers = list()
    writers = list()
    actors = dict()

    recomm = get_recommendations(id)
    popularity = round(movie_data.get('vote_average'), 1)

    get_cast_details(id, directors, producers, writers, actors)
    return render_template("show_movie.html", 
                            movie=movie_data,
                            genres = genre,
                            popularity = popularity,
                            recommendations = recomm,
                            genres_ids = get_genre_ids(),
                            actors=actors,
                            directors=directors,
                            producers=producers,
                            writers=writers)

def get_cast_details(id, directors, producers, writers, actors):
    credit_data = get_imdb_data("https://api.themoviedb.org/3/movie/"+id+"/credits")

    cast_data = credit_data.get("cast")
    for dt in cast_data:
        actors[dt.get('order')] = {'name': dt.get('name'), 
                                   'profile_pic': dt.get('profile_path')}

    crew_data = credit_data.get("crew")
    for dt in crew_data:
        if dt.get('job') == 'Director':
            directors.append(dt.get('name'))
        elif dt.get('job') == 'Producer':
            producers.append(dt.get('name'))
        elif dt.get('job') == 'Writer':
            writers.append(dt.get('name'))

def get_recommendations(id):
    url = "https://api.themoviedb.org/3/movie/"+id+"/recommendations?page=1"
    recomm = get_imdb_data(url).get("results")
    return recomm


def get_reviews(id, reviews):
    reviews = get_imdb_data("https://api.themoviedb.org/3/movie/"+id+"/reviews?page=1").get("results")

    for rev in reviews:
        print(rev.get("created_at"))
        created_at = re.search('\d{4}-\d{2}-\d{2}', str(rev.get("created_at")))

        reviews.append({"author": rev.get("author"), 
                        "review": rev.get("content"), 
                        "created_at": created_at})
    
    print(reviews)












# Rate a movie
@movie_route.route("/movie/rate/<string:id>", methods=["GET"])
@login_required
def rate_movie(id):
    rating = int(request.args.get("rating"))
    current_app.db.movie.update_one({"movie_Id": id}, {"$set": {"rating": rating}})
    return redirect(url_for(".movie", id=id))

# Update last watched of movie
@movie_route.route("/movie/last_watched/<string:id>", methods=["GET"])
@login_required
def last_watched_update(id):
    current_app.db.movie.update_one({"movie_Id": id}, {"$set": {"last_watched": datetime.datetime.today()}})
    return redirect(url_for(".movie", id=id))

# Update last watched of movie
@movie_route.route("/watchlist", methods=["GET"])
@login_required
def get_watchlist(id):
    print("watchlist")
    return redirect(url_for("pages.homepage_redirect"))