from news.config import session_maker
from news.models import Newspaper


async def insert_newspapers_data_into_news_db(newspaper_data: dict) -> None:
    with session_maker() as session:
        session.add(
            Newspaper(name=newspaper_data["name"],
                      date=newspaper_data["date"],
                      image_url=newspaper_data["img_url"])
        )
        session.commit()
