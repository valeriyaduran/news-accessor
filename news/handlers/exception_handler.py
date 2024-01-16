import time

from loguru import logger


class RequestSleep:
    @staticmethod
    def sleep_before_new_request(response) -> None:
        if response.status == 429:
            try:
                seconds_retry_after = int(response.headers["Retry-After"])
                logger.info(f"Retry after {seconds_retry_after}")
            except KeyError:
                logger.info("'Retry-After' key error")
                seconds_retry_after = 60
            logger.info(f"Waiting for {seconds_retry_after} seconds and trying to send request again...")
            time.sleep(seconds_retry_after)
        else:
            logger.info(f"Waiting for 60 seconds and trying to send request again...")
            time.sleep(60)
