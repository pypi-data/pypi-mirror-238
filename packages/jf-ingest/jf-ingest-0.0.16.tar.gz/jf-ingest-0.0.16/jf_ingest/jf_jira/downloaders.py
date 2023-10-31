from collections import namedtuple
import datetime
import logging
from typing import Any, Dict, Generator

import pytz
from jf_ingest import diagnostics, logging_helper
from jira import JIRA, JIRAError

from jf_ingest.utils import retry_for_429s
from jf_ingest.jf_jira.exceptions import NoAccessibleProjectsException

# jira renamed this between api versions for some reason
try:
    from jira.resources import AgileResource as AGILE_BASE_REST_PATH
except ImportError:
    from jira.resources import GreenHopperResource as AGILE_BASE_REST_PATH

logger = logging.getLogger(__name__)


def get_jira_connection(config, creds, max_retries=3) -> JIRA:
    kwargs = {
        "server": config.jira_url,
        "max_retries": max_retries,
        "options": {
            "agile_rest_path": AGILE_BASE_REST_PATH,
            "verify": not config.skip_ssl_verification,
        },
    }

    if creds.jira_username and creds.jira_password:
        kwargs["basic_auth"] = (creds.jira_username, creds.jira_password)
    elif creds.jira_bearer_token:
        kwargs["options"]["headers"] = {
            "Authorization": f"Bearer {creds.jira_bearer_token}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Atlassian-Token": "no-check",
        }
    else:
        raise RuntimeError(
            "No valid Jira credentials found! Check your JIRA_USERNAME, JIRA_PASSWORD, or JIRA_BEARER_TOKEN environment variables."
        )

    jira_connection = JIRA(**kwargs)

    jira_connection._session.headers[
        "User-Agent"
    ] = f'jellyfish/1.0 ({jira_connection._session.headers["User-Agent"]})'

    return jira_connection


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_fields(
    jira_connection: JIRA,
    include_fields: list[str] = [],
    exclude_fields: list[str] = [],
) -> list[dict]:
    logger.info("downloading jira fields... ")

    filters = []
    if include_fields:
        filters.append(lambda field: field["id"] in include_fields)
    if exclude_fields:
        filters.append(lambda field: field["id"] not in exclude_fields)

    fields = [
        field
        for field in jira_connection.fields()
        if all(filter(field) for filter in filters)
    ]

    logger.info("✓")
    return fields


def _project_is_accessible(jira_connection: JIRA, project_id: str):
    try:
        retry_for_429s(
            jira_connection.search_issues, f"project = {project_id}", fields=["id"]
        )
        return True
    except JIRAError as e:
        # Handle zombie projects that appear in the project list
        # but are not actually accessible.
        if (
            e.status_code == 400
            and e.text
            == f"A value with ID '{project_id}' does not exist for the field 'project'."
        ):
            logging_helper.log_standard_error(
                logging.ERROR, msg_args=[project_id], error_code=2112,
            )
            return False
        else:
            raise


def _detect_project_rekeys_and_update_metadata(
    projects: list,
    jellyfish_project_ids_to_keys: dict[str, str],
    jellyfish_issue_metadata: dict[str, dict],
):
    rekeyed_projects = []
    for project in projects:
        # Detect if this project has potentially been rekeyed !
        if (
            project.id in jellyfish_project_ids_to_keys
            and project.raw["key"] != jellyfish_project_ids_to_keys[project.id]
        ):
            logger.debug(
                f'Project (project_id={project.id}) {project.raw["key"]} was detected as being rekeyed (it was previously {jellyfish_project_ids_to_keys[project.id]}. Attempting to re-download all related jira issue data'
            )
            rekeyed_projects.append(project.id)

    # Mark issues for redownload if they are associated with rekeyed projects
    for metadata in jellyfish_issue_metadata.values():
        if metadata["project_id"] in rekeyed_projects:
            # Updating the updated time for each issue will force a redownload
            metadata["updated"] = pytz.utc.localize(datetime.datetime.min).isoformat()


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_projects_and_versions(
    jira_connection: JIRA,
    jellyfish_project_ids_to_keys: dict[str, str],
    jellyfish_issue_metadata: str,
    include_projects: list[str],
    exclude_projects: list[str],
    include_categories: list[str],
    exclude_categories: list[str],
) -> list[dict]:
    logger.info("downloading jira projects... [!n]")

    filters = []
    if include_projects:
        filters.append(lambda proj: proj.key in include_projects)
    if exclude_projects:
        filters.append(lambda proj: proj.key not in exclude_projects)
    if include_categories:

        def _include_filter(proj):
            # If we have a category-based allowlist and the project
            # does not have a category, do not include it.
            if not hasattr(proj, "projectCategory"):
                return False

            return proj.projectCategory.name in include_categories

        filters.append(_include_filter)

    if exclude_categories:

        def _exclude_filter(proj):
            # If we have a category-based excludelist and the project
            # does not have a category, include it.
            if not hasattr(proj, "projectCategory"):
                return True

            return proj.projectCategory.name not in exclude_categories

        filters.append(_exclude_filter)

    all_projects = retry_for_429s(jira_connection.projects)

    projects = [
        proj
        for proj in all_projects
        if all(filt(proj) for filt in filters)
        and _project_is_accessible(jira_connection, proj.id)
    ]

    if not projects:
        raise NoAccessibleProjectsException(
            "No Jira projects found that meet all the provided filters for project and project category. Aborting... "
        )

    _detect_project_rekeys_and_update_metadata(
        projects=projects,
        jellyfish_project_ids_to_keys=jellyfish_project_ids_to_keys,
        jellyfish_issue_metadata=jellyfish_issue_metadata,
    )

    logger.info("✓")

    logger.info("downloading jira project components... [!n]")
    for p in projects:
        p.raw.update(
            {
                "components": [
                    c.raw for c in retry_for_429s(jira_connection.project_components, p)
                ]
            }
        )
    logger.info("✓")

    logger.info("downloading jira versions... [!n]")
    result = []
    for p in projects:
        versions = retry_for_429s(jira_connection.project_versions, p)
        p.raw.update({"versions": [v.raw for v in versions]})
        result.append(p.raw)
    logger.info("✓")
    return result


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_users(
    jira_connection,
    gdpr_active,
    quiet=False,
    required_email_domains=None,
    is_email_required=False,
) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_resolutions(jira_connection: JIRA) -> list[dict]:
    logger.info("downloading jira resolutions... [!n]")
    result = [r.raw for r in retry_for_429s(jira_connection.resolutions)]
    logger.info("✓")
    return result


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issuetypes(jira_connection, project_ids) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issuelinktypes(jira_connection: JIRA) -> list[dict]:
    """Download Jira Issue Link Types from the issueLinkType endpoint.

    Args:
        jira_connection (JIRA): A Jira connection, from the jira Python library

    Returns:
        list[dict]: A list of 'raw' JSON objects pulled directly from the issueLinkType endpoint
    """
    logger.info("downloading jira issue link types... [!n]")
    result = [lt.raw for lt in retry_for_429s(jira_connection.issue_link_types)]
    logger.info("✓")
    return result


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_priorities(jira_connection: JIRA) -> list[dict]:
    """Loads Jira Priorities from their API. Has 429 handling logic

    Args:
        jira_connection (JIRA): A Jira connection (with the provided Jira Library)

    Returns:
        list[dict]: A list of 'raw' JSON objects pulled from the 'priority' endpoint
    """
    logger.info("downloading jira priorities... [!n]")
    result = [p.raw for p in retry_for_429s(jira_connection.priorities)]
    logger.info("✓")
    return result


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_boards_and_sprints(
    jira_connection: JIRA, project_ids, download_sprints
) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def get_issues(jira_connection, issue_jql, start_at, batch_size) -> list[dict]:
    return []


# TODO: Make this a dataclass. Not a fan of namedtuple
IssueMetadata = namedtuple("IssueMetadata", ("key", "updated"))


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_all_issue_metadata(
    jira_connection,
    all_project_ids,
    earliest_issue_dt,
    num_parallel_threads,
    issue_filter,
) -> Dict[int, IssueMetadata]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def detect_issues_needing_sync(
    issue_metadata_from_jira: Dict[int, IssueMetadata],
    issue_metadata_from_jellyfish: Dict[int, IssueMetadata],
) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_worklogs(jira_connection, issue_ids, work_logs_pull_from) -> list[dict]:
    return []


# Returns an array of CustomFieldOption items
@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_customfieldoptions(jira_connection, project_ids) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_statuses(jira_connection) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def detect_issues_needing_re_download(
    downloaded_issue_id_and_key_tuples: set[tuple[str, str]],
    issue_metadata_from_jellyfish,
    issue_metadata_addl_from_jellyfish,
) -> list[dict]:
    return []


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_necessary_issues(
    jira_connection,
    issue_ids_to_download,
    include_fields,
    exclude_fields,
    num_parallel_threads,
    suggested_batch_size: int = 2000,
) -> Generator[Any, None, None]:
    return []
