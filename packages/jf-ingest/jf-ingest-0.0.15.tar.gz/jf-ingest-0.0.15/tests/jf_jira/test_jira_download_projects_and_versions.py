from contextlib import contextmanager
import datetime
import json

import pytz
from jf_ingest.jf_jira.exceptions import NoAccessibleProjectsException
import pytest
import os
from unittest.mock import patch

import requests_mock

from jf_ingest.jf_jira.downloaders import download_projects_and_versions
from tests.jf_jira.utils import (
    _register_jira_uri,
    _register_jira_uri_with_file,
    get_jira_mock_connection,
    get_jellyfish_issue_metadata,
)


@contextmanager
def _mock_for_get_jira_projects_and_versions(project_accessible: bool = True):
    with patch(
        "jf_ingest.jf_jira.downloaders._project_is_accessible"
    ) as project_accessible_mock, requests_mock.Mocker() as _requests_mock:
        project_accessible_mock.return_value = project_accessible
        _register_jira_uri_with_file(
            _requests_mock, "project", "api_responses/project.json"
        )
        _register_jira_uri_with_file(
            _requests_mock,
            "project/OJ/versions",
            "api_responses/project_versions_OJ.json",
        )
        _register_jira_uri_with_file(
            _requests_mock,
            "project/JFR/versions",
            "api_responses/project_versions_JFR.json",
        )
        _register_jira_uri_with_file(
            _requests_mock,
            "project/OJ/components",
            "api_responses/project_components_OJ.json",
        )
        _register_jira_uri(_requests_mock, "project/JFR/components", "[]")
        yield


def test_get_jira_projects_and_versions_no_project_access():
    # test basic project exclusion/inclusion
    # Test when all projects are accessible
    with _mock_for_get_jira_projects_and_versions(project_accessible=False):
        # Make sure error raises when no projects available
        with pytest.raises(NoAccessibleProjectsException):
            connection = get_jira_mock_connection()
            print(connection)
            download_projects_and_versions(connection, {}, {}, [], [], [], [])


def test_get_jira_projects_and_versions_full_test():
    # test basic project exclusion/inclusion
    # Test when all projects are accessible
    with _mock_for_get_jira_projects_and_versions():
        projects = download_projects_and_versions(
            jira_connection=get_jira_mock_connection(),
            jellyfish_project_ids_to_keys={},
            jellyfish_issue_metadata=get_jellyfish_issue_metadata(),
            include_projects=[],
            exclude_projects=[],
            include_categories=[],
            exclude_categories=[],
        )

        with open(
            f"{os.path.dirname(__file__)}/fixtures/results/project_version_component.json",
            "r",
        ) as f:
            result_project_version_component_data = f.read()
            assert projects == json.loads(result_project_version_component_data)


def test_get_jira_projects_and_versions_filtering_test():
    # test basic project exclusion/inclusion
    # Test when all projects are accessible
    with _mock_for_get_jira_projects_and_versions():

        # Test Include Filter
        projects = download_projects_and_versions(
            jira_connection=get_jira_mock_connection(),
            jellyfish_project_ids_to_keys={},
            jellyfish_issue_metadata=get_jellyfish_issue_metadata(),
            include_projects=["OJ"],
            exclude_projects=[],
            include_categories=[],
            exclude_categories=[],
        )

        assert "JFR" not in [proj["key"] for proj in projects]
        assert "OJ" in [proj["key"] for proj in projects]

        # Test Exclude Filter
        projects = download_projects_and_versions(
            jira_connection=get_jira_mock_connection(),
            jellyfish_project_ids_to_keys={},
            jellyfish_issue_metadata=get_jellyfish_issue_metadata(),
            include_projects=[],
            exclude_projects=["OJ"],
            include_categories=[],
            exclude_categories=[],
        )

        assert "JFR" in [proj["key"] for proj in projects]
        assert "OJ" not in [proj["key"] for proj in projects]


def test_get_jira_projects_and_versions_rekey_test():
    with _mock_for_get_jira_projects_and_versions():
        earliest_date_str = pytz.utc.localize(datetime.datetime.min).isoformat()

        jellyfish_issue_metadata = get_jellyfish_issue_metadata()

        # BASELINE: TEST THAT WE DO NOT AFFECT ISSUE META UPDATED DATES AT ALL
        download_projects_and_versions(
            jira_connection=get_jira_mock_connection(),
            jellyfish_project_ids_to_keys={},
            jellyfish_issue_metadata=jellyfish_issue_metadata,
            include_projects=[],
            exclude_projects=[],
            include_categories=[],
            exclude_categories=[],
        )

        oj_issue_metadata = [
            metadata
            for metadata in jellyfish_issue_metadata.values()
            if metadata["project_id"] == "10000"
        ]

        assert not all(
            issue_metadata["updated"] == earliest_date_str
            for issue_metadata in oj_issue_metadata
        )

        # TEST THAT WE DO AFFECT ISSUE META UPDATED DATES !
        download_projects_and_versions(
            jira_connection=get_jira_mock_connection(),
            jellyfish_project_ids_to_keys={"10000": "OJ-NEW"},
            jellyfish_issue_metadata=jellyfish_issue_metadata,
            include_projects=[],
            exclude_projects=[],
            include_categories=[],
            exclude_categories=[],
        )

        oj_issue_metadata = [
            metadata
            for metadata in jellyfish_issue_metadata.values()
            if metadata["project_id"] == "10000"
        ]

        assert all(
            issue_metadata["updated"] == earliest_date_str
            for issue_metadata in oj_issue_metadata
        )
