from loguru import logger as lo


def log_unknown_error(e):
    lo.error(f"Unknown Error: {repr(e)} - {traceback.format_exception(type(e), e, e.__traceback__)}")