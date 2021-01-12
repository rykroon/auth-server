from datetime import datetime
import uuid
from mongoengine import Document, QuerySet
from mongoengine.errors import DoesNotExist
from mongoengine.fields import DateTimeField, ObjectIdField, UUIDField
from werkzeug.exceptions import NotFound


class BaseQuerySet(QuerySet):
    def get_or_404(self, *args, **kwargs):
        """
        Get a document and raise a 404 Not Found error if it doesn't
        exist.
        """
        try:
            return self.get(*args, **kwargs)
        except DoesNotExist:
            message = kwargs.get("message", None)
            raise NotFound(message)

    def first_or_404(self, message=None):
        """Same as get_or_404, but uses .first, not .get."""
        obj = self.first()
        if not obj:
            raise NotFound(message)
        return obj


class BaseDocument(Document):
    meta = {
        'abstract': True,
        'queryset_class': BaseQuerySet
    }

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    date_created = DateTimeField(required=True, default=datetime.utcnow)
    date_updated = DateTimeField(required=True)
    date_deleted = DateTimeField(null=True)

    def clean(self):
        self.date_updated = datetime.utcnow()


