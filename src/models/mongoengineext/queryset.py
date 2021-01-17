from mongoengine import QuerySet
from mongoengine.errors import DoesNotExist
from werkzeug.exceptions import BadRequest, NotFound



class BaseQueryset(QuerySet):

    def _first_or_raise(self, exc, msg=None):
        obj = self.first()
        if obj is None:
            raise exc(msg)
        return obj

    def first_or_400(self, msg=''):
        return self._first_or_raise(BadRequest, msg)

    def first_or_404(self, msg=''):
        return self._first_or_raise(NotFound, msg)

    

