import json
from volstreet import config
import requests
from volstreet.config import logger


def notifier(message, webhook_url=None, level="INFO"):
    levels = ["INFO", "CRUCIAL", "ERROR"]
    if levels.index(level) < levels.index(config.NOTIFIER_LEVEL):
        return
    if webhook_url is None or webhook_url is False:
        print(message)
        return
    else:
        notification_url = webhook_url
        data = {"content": message}
        try:
            requests.post(
                notification_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"},
            )
            print(message)
        except requests.exceptions.SSLError as e:
            logger.error(
                f"Error while sending notification: {e}",
                exc_info=(type(e), e, e.__traceback__),
            )
