from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Newspaper(Base):
    __tablename__ = "newspaper"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
