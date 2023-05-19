import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from movie_library.src.api.routes import pages
from movie_library.src.api.movie_route import movie_route
from movie_library.src.api.user_route import user_route

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
    )
    app.db = MongoClient(app.config["MONGODB_URI"]).cinema_catalog

    app.register_blueprint(pages)
    app.register_blueprint(movie_route)
    app.register_blueprint(user_route)
    return app