import os

from aiohttp import web
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#
# class PostgresAccessor:
#     def __init__(self) -> None:
#         self.session_maker = None
#
#     def setup_pg_accessor(self, application: web.Application) -> None:
#         application.on_startup.append(self._on_connect)
#
#     async def _on_connect(self, application: web.Application):
#         load_dotenv(dotenv_path=".env.dev")
#         session_maker = sessionmaker(bind=create_engine(url=os.getenv("POSTGRES_URL")))
#         self.session_maker = session_maker
