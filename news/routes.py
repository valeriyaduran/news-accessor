from aiohttp import web

routes = web.RouteTableDef()


@routes.post('/news')
async def post_handler(request):
    pass
