from datetime import datetime
import uuid
from mongoengine import Document
from mongoengine.errors import DoesNotExist
from mongoengine.fields import DateTimeField, UUIDField
from werkzeug.exceptions import NotFound
from .queryset import BaseQueryset


class BaseDocument(Document):
    meta = {
        'abstract': True,
        'queryset': BaseQueryset
    }

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    date_created = DateTimeField(required=True, default=datetime.utcnow)
    date_updated = DateTimeField(required=True)
    date_deleted = DateTimeField(null=True)

    def clean(self):
        super().clean()

        fields = list(self._fields) if self.pk is None else self._get_changed_fields()

        if fields:
            self.date_updated = datetime.utcnow()

        for field in fields:
            clean_method_name = '_clean_{}'.format(field)
            clean_method = getattr(self, clean_method_name, None)
            if clean_method:
                clean_method()

    def to_dict(self):
        return {f: getattr(self, f) for f in self._fields}

