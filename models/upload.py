from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Upload(Base):
    __tablename__ = 'uploads'

    uid = Column(String(36), primary_key=True)
    filename = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    upload_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    finish_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="uploads")

    def __init__(self, uid, filename, status, user=None):
        self.uid = uid
        self.filename = filename
        self.status = status
        self.user = user
