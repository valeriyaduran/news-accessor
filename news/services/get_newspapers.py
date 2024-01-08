import asyncio
import json
from datetime import datetime

from aiohttp import ClientSession, TCPConnector

# from bs4 import BeautifulSoup
from loguru import logger

from news.handlers.exception_handler import RequestSleep
from news.services.fill_in_news_db import insert_newspapers_data_into_news_db


class Newspaper:
    def __init__(self) -> None:
        self.base_url: str = "https://news.google.com/newspapers"
        self.partial_newspaper_url: str = "https://news.google.com/newspapers?nid="
        self.news_urls: dict = {}
        self.max_left_retries: int = 5

    # async def parse_news_page_to_get_news_urls(self) -> dict:
    #     async with ClientSession(connector=TCPConnector(ssl=False)) as session:
    #         async with session.get(url=self.base_url) as response:
    #             page_content = await response.text()
    #             if response.status == 200:
    #                 soup = BeautifulSoup(page_content, "html.parser")
    #                 a_tags = soup.find_all("a")
    #                 for a_tag in a_tags:
    #                     newspaper_link = a_tag.get("href")
    #                     if newspaper_link and self.partial_newspaper_url in newspaper_link:
    #                         newspaper_name = a_tag.text
    #                         self.news_urls[newspaper_link] = {"name": newspaper_name}
    #             else:
    #                 while self.max_left_retries > 0:
    #                     logger.error(f"Request error for url {self.base_url}. Status code = {response.status}")
    #                     RequestSleep.sleep_before_new_request(response=response)
    #                     self.max_left_retries -= 1
    #                     await self.parse_news_page_to_get_news_urls()
    #     return self.news_urls

    async def get_image_urls(self, news_url) -> dict:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=news_url) as response:
                # page_content = await response.text()
                # soup = BeautifulSoup(page_content, "html.parser")
                # script_tag_data = soup.select("script:contains('editions')")
                # for tag in script_tag_data:
                #     text_in_tag = tag.text
                #     summary_data = \
                #     json.loads("{" + "{".join(text_in_tag.split("{")[1:]).replace(text_in_tag.split("}")[-1], ""))[
                #         "summary_data"]
                #     for data in summary_data:
                #         try:
                #             for edition in data["editions"]:
                #                 self.news_urls[news_url].update({"img_url": edition["img_url"]})
                #                 self.news_urls[news_url].update({"date": datetime.strptime(edition["date"],
                #                                                                            "%Y%m%d").date()})
                for news in self.news_urls:
                    await insert_newspapers_data_into_news_db(newspaper_data=self.news_urls[news])
            # except KeyError:
            #     pass
        return self.news_urls

    async def main(self) -> dict:
        # await self.parse_news_page_to_get_news_urls()
        self.news_urls = {'https://news.google.com/newspapers?nid=5LPo_wSKItgC':
                              {'name': 'A Propos',
                               'img_url': 'https://news.google.com/newspapers?id=fMgjAAAAIBAJ&sjid=QUEDAAAAIBAJ&pg=2768,4674218&img=1&zoom=1',
                               'date': '19740808'},
                          'https://news.google.com/newspapers?nid=2LRQiq5aZigC':
                              {'name': "A'tome",
                               'img_url': 'https://news.google.com/newspapers?id=M7plAAAAIBAJ&sjid=IY4NAAAAIBAJ&pg=5760,558656&img=1&zoom=1',
                               'date': '19740926'},
                          'https://news.google.com/newspapers?nid=AkQCnCHIR28C':
                              {'name': "L'Abeille",
                               'img_url': 'https://news.google.com/newspapers?id=rq1CAAAAIBAJ&sjid=Q6sMAAAAIBAJ&pg=2216,3436672&img=1&zoom=1',
                               'date': '18280407'},
                          'https://news.google.com/newspapers?nid=AXPGKjj_ei8C':
                              {'name': "L'Abeille Canadienne",
                               'img_url': 'https://news.google.com/newspapers?id=bOpJAAAAIBAJ&sjid=CisDAAAAIBAJ&pg=3000,280056&img=1&zoom=1',
                               'date': '18840208'}}
        tasks = [asyncio.create_task(self.get_image_urls(news_url=news_url)) for news_url in self.news_urls]
        await asyncio.gather(*tasks)
        return self.news_urls


if __name__ == "__main__":
    newspaper = Newspaper()
    asyncio.run(newspaper.main())
