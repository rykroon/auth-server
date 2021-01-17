from flask.views import MethodView
from mongoengine.errors import ValidationError
from werkzeug.exceptions import BadRequest


class APIView(MethodView):
    #inspired by Django Rest Framework

    authentication_classes = []
    permission_classes = []
    throttle_classes = []

    def dispatch_request(self, *args , **kwargs):
        #self._perform_authentication()
        #self._check_permissions()
        #self._check_throttles()

        try:
            return super().dispatch_request(*args, **kwargs)
        except ValidationError as e:
            raise BadRequest(str(e))

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