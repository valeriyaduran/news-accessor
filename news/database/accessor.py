import os

from aiohttp import web
from dotenv import load_dotenv
from sqlalchemy import create_engine


class PostgresAccessor:
    def __init__(self) -> None:
        # self.db = None
        self.engine = None

    def setup_pg_accessor(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        # application.on_shutdown.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application) -> None:
        load_dotenv(dotenv_path=".env.dev")
        self.engine = create_engine(url=os.getenv("POSTGRES_URL"))
        # await db.set_bind(bind=os.getenv("POSTGRES_URL"))
        # self.session_maker = session_maker
    #
    # async def _on_disconnect(self, application: web.Application) -> None:
    #     # if self.db is not None:
    #     #     await self.db.pop_bind().close()
    #     # self.session_maker.close_all()