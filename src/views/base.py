from flask import request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest


class BaseView(MethodView):

    def get_param(self, param_name, required=True, default=None, choices=None):
        """
            :param param_name: The name of the parameter
            :param required: Whether or not the parameter is required
            :param default: The default value of the parameter
            :param choices: The valid choices for the parameter
        """
        param = request.json.get(param_name, default=default)
        if required and param is None:
            raise BadRequest("Missing parameter '{}'.".format(param_name))

        if choices and param not in choices:
            raise BadRequest("Invalid value for parameter '{}'.".format(param_name))

    def get_document(self, document_type, **kwargs):
        doc = document_type.objects.filter(**kwargs).first()
        if doc is None:
            raise BadRequest("Invalid '{}'.".format(document_type.__name__))

