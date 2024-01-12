from aiohttp import web

from news.routes import routes

app = web.Application()
app.add_routes(routes=routes)


if __name__ == "__main__":
    web.run_app(app=app)
