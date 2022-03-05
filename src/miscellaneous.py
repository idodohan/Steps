from flask import Blueprint, jsonify
from src.database import Statistic, db
from src.constants.http_status_codes import HTTP_200_OK

miscellaneous_blueprint = Blueprint("miscellaneous", __name__, url_prefix="/api/v1")

# this file is responsible for all api requests that dont have a spesific blueprint

@miscellaneous_blueprint.route('/postsnumber', methods=['GET'])
def get_posts_count():
    number_of_posts = db.session.query(Statistic).first().number_of_posts

    return jsonify({
        'number of posts': f"{number_of_posts}"
    }), HTTP_200_OK
