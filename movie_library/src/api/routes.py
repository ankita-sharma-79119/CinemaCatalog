from flask import (
    render_template, 
    session, 
    Blueprint, 
    redirect, 
    request,
    current_app,
    url_for)
from movie_library.src.api.imdb import get_imdb_data

pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)

now_playing = []
genre_ids = dict()

# Main Homepage Route
@pages.route("/homepage")
def homepage():
    if len(now_playing) == 0:
        url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
        now_playing.extend(get_imdb_data(url).get("results"))

    get_genre_ids()

    popular = get_data(1)
    return render_template("index.html", 
                           now_playing = now_playing[:6],
                           popular = popular[:6],
                           genres_ids = genre_ids)

@pages.route("/")
def homepage_redirect():
    return redirect("homepage")

@pages.route("/popular/<int:selected>/<int:current>")
def popular_page(selected: int, current: int):
    movies_list = get_data(selected)
    page_start = current

    if selected-current>2:
        page_start = selected
    
    if selected < current:
        page_start = selected-2

    return render_template("popular.html", 
                           popular = movies_list,
                           genres_ids = genre_ids,
                           selected_page = selected,
                           starting_page = page_start)

def get_data(page: int):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page="+str(page)
    return get_imdb_data(url).get("results")

def get_genre_ids():
    if len(genre_ids) == 0:
        url = "https://api.themoviedb.org/3/genre/movie/list"
        genre = get_imdb_data(url).get("genres")
        for g in genre:
            genre_ids[g.get('id')] = g.get('name')
    return genre_ids