from sanic import Sanic
from module import Init
from config import app as app_config
import asyncio

""" sanic module """
app = Sanic()

""" for blueprint registration """
Init(app)

if __name__ == "__main__":
    server = app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG,
        workers=app_config.WORKERS)

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(server)
    loop.run_forever()
