from flask import Blueprint, jsonify
from src.database import User, Post,Statistic, db
from sqlalchemy import func, desc
from src.constants.http_status_codes import HTTP_200_OK

statistics_blueprint = Blueprint("statistics", __name__, url_prefix="/api/v1/statistics")

@statistics_blueprint.route('/topcreators', methods=['GET'])
def get_top_creators():
    """
    :return: returns the 10 top creators (creators with the highest amount of posts in descending order
    """
    top_creators = db.session.query(User, func.count(Post.posted_by).label('total'))\
        .join(Post)\
        .group_by(User)\
        .order_by(desc('total'))\
        .limit(10).all()


    return jsonify({
        'top_creators': f"{top_creators}"
    }), HTTP_200_OK


@statistics_blueprint.route('/runtimes', methods=['GET'])
def get_average_runtime():
    """
    :return: returns the average runtime of the GET/POST posts methods.
    """
    statistic = db.session.query(Statistic).first()
    average_runtime = statistic.total_runtime / statistic.number_of_requests

    return jsonify({
        'average_runtime': f"{average_runtime}"
    }), HTTP_200_OK


def add_statistics_to_db(runtime: float, new_record=True) -> None:
    """
    :param runtime: runtime of function in ms
    :param new_record: if the method type that called this function is POST, update number_of_posts
    :return:
    """
    statistic = db.session.query(Statistic).first()
    statistic.total_runtime += runtime
    statistic.number_of_requests += 1

    if new_record:
        statistic.number_of_posts += 1  # obviously, if post is deleted it should be -= 1, but there isnt implementation for delete_post

    db.session.commit()
