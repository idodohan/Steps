from flask import Flask
from src.database import db
from src.posts import posts_blueprint
from src.users import users_blueprint
from src.statistics import statistics_blueprint
from src.miscellaneous import miscellaneous_blueprint
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(SECRET_KEY=os.environ.get("SECRET_KEY"),
                                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                                SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"))
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    # register all blueprints
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(statistics_blueprint)
    app.register_blueprint(miscellaneous_blueprint)

    return app
