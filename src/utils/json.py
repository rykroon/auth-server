from datetime import datetime, date, time
from decimal import Decimal
import json
from uuid import UUID


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.decode()

        if isinstance(o, (datetime, date, time)):
            return o.isoformat()

        if isinstance(o, Decimal):
            return float(o)

        if isinstance(o, UUID):
            return str(o)

        return super().default(o)


class JSONDecoder(json.JSONDecoder):
    pass