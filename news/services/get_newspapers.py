import asyncio
import json
from asyncio import Semaphore
from datetime import datetime

from aiohttp import ClientSession, TCPConnector

from bs4 import BeautifulSoup
from loguru import logger

from news.config import base_newspaper_url, partial_newspaper_url
from news.handlers.exception_handler import RequestSleep
from news.services.fill_in_news_db import insert_newspapers_data_into_news_db


class Newspaper:
    def __init__(self) -> None:
        self.base_url: str = base_newspaper_url
        self.partial_newspaper_url: str = partial_newspaper_url
        self.news_urls: dict = {}
        self.max_left_retries: int = 5

    async def parse_news_page_to_get_news_urls(self) -> dict:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=self.base_url) as response:
                page_content = await response.text()
                if response.status == 200:
                    soup = BeautifulSoup(page_content, "html.parser")
                    a_tags = soup.find_all("a")
                    for a_tag in a_tags:
                        newspaper_link = a_tag.get("href")
                        if newspaper_link and self.partial_newspaper_url in newspaper_link:
                            newspaper_name = a_tag.text
                            self.news_urls[newspaper_link] = {"name": newspaper_name}
                else:
                    while self.max_left_retries > 0:
                        logger.error(f"Request error for url {self.base_url}. Status code = {response.status}")
                        RequestSleep.sleep_before_new_request(response=response)
                        self.max_left_retries -= 1
                        await self.parse_news_page_to_get_news_urls()
        return self.news_urls

    async def get_image_urls(self, news_url: str, semaphore: Semaphore) -> dict:
        async with semaphore:
            async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                async with session.get(url=news_url) as response:
                    page_content = await response.text()
                    soup = BeautifulSoup(page_content, "html.parser")
                    script_tag_data = soup.select("script:contains('editions')")
                    for tag in script_tag_data:
                        text_in_tag = tag.text
                        summary_data = \
                            json.loads(
                                "{" + "{".join(text_in_tag.split("{")[1:]).replace(text_in_tag.split("}")[-1], ""))[
                                "summary_data"]
                        for data in summary_data:
                            try:
                                for edition in data["editions"]:
                                    self.news_urls[news_url].update({"img_url": edition["img_url"]})
                                    self.news_urls[news_url].update({"date": datetime.strptime(edition["date"],
                                                                                               "%Y%m%d").date()})
                                    await insert_newspapers_data_into_news_db(newspaper_data=self.news_urls[news_url])
                            except KeyError:
                                pass
        return self.news_urls

    async def main(self) -> dict:
        semaphore = asyncio.Semaphore(value=100)
        await self.parse_news_page_to_get_news_urls()
        tasks = [asyncio.create_task(self.get_image_urls(news_url=news_url, semaphore=semaphore))
                 for news_url in self.news_urls]
        await asyncio.gather(*tasks)
        return self.news_urls


if __name__ == "__main__":
    newspaper = Newspaper()
    asyncio.run(newspaper.main())
