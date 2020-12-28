from datetime import datetime
import uuid
from mongoengine import Document
from mongoengine.fields import DateTimeField, UUIDField


class BaseModel(Document):
    meta = {
        'abstract': True
    }

    uuid = UUIDField(required=True, default=uuid.uuid4, unique=True)
    date_created = DateTimeField(required=True, default=datetime.utcnow)
    date_updated = DateTimeField(required=True)

    def clean(self):
        self.date_updated = datetime.utcnow()


