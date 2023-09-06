from loguru import logger as lo
from prometheus_client import Counter


def cnter_inc(prometheus_cnter: Counter, *args):
    try:
        prometheus_cnter.labels(*args).inc()
    except Exception as e:
        lo.error(f"Failed to increase prometheus counter {prometheus_cnter} with args {args} due to {e}")