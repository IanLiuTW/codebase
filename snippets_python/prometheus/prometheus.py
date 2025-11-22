from loguru import logger as lo
from prometheus_client import make_asgi_app, Counter


# In web server like FastAPI, you can expose an endpoint by doing this:
app.mount("/metrics", make_asgi_app())


def cnter_inc(prometheus_cnter: Counter, *args):
    try:
        prometheus_cnter.labels(*args).inc()
    except Exception as e:
        lo.error(f"Failed to increase prometheus counter {prometheus_cnter} with args {args} due to {e}")