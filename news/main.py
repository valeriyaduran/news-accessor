from aiohttp import web

from news import views

app = web.Application()
app.router.add_get("/", views.index)


if __name__ == '__main__':
    web.run_app(app=app)
