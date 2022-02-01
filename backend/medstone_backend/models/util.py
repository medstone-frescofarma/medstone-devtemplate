from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column, DateTime

class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class EmailType(sa.types.TypeDecorator):
    impl = sa.Unicode

    def __init__(self, length=255, *args, **kwargs):
        super(EmailType, self).__init__(length=length, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.lower()
        return value

    @property
    def python_type(self):
        return self.impl.type.python_type
