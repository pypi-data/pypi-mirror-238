import json
import os

import requests_mock

from jf_ingest.jf_jira.auth import JiraAuthConfig, get_jira_connection


def get_jira_mock_connection():

    _MOCK_SERVER_INFO_RESP = (
        '{"baseUrl":"https://test-co.atlassian.net","version":"1001.0.0-SNAPSHOT",'
        '"versionNumbers":[1001,0,0],"deploymentType":"Cloud","buildNumber":100218,'
        '"buildDate":"2023-03-16T08:21:48.000-0400","serverTime":"2023-03-17T16:32:45.255-0400",'
        '"scmInfo":"9999999999999999999999999999999999999999","serverTitle":"JIRA",'
        '"defaultLocale":{"locale":"en_US"}} '
    )

    auth_config = JiraAuthConfig(
        url="https://test-co.atlassian.net/",
        personal_access_token="asdf",
        company_slug="test_co",
    )

    with requests_mock.Mocker() as m:
        _register_jira_uri(m, "serverInfo", f"{_MOCK_SERVER_INFO_RESP}")
        _register_jira_uri_with_file(m, "field", "api_responses/fields.json")
        jira_conn = get_jira_connection(config=auth_config, max_retries=1)

    return jira_conn


def get_fixture_file_data(fixture_path: str):
    with open(f"{os.path.dirname(__file__)}/fixtures/{fixture_path}", "r") as f:
        return f.read()


def get_jellyfish_issue_metadata():
    with open(
        f"{os.path.dirname(__file__)}/fixtures/jellyfish_issue_metadata.json", "r"
    ) as f:
        return json.loads(f.read())["issue_metadata"]


def _register_jira_uri_with_file(
    mock: requests_mock.Mocker, endpoint: str, fixture_path: str
):
    _register_jira_uri(mock, endpoint, get_fixture_file_data(fixture_path=fixture_path))


def _register_jira_uri(mock: requests_mock.Mocker, endpoint: str, return_value: str):
    _MOCK_REST_BASE_URL = "https://test-co.atlassian.net/rest/api/2"

    mock.register_uri(
        "GET", f"{_MOCK_REST_BASE_URL}/{endpoint}", text=return_value,
    )
