import pytest
from unittest.mock import patch
from jira import JIRAError
from jf_ingest.utils import (
    RETRY_EXPONENT_BASE,
    RetryLimitExceeded,
    get_wait_time,
    retry_for_429s,
)


MOCK_RETRY_AFTER_TIME = 12345


class MockJiraErrorResponse:
    headers = {"Retry-After": MOCK_RETRY_AFTER_TIME}


MOCKED_429_JIRA_ERROR = JIRAError(
    status_code=429,
    text="This is a spoofed Jira Error",
    response=MockJiraErrorResponse(),
)


def test_get_default_wait_time():
    # Get Default Wait Times
    for retry_num in range(0, 10):
        assert (
            get_wait_time(e=None, retries=retry_num) == RETRY_EXPONENT_BASE ** retry_num
        )


def test_get_wait_times_for_retry_error():
    # Test when we have a valid Error
    mock_error = MOCKED_429_JIRA_ERROR

    assert get_wait_time(mock_error, retries=0) == MOCK_RETRY_AFTER_TIME


def test_get_wait_time_for_non_retry_error():
    mock_non_retry_exception = Exception()
    retries = 5
    assert (
        get_wait_time(mock_non_retry_exception, retries=retries)
        == RETRY_EXPONENT_BASE ** retries
    )


def test_retry_for_429s_timeout():
    def always_raise_429():
        raise MOCKED_429_JIRA_ERROR

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
            raise MOCKED_429_JIRA_ERROR

    with patch("jf_ingest.utils.time.sleep", return_value=0) as m:
        assert retry_for_429s(raise_429_three_times) == success_message
        m.assert_called_with(MOCK_RETRY_AFTER_TIME)


def test_retry_for_429s_with_generic_error():
    def raise_non_429():
        raise Exception("Generic Error Testing")

    with pytest.raises(Exception):
        retry_for_429s(raise_non_429)
