from flask import Blueprint
from .base import BaseView


bp = Blueprint('users', __name__)


class UserView(BaseView):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


user_view = UserView.as_view('UserView')
bp.add_url_rule('/users', view_func=user_view, methods=['POST'])