from flask import Blueprint, request, jsonify
from src.database import Post, db
from datetime import datetime
from src.statistics import add_statistics_to_db
from src.users import get_user_by_id
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from src.utilities import start_time_measure, end_time_measure

posts_blueprint = Blueprint("posts", __name__, url_prefix="/api/v1/posts")


@posts_blueprint.route('', methods=['GET'])
def get_posts():
    """
    request expects from_date=date from which to filter, number_of_posts=number of posts to return
    if from_date is empty take current date == dont filter by date
    if number_of_posts is empty take -1 posts == take all posts
    :return:
    """
    start_time = start_time_measure()

    from_date = request.json['from_date'] if request.json['from_date'] else datetime.now()
    number_of_posts = request.json['number_of_posts'] if request.json['number_of_posts'] else -1

    posts_to_return = db.session.query(Post).filter(Post.created_at <= from_date).filter(Post.created_at <= from_date).order_by(Post.created_at).limit(number_of_posts).all()

    add_statistics_to_db(end_time_measure(start_time), new_record=False)


    return jsonify({
        'posts': f"{posts_to_return}"
    }), HTTP_200_OK


@posts_blueprint.route('', methods=['POST'])
def post_post():
    """
    creates a new post
    request expects:
     created_at: date in which the post has been created. if empty take current time
     posted_by: user_id
     title: post title
     body: REQUIRED! body of the post
    :return:
    """
    start_time = start_time_measure()

    created_at = request.json['created_at'] if request.json['created_at'] else datetime.now()
    posted_by = request.json['posted_by']  # assuming this is the frontend responsibility
    title = request.get_json().get('title')
    body = request.json['body']

    # finds the user object by its id
    user = get_user_by_id(posted_by)

    # body is required
    if not body:
        return jsonify({'error': "You forgot to enter the body"}), HTTP_400_BAD_REQUEST

    # creates a new post
    post = Post(created_at=created_at, user=user, title=title, body=body)

    # updates the db
    db.session.add(post)
    db.session.commit()

    add_statistics_to_db(end_time_measure(start_time), new_record=True)

    return jsonify({
        'message': "Post created",
        'post': {
            'title': title,
            'body': body,
            'posted_by': user.username,
            'created_at': created_at
        }

    }), HTTP_201_CREATED