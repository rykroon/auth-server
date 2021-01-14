from datetime import datetime
import uuid
from mongoengine import Document, QuerySet
from mongoengine.errors import DoesNotExist
from mongoengine.fields import DateTimeField, ObjectIdField, UUIDField
from werkzeug.exceptions import NotFound


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


