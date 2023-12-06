from UI import UI
import logging
import os
import threading
import json


def check_for_folders(logger):
    try:
        if not os.path.exists("Downloads"):
            logger.info("Downloads folder not found")
            logger.info("Creating Downloads folder")
            os.mkdir("Downloads")
        if not os.path.exists("Video"):
            logger.info("Video folder not found")
            logger.info("Creating Video folder")
            os.mkdir("Video")
    except Exception as e:
        logger.error("Error creating Downloads folder")
        logger.error(e)


def check_settings(logger):
    # reading json
    try:
        with open('settings.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            return json_object
    except Exception as e:
        print(e)
        return None


class Client:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.protocol = ['closed', 'restart']
        self.logger = logging.getLogger(__name__)
        self.logger.info("Checking for folders")
        check_for_folders(self.logger)
        self.settings = check_settings(self.logger)
        self.logger.info("Starting client")

        self.status = self.start()

        self.logger.info("Closing Client")

    def start(self):
        try:
            settings = UI(self.logger, self.settings)

            if settings.currentDelete:
                self.logger.info("Deleting mp4 file")
                # TODO: Delete mp4 file

            return self.protocol[0]
        except Exception as e:
            self.logger.error("Error starting UI")
            self.logger.error(e)
            return self.protocol[0]


if __name__ == '__main__':
    try:
        app = threading.Thread(target=Client)
        app.start()
        app.join()
    except Exception as e:
        logging.error({e})
