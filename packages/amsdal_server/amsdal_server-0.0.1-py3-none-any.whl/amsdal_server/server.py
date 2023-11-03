import uvicorn
from amsdal_utils.lifecycle.enum import LifecycleEvent
from amsdal_utils.lifecycle.producer import LifecycleProducer
from fastapi import FastAPI
from fastapi import responses
from pydantic import ValidationError

from amsdal_server.apps.common.error_handlers.validation_error_handler import validation_error_handler
from amsdal_server.apps.common.middlewares.utils import init_middlewares
from amsdal_server.apps.router import init_routers
from amsdal_server.configs.main import settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    docs_url='/docs' if settings.IS_DOCS_ENABLED else None,
    default_response_class=responses.ORJSONResponse,
)
init_routers(app)
init_middlewares(app)

app.exception_handler(ValidationError)(validation_error_handler)

app.on_event('startup')(lambda: LifecycleProducer.publish(LifecycleEvent.ON_SERVER_STARTUP))


def start(*, is_development_mode: bool = False) -> None:
    _app = '__main__:app' if is_development_mode else app
    """Start the server."""
    uvicorn.run(
        _app,  # type: ignore[arg-type]
        host=settings.HOST,
        port=settings.PORT,
        # We already log in LoggerMiddleware
        # no need to duplicate these logs with uvicorn
        access_log=False,
        reload=is_development_mode,
    )


if __name__ == '__main__':
    start(is_development_mode=True)
