from jira import JIRAError
from jf_ingest.jf_jira.exceptions import JiraRetryLimitExceeded
import pytest
from unittest.mock import patch

from jf_ingest.jf_jira.auth import (
    JiraAuthConfig,
    JiraAuthMethod,
    JiraAuthenticationException,
    get_jira_connection,
)


def _get_jira_auth_config(args):
    company_slug = "test_company"
    url = "https://test-co.atlassian.net/"
    return JiraAuthConfig(company_slug=company_slug, url=url, **args)


def test_jira_conn_basic_auth_no_auth():
    config = _get_jira_auth_config({"auth_method": JiraAuthMethod.BasicAuth})

    with pytest.raises(RuntimeError) as excinfo:
        get_jira_connection(config)

    assert (
        str(excinfo.value)
        == f"No valid basic authentication mechanism for {config.url} - need a username/password combo or a personal access token"
    )


def test_jira_conn_basic_auth_user_password():
    config = _get_jira_auth_config(
        {
            "auth_method": JiraAuthMethod.BasicAuth,
            "user": "jira_user@test.co",
            "password": "test_password",  # pragma: allowlist secret
        }
    )

    # TEST BASIC AUTH ERROR LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=401)):
        with pytest.raises(JiraAuthenticationException):
            get_jira_connection(config, max_retries=0)

    # TEST BASIC AUTH ERROR LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=403)):
        with pytest.raises(JiraAuthenticationException):
            get_jira_connection(config, max_retries=0)

    # TEST RETRY LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=429)):
        with pytest.raises(JiraRetryLimitExceeded):
            get_jira_connection(config, max_retries=0)


def test_jira_conn_basic_auth_personal_access_token():
    config = _get_jira_auth_config(
        {"auth_method": JiraAuthMethod.BasicAuth, "personal_access_token": "a_PAT"}
    )

    # TEST BASIC AUTH ERROR LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=401)):
        with pytest.raises(JiraAuthenticationException):
            get_jira_connection(config, max_retries=0)

    # TEST BASIC AUTH ERROR LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=403)):
        with pytest.raises(JiraAuthenticationException):
            get_jira_connection(config, max_retries=0)

    # TEST RETRY LOGIC
    with patch("jf_ingest.jf_jira.auth.JIRA", side_effect=JIRAError(status_code=429)):
        with pytest.raises(JiraRetryLimitExceeded):
            get_jira_connection(config, max_retries=0)
