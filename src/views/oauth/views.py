from datetime import datetime, timedelta
import os
from flask import Blueprint, request, jsonify
from flask.views import MethodView
import jwt
import exceptions as exc
from tokens import create_access_token, create_refresh_token, decode_token


oauth = Blueprint('oauth', __name__)

class OauthView(MethodView):

    def get_param(self, param_name, required=True, default=None):
        param_value = request.json.get(param_name, default)
        if required and not param_value:
            raise Exception
        return param_value

