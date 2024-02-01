import logging
import pathlib
import atexit


logger = logging.getLogger("app")


def setup_logging():
    config_file = pathlib.Path("stderr-file.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main():
    setup_logging()


if __name__ == "__main__":
    main()