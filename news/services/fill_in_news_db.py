import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from news.database.db import Newspaper

load_dotenv(dotenv_path=".env.dev")
session_maker = sessionmaker(bind=create_engine(url=os.getenv("POSTGRES_URL")))


async def insert_newspapers_data_into_news_db(newspaper_data: dict) -> None:
    with session_maker() as session:
        session.add(
            Newspaper(name=newspaper_data["name"],
                      date=newspaper_data["date"],
                      image_url=newspaper_data["img_url"])
        )
        session.commit()
