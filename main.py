from UI import UI
import logging
import os
import threading


def check_for_folders(logger):
    try:
        if not os.path.exists("Downloads"):
            logger.info("Downloads folder not found")
            logger.info("Creating Downloads folder")
            os.mkdir("Downloads")
    except Exception as e:
        logger.error("Error creating Downloads folder")
        logger.error(e)


def start(logger):

    UI(logger)


class Client:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Checking for folders")
        check_for_folders(self.logger)
        self.logger.info("Starting client")
        start(self.logger)
        self.logger.info("Closing Client")


if __name__ == '__main__':
    app = threading.Thread(target=Client)
    app.start()
    print("Client Started")
    app.join()
    print("Client Closed")

