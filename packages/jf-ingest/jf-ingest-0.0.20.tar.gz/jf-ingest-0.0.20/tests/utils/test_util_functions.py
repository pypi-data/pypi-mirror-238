import logging
import pytest
from unittest.mock import patch
from jira import JIRAError
from jf_ingest.utils import (
    RETRY_EXPONENT_BASE,
    RetryLimitExceeded,
    batch_iterable,
    get_wait_time,
    retry_for_429s,
)

logger = logging.getLogger(__name__)

MOCK_RETRY_AFTER_TIME = 12345


class MockJiraErrorResponseWithRetryAfterAsInt:
    headers = {"Retry-After": MOCK_RETRY_AFTER_TIME}


class MockJiraErrorResponseWithRetryAfterAsStr:
    headers = {"Retry-After": str(MOCK_RETRY_AFTER_TIME)}


class MockJiraErrorResponseWithZeroRetryAfter:
    headers = {"Retry-After": 0}


class MockJiraErrorResponseWithNonIntRetryAfter:
    headers = {"Retry-After": "CAT"}


MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_INT = JIRAError(
    status_code=429,
    text="This is a spoofed Jira Error",
    response=MockJiraErrorResponseWithRetryAfterAsInt(),
)
MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_STR = JIRAError(
    status_code=429,
    text="This is a spoofed Jira Error",
    response=MockJiraErrorResponseWithRetryAfterAsStr(),
)

MOCKED_429_JIRA_ERROR_RETRY_AFTER_IS_ZERO = JIRAError(
    status_code=429,
    text="This is a spoofed Jira Error with Retry After set to 0",
    response=MockJiraErrorResponseWithZeroRetryAfter(),
)

MOCKED_429_JIRA_ERROR_RETRY_AFTER_IS_NOT_INT = JIRAError(
    status_code=429,
    text="This is a spoofed Jira Error with Retry After set to a non int",
    response=MockJiraErrorResponseWithNonIntRetryAfter(),
)


def test_get_default_wait_time():
    # Get Default Wait Times
    for retry_num in range(0, 10):
        assert (
            get_wait_time(e=None, retries=retry_num) == RETRY_EXPONENT_BASE ** retry_num
        )


def test_get_wait_times_for_retry_error():
    # Test when we have a valid Error
    mock_error = MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_INT

    for retry_num in range(0, 5):
        logger.info(f"Retry number {retry_num}...")
        assert get_wait_time(mock_error, retries=retry_num) == MOCK_RETRY_AFTER_TIME


def test_get_wait_times_for_retry_error_when_retry_is_str():
    # Test when we have a valid Error
    mock_error = MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_STR

    for retry_num in range(0, 5):
        logger.info(f"Retry number {retry_num}...")
        assert get_wait_time(mock_error, retries=retry_num) == MOCK_RETRY_AFTER_TIME


def test_get_wait_times_for_retry_error_non_zero():
    # Test when we have a valid Error
    mock_error = MOCKED_429_JIRA_ERROR_RETRY_AFTER_IS_ZERO

    for retry_num in range(0, 10):
        logger.info(f"Retry number {retry_num}...")
        expected_wait_time = RETRY_EXPONENT_BASE ** retry_num
        # Retry times SHOULD NEVER be zero
        assert get_wait_time(mock_error, retries=retry_num) != 0
        assert get_wait_time(mock_error, retries=retry_num) == expected_wait_time


def test_get_wait_times_for_retry_error_non_zero():
    # Test when we have a valid Error
    mock_error = MOCKED_429_JIRA_ERROR_RETRY_AFTER_IS_NOT_INT

    for retry_num in range(0, 10):
        logger.info(f"Retry number {retry_num}...")
        expected_wait_time = RETRY_EXPONENT_BASE ** retry_num
        # Retry times SHOULD NEVER be zero
        assert get_wait_time(mock_error, retries=retry_num) != 0
        assert get_wait_time(mock_error, retries=retry_num) == expected_wait_time


def test_get_wait_time_for_non_retry_error():
    mock_non_retry_exception = Exception()
    retries = 5
    assert (
        get_wait_time(mock_non_retry_exception, retries=retries)
        == RETRY_EXPONENT_BASE ** retries
    )


def test_retry_for_429s_timeout():
    def always_raise_429():
        raise MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_INT

    with patch("jf_ingest.utils.time.sleep", return_value=0) as m:
        with pytest.raises(RetryLimitExceeded):
            retry_for_429s(always_raise_429)

        try:
            retry_for_429s(always_raise_429)
        except RetryLimitExceeded:
            m.assert_called_with(MOCK_RETRY_AFTER_TIME)


def test_retry_for_429s_retry_works():
    arg_dict = {"retry_count": 0}
    success_message = "Success!"

    def raise_429_three_times():
        if arg_dict["retry_count"] == 3:
            return success_message
        else:
            arg_dict["retry_count"] += 1
            raise MOCKED_429_JIRA_ERROR_WITH_RETRY_AS_INT

    with patch("jf_ingest.utils.time.sleep", return_value=0) as m:
        assert retry_for_429s(raise_429_three_times) == success_message
        m.assert_called_with(MOCK_RETRY_AFTER_TIME)


def test_retry_for_429s_with_generic_error():
    def raise_non_429():
        raise Exception("Generic Error Testing")

    with pytest.raises(Exception):
        retry_for_429s(raise_non_429)


def test_retry_for_429s_with_jira_non_429_error():
    def raise_non_429():
        raise JIRAError(text="Generic Error Testing", status_code=401)

    with pytest.raises(JIRAError):
        retry_for_429s(raise_non_429)


def test_batch_iterable():
    total_data_size = 85926
    batch_size = 62
    data = [i for i in range(total_data_size)]

    recompiled_batches = []
    for batch in batch_iterable(data, batch_size=batch_size):
        # Assert we are getting proper batch sizes
        assert len(batch) <= batch_size
        recompiled_batches.extend(batch)

    # Assert we got ALL the data
    assert len(recompiled_batches) == total_data_size

    # Assert that data is returned matching and in order
    for i in range(total_data_size):
        assert data[i] == recompiled_batches[i]
