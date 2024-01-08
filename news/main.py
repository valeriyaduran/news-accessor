from aiohttp import web

from news import views
from news.database.accessor import PostgresAccessor


class ServerSetup:
    def __init__(self):
        self.application: web.Application = web.Application()

    def setup_routes(self) -> None:
        self.application.router.add_get("/", views.index)

    def setup_accessors(self) -> None:
        self.application["engine"] = PostgresAccessor()
        self.application["engine"].setup_pg_accessor(application=self.application)

    def setup_app(self):
        self.setup_accessors()
        self.setup_routes()


if __name__ == "__main__":
    server_setup = ServerSetup()
    server_setup.setup_app()
    web.run_app(app=server_setup.application)