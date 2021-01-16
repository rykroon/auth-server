from mongoengine import QuerySet
from mongoengine.errors import DoesNotExist
from werkzeug.exceptions import BadRequest, NotFound



class BaseQueryset(QuerySet):

    def get_or_400(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            raise BadRequest

    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            raise NotFound

    

