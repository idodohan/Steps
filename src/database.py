from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """
    represents user model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref="user")

    def __repr__(self) -> str:
        return f'User: {self.username}'


class Post(db.Model):
    """
    represents post model
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(80), default="")
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<<By:{self.user.username}|Title:{self.title}|Body:{self.body}|Created at:{self.created_at}>>"


class Statistic(db.Model):
    """
    the idea behind storing these parameters in the db is in order to keep tracking the average even if the server shuts down.
    there isnt a calculated col of average because its less efficient than calculating only when requested.

    the reason i included number_of_posts in here is beacuse it is more efficient than the count function.
    (downside is- if someone manually edits the db it can get out of sync. but i still chose to implement it that way
    because you shouldnt change the db manually, plus you can always create a 'sync' function)
    """
    id = db.Column(db.Integer, primary_key=True)
    number_of_requests = db.Column(db.Integer, default=0)
    total_runtime = db.Column(db.Float, default=0)
    number_of_posts = db.Column(db.Integer, default=0)


