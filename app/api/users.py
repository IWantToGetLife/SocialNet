from flask import jsonify, current_app, url_for, request
from . import api
from ..models import User


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
