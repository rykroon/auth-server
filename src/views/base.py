from flask import g, request
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

        return param

    def get_document(self, doc_cls, **kwargs):
        doc = doc_cls.objects.filter(**kwargs).first()
        if doc is None:
            raise BadRequest("Invalid '{}'.".format(doc_cls.__name__))
        return doc

    @classmethod
    def register_api(cls, blueprint, url, pk='id', pk_type='int', create=False, list_=False, get=False, update=False, delete=False):
        view_func = cls.as_view(cls.__name__)
        if create:
            blueprint.add_url_rule(url, view_func=view_func, methods=['POST'])

        if list_:
            blueprint.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET'])

        if get or update or delete:
            z = zip(('GET', 'UPDATE', 'DELETE'), (get, update, delete))
            methods = [m for m, b in z if b]
            blueprint.add_url_rule('{}<{}:{}>'.format(url, pk_type, pk),
                view_func=view_func,
                methods=methods
            )


class APIView(MethodView):
    #inspired by Django Rest Framework

    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def dispatch_request(self):
        self._perform_authentication()
        self._check_permissions()
        self._check_throttles()
        return super().dispatch_request()

    def _perform_authentication(self):
        for auth_class in self.authentication_classes:
            authenticator = auth_class()
            g.client = authenticator.authenticate()
            if g.client is not None:
                return

        self._not_authenticated()

    def _not_authenticated(self):
        pass

    def _check_permissions(self):
        pass

    def _check_throttles(self):
        pass

        

