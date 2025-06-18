from pathlib import Path

import fastapi
import fastapi_chameleon
import uvicorn
from starlette.staticfiles import StaticFiles

from data import db_session
from views import account
from views import home
from views import packages
from views import blog

app = fastapi.FastAPI()  # docs_url=None, redoc_url=None)


def main():
    configure(dev_mode=True)
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)


def configure(dev_mode: bool):
    configure_templates(dev_mode)
    configure_routes()
    configure_db(dev_mode)


def configure_templates(dev_mode: bool):
    folder = Path(__file__).parent
    template_folder = str(folder / 'templates')
    print(f"Loading templates from: {template_folder}")
    fastapi_chameleon.global_init(template_folder, auto_reload=dev_mode)


def configure_routes():
    app.mount('/static', StaticFiles(directory='static'), name='static')
    app.include_router(home.router)
    app.include_router(account.router)
    app.include_router(packages.router)
    app.include_router(blog.router)


def configure_db(dev_mode: bool):
    file = (Path(__file__).parent / 'db' / 'pypi.sqlite').absolute()
    db_session.global_init(file.as_posix())


if __name__ == '__main__':
    main()
else:
    configure(dev_mode=False)
