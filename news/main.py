from aiohttp import web

from news import views


class ServerSetup:
    def __init__(self):
        self.application: web.Application = web.Application()

    def setup_routes(self) -> None:
        self.application.router.add_get("/", views.index)

    # def setup_accessors(self) -> None:
    #     self.application["engine"] = PostgresAccessor()
    #     self.application["engine"].setup_pg_accessor(application=self.application)

    def init_app(self):
        # self.setup_accessors()
        self.setup_routes()


server_setup = ServerSetup()
server_setup.init_app()
web.run_app(app=server_setup.application)
