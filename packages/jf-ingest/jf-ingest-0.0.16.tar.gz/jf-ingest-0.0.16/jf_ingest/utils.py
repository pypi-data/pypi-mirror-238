import dataclasses
import logging
import gzip
import json
import time
from typing import Any, Callable, Optional

from jira import JIRAError

from jf_ingest import logging_helper

logger = logging.getLogger(__name__)

RETRY_EXPONENT_BASE = 5


class RetryLimitExceeded(Exception):
    pass


class StrDefaultEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return str(o)


class IngestIOHelper:
    def __init__(self, s3_bucket: str, s3_path: str, local_file_path: str):
        self.s3_bucket = s3_bucket
        self.s3_path = (s3_path,)
        # EVERYTHING in this file path will (potentially) be uploaded to S3!
        # DO NOT put any creds file in this path!!!!
        self.local_file_path = local_file_path

    def _get_file_name(self, object_name: str, batch_number: Optional[int] = 0):
        return f'{object_name}{batch_number if batch_number else ""}.json.gz'

    def write_json_data_to_local(
        self,
        object_name: str,
        json_data: dict | list[dict],
        batch_number: Optional[int] = 0,
    ):
        try:
            file_name = self._get_file_name(
                object_name=object_name, batch_number=batch_number
            )
            full_file_path = f"{self.local_file_path}/{file_name}"
            logger.info(f"Attempting to save {object_name} data to {full_file_path}")
            with gzip.open(full_file_path, "w") as f:
                f.write(
                    json.dumps(json_data, indent=2, cls=StrDefaultEncoder).encode(
                        "utf-8"
                    )
                )
                logger.debug(
                    f"File: {full_file_path}, Size: {round(f.tell() / 1000000, 1)}MB"
                )
        except Exception as e:
            logger.error(
                f"Exception encountered when attempting to write data to local file! Error: {e}"
            )

    def upload_files_to_s3(self):
        # TODO: Write multi threaded uploader to upload this local_file_path
        raise NotImplementedError("Function not implemented!")


def get_wait_time(e: Optional[Exception], retries: int) -> int:
    """
    This function attempts to standardize determination of a wait time on a retryable failure.
    If the exception's response included a Retry-After header, respect it.
    If it does not, we do an exponential backoff - 5s, 25s, 125s.

    A possible future addition would be to add a jitter factor.
    This is a fairly standard practice but not clearly required for our situation.
    """
    # getattr with a default works on _any_ object, even None.
    # We expect that almost always e will be a JIRAError or a RequestException, so we will have a
    # response and it will have headers.
    # So I'm choosing to use the getattr call to handle the valid but infrequent possibility
    # that it may not (None or another Exception type that doesn't have a response), rather tha
    # preemptively checking.
    response = getattr(e, "response", None)
    headers = getattr(response, "headers", {})
    retry_after = headers.get("Retry-After")
    if retry_after is not None:
        return int(retry_after)
    else:
        return RETRY_EXPONENT_BASE ** retries


def retry_for_429s(f: Callable[..., Any], *args, max_retries: int = 5, **kwargs) -> Any:
    """
    This function allows for us to retry 429s from Jira. There are much more elegant ways of accomplishing
    this, but this is a quick and reasonable approach to doing so.

    Note:
        - max_retries=5 will give us a maximum wait time of 10m25s.
    """
    for retry in range(max_retries + 1):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            if (
                hasattr(e, "status_code")
                and e.status_code == 429
                and retry < max_retries
            ):
                wait_time = get_wait_time(e, retries=retry)
                logging_helper.log_standard_error(
                    logging.WARNING,
                    # NOTE: Getting the function name here isn't always useful,
                    # because sometimes we circumvent the JIRA standard library
                    # and use functions like "get" and "_get_json", but it's still
                    # better than nothing
                    msg_args=[f.__name__, retry, max_retries, wait_time],
                    error_code=3071,
                )
                time.sleep(wait_time)
                continue
            else:
                raise RetryLimitExceeded(e)
