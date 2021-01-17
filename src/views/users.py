from flask import Blueprint, g, jsonify, request
from .base import APIView
from models import User
from rest_framework import HmacAuthentication


bp = Blueprint('users', __name__)


class UserView(APIView):

    authentication_classes = [HmacAuthentication]

    def get(self):
        pass

    def post(self):
        payload = request.get_json()
        user = User(**payload)
        user.client_id = g.client.pk
        user.save()
        return jsonify(user.to_dict())

    def put(self):
        pass

    def delete(self):
        pass


user_view = UserView.as_view('UserView')
bp.add_url_rule('/users', view_func=user_view, methods=['POST'])