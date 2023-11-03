from collections import namedtuple
import datetime
import logging
import string
from tqdm import tqdm
from typing import Any, Dict, Generator

import pytz
from jf_ingest import diagnostics, logging_helper
from jira import JIRA, JIRAError

from jf_ingest.utils import retry_for_429s
from jf_ingest.jf_jira.exceptions import (
    NoAccessibleProjectsException,
    NoJiraUsersFoundException,
)

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
    jira_basic_connection: JIRA,
    jira_atlas_connect_connection: JIRA,  # Set this to NONE for Agent
    gdpr_active: bool,
    search_users_by_letter_email_domain: str = None,  # Direct connect related Field
    required_email_domains: list[str] = [],  # Agent related field
    is_email_required=False,  # Agent related Field
) -> list[dict]:
    """ Download Jira Users to memory

    Args:
        jira_basic_connection (JIRA): A Jira connection authenticated with Basic Auth. Should NEVER be set to None!
        jira_atlas_connect_connection (JIRA): A Jira connection authenticated with Atlassian Direct Connect. Should be set to None
        when working with Agent or for specific instances in M.I.
        gdpr_active (bool): A boolean flag that represents if the client is Jira Server or Jira Cloud. If gdpr_active is False than
        the client is on Jira Server. For Jira Server clients we search for user data via _search_by_letter
        search_users_by_letter_email_domain (str, optional): Something set on Jira Instances (M.I.) that narrows down
        the search results when using _search_users_by_letter. ONLY APPLICABLE WITH JIRA SERVER INSTANCES. Defaults to None.
        required_email_domains (list[str], optional): Used by Agent, set up in the config.yml file. Used to filter for only
        specific users that we care about. Defaults to None.
        is_email_required (str, optional): When provided, if we are filtering by email domains (with required_email_domains)
        than this field WILL INCLUDE emails that have a null email field!!! Beware: counter intuitive!. Defaults to None.

    Returns:
        list[dict]: A list of raw jira users, augmented with emails
    """
    logger.info("downloading users... [!n]")
    jira_users = search_users(
        jira_connection=jira_basic_connection,
        gdpr_active=gdpr_active,
        search_users_by_letter_email_domain=search_users_by_letter_email_domain,
        required_email_domains=required_email_domains,
        is_email_required=is_email_required,
    )

    # Fetching user email requires Atlassian Connect connection
    if jira_atlas_connect_connection:
        jira_users = augment_jira_user_with_email(
            jira_atlas_connect_connection, jira_users
        )
    else:
        # If we don't have emails, we don't need to record the date at
        # which we pulled them.
        for u in jira_users:
            u["email_pulled"] = None

    logger.info("✓")
    return jira_users


def search_users(
    jira_connection: JIRA,
    gdpr_active: bool,
    search_users_by_letter_email_domain: str = None,
    required_email_domains: list = [],
    is_email_required: bool = False,
    page_size: int = 1000,
):
    """_summary_

    Args:
        jira_connection (JIRA): A Jira connection (Basic Auth)
        gdpr_active (bool): If True, we are on Jira Cloud (use the good API). If False, we use the painful _search_by_letter_approach
        search_users_by_letter_email_domain (str, optional): For Server only. Allows us to narrow down search results. Defaults to None.
        required_email_domains (list, optional): Agent only. Used to scrub out users we don't want. Agent feature. Defaults to [].
        is_email_required (bool, optional): _description_. Defaults to False.
        page_size (int, optional): _description_. Defaults to 1000.

    Raises:
        NoJiraUsersFoundException: _description_

    Returns:
        _type_: A list of raw jira users
    """
    if gdpr_active:
        jira_users = _get_all_users_for_gdpr_active_instance(
            jira_connection=jira_connection, page_size=page_size
        )
    else:
        jira_users = _search_users_by_letter(
            jira_connection, search_users_by_letter_email_domain, page_size=page_size
        )

    jira_users = _scrub_jira_users(
        jira_users, required_email_domains, is_email_required
    )
    logger.debug(f"found {len(jira_users)} users")

    if len(jira_users) == 0:
        raise NoJiraUsersFoundException(
            'We are unable to see any users. Please verify that this user has the "browse all users" permission.'
        )
    return jira_users


def _jira_user_key(user_dict: dict, gdpr_active: bool = False, **kwargs):
    """Helper function used for getting unique set of users

    Args:
        user_dict (dict): Raw User dict from JIRA API
        gdpr_active (bool, optional): Switches what key to grab, depending on if we are server or cloud. Defaults to False.

    Raises:
        KeyError: _description_

    Returns:
        _type_: Jira User Unique key (accountId or Key, depending on gdpr_active)
    """

    # Choose the key name based on the GDPR status
    if gdpr_active:
        key_name = "accountId"
    else:
        key_name = "key"

    # Return a default value if one is provided, otherwise raise a KeyError
    try:
        if "default" in kwargs:
            default_value = kwargs["default"]
            return user_dict.get(key_name, default_value)
        else:
            return user_dict[key_name]
    except KeyError as e:
        raise KeyError(
            f'Error extracting user data from Jira data. GDPR set to "{gdpr_active}" and expecting key name: "{key_name}" in user_dict. This is most likely an issue with how the GDPR flag is set on Jira instance. If this is a Jira Agent configuration, the agent config.yml settings may also be wrong.'
        ) from e


def get_searchable_jira_letters() -> list[str]:
    """Returns a list of lowercase ascii letters and all digits. DOES NOT INCLUDE PUNCTUATION!!!
    
    Note from Noah 6/28/22 - when using _search_users_by_letter with at least some
    jira server instances, some strange behavior occurs, explained with an example:
    take a case where search_users_by_letter_email_domain is set to '@business.com'
    meaning the query for the letter 'a' will be 'a@business.com'. Jira appears to
    take this query and split it on the punctuation and symbols, e.g [a, business, com].
    It then searches users username, name, and emailAddress for matches, performing the
    same punctuation and symbol split, and looking for matches starting at the beginning
    of each string, e.g. anna@business.com is split into [anna, business, com] and matches,
    but barry@business.com, split into [barry, business, com] will not match. Notably,
    these splits can match multiple substrings, which can lead to large lists of users.
    For example, when searching on the letter c, the full query would be 'c@business.com'
    split into [c, business, com]. This would obviously match cam@business.com, following
    the pattern from before, but unfortunately, the 'c' in the query will match any email
    ending in 'com', so effectively we will download every user. This will occur for
    letters matching every part of the variable search_users_by_letter_email_domain, split
    on punctuation and symbols.
    Notably, this will also happen when search_users_by_letter_email_domain is not set but
    there is still an overlap in the query and email address, e.g. query 'b' would hit all
    users in this hypothetical instance with an '@business.com' email address, since jira
    will split that address and search for strings starting with that query, matching b to business.
    In the future, this domain searching could provide a faster way than searching every
    letter to get all users for instances that have that variable set, but for the time
    being it requires pagination when searching by letter.


    Returns:
        list[str]: A list of lowercase ascii letters and all digits
    """
    return [*string.ascii_lowercase, *string.digits]


def _search_by_users_by_letter_helper(
    jira_connection: JIRA,
    base_query: str,
    search_users_by_letter_email_domain: str = None,
    max_results: int = 1000,
) -> list[dict]:
    """This is both a recursive and iterative function for searching for users on GDPR non compliant instances.
    It works by searching for each letter/number in the ascii set (get_searchable_jira_letters). If we find there
    are more than 1000 values for a letter, we will page for more results for that letter.
    
    IF we find that we can get exactly 1000 results for a letter and nothing more, that means we've likely hit
    this jira bug: https://jira.atlassian.com/browse/JRASERVER-65089. The work around for this scenario is to
    recursively iterate on THE NEXT letters that we want to search on. For example, if we are searching for the
    letter 'a', and we get exactly 1000 results than we would recurse on this function with the following queries:
    'aa', 'ab', 'ac', 'ad'... until we no longer run into this error

    Args:
        jira_connection (JIRA): _description_
        base_query (str): _description_
        search_users_by_letter_email_domain (str, optional): _description_. Defaults to None.
        max_results (int, optional): _description_. Defaults to 1000.

    Returns:
        list[dict]: A list of raw user objects
    """
    users = []
    for letter in get_searchable_jira_letters():
        start_at = 0
        query_iteration = f"{base_query}{letter}"
        query_to_search = (
            f"{query_iteration}@{search_users_by_letter_email_domain}"
            if search_users_by_letter_email_domain
            else f"{query_iteration}"
        )
        total_found_for_current_iter = 0
        while True:
            users_page: list[dict] = jira_connection._get_json(
                "user/search",
                {
                    "startAt": start_at,
                    "maxResults": max_results,
                    "includeActive": True,
                    "includeInactive": True,
                    "username": query_to_search,
                },
            )
            users.extend(users_page)
            total_found_for_current_iter += len(users_page)

            # IF we get back a full page for a letter, than we need to refire I query.
            # Example: if we get 1000 users for the letter 'b', than we need to search
            # for ba, bb, bc, bd, etc.
            # Following work around from here: https://jira.atlassian.com/browse/JRASERVER-65089
            if not users_page and start_at == max_results:
                logger.info(
                    f"Jira bug relating to only getting limited (10, 100, or 1000) results per page hit when querying for {query_to_search} encountered. "
                    f"Specifically it looks like we have found {total_found_for_current_iter} results for {query_to_search}"
                    "Recursing on this function to search for more user results"
                )
                users.extend(
                    _search_by_users_by_letter_helper(
                        jira_connection=jira_connection,
                        base_query=query_iteration,
                        search_users_by_letter_email_domain=search_users_by_letter_email_domain,
                        max_results=max_results,
                    )
                )
                break
            elif not users_page:
                break
            else:
                start_at += len(users_page)

    return users


def _search_users_by_letter(
    jira_connection: JIRA,
    search_users_by_letter_email_domain: str = None,
    page_size: int = 1000,
):
    """Search the 'old' API with each letter in the alphabet. Used ONLY by non GDPR instances

    Args:
        jira_connection (JIRA): Basic Jira Connection
        search_users_by_letter_email_domain (str, optional): If provided, email domain will be used to narrow down the list of returned users from the API. Defaults to None.
        page_size (int, optional): _description_. Defaults to 1000.

    Returns:
        _type_: _description_
    """

    non_deduped_jira_users = _search_by_users_by_letter_helper(
        jira_connection=jira_connection,
        base_query="",
        search_users_by_letter_email_domain=search_users_by_letter_email_domain,
        max_results=page_size,
    )
    jira_users_dict = {_jira_user_key(u, False): u for u in non_deduped_jira_users}

    return list(jira_users_dict.values())


def _get_all_users_for_gdpr_active_instance(
    jira_connection: JIRA, page_size=1000,
):
    """Gets ALL users from JIRA API. This includes active and inactive. Leverages
    the "Get All Users" API endpoint: 
    https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-users/#api-rest-api-2-users-search-get

    Args:
        jira_connection (JIRA): Jira Connection
        max_results (int, optional): Total number of users per page. Defaults to 1000.

    Returns:
        _type_: Returns unique list of all Jira Users in the Jira instance
    """
    jira_users = {}
    start_at = 0

    # Fetch users one page at a time
    while True:
        users = jira_connection._get_json(
            "users/search", {"startAt": start_at, "maxResults": page_size,}
        )

        jira_users.update({_jira_user_key(u, gdpr_active=True): u for u in users})

        if len(users) == 0:
            break  # no need to keep paging
        else:
            start_at += len(users)

    return list(jira_users.values())


def _scrub_jira_users(
    jira_users: list, required_email_domains: list[str], is_email_required: bool
):
    """Helper function for removing users we want to ignore. This is used predominantly by the agent as of 10/30/23

    Args:
        jira_users (list): _description_
        required_email_domains (list[str]): _description_
        is_email_required (bool): _description_
    """

    def _get_email_domain(email: str):
        try:
            return email.split("@")[1]
        except AttributeError:
            return ""
        except IndexError:
            return ""

    filtered_users = []
    for user in jira_users:
        """
        Scrubs external jira users in-place by overwriting 'displayName' and 'emailAddress' fields
        See OJ-5558 for more info.
        """
        if "accountType" in user and user["accountType"] == "customer":
            user["displayName"] = "EXTERNAL"
            user["emailAddress"] = ""

        # Filter out unwanted emails
        # (Agent use case)
        if required_email_domains:
            try:
                email = user["emailAddress"]
                email_domain = _get_email_domain(email)
                if email_domain in required_email_domains:
                    filtered_users.append(user)
            except KeyError:
                # NOTE: This was introduced in the Agent awhile ago
                # and honestly it seems like a bug from a UX perspective.
                # The comment around this functionality (see example.yml)
                # implies that this statement should really be 'if not is_email_required'
                # Switching this without doing any research could cause a flood
                # of bad user data to get ingested, though, so we'd need to do a careful
                # analysis of who has this flag set and work with them to straighten it out.
                # Pain.
                if is_email_required:
                    filtered_users.append(user)
        else:
            filtered_users.append(user)

    return filtered_users


def _should_augment_email(user: dict) -> bool:
    """Helper function for determing if a user should be augmented

    Args:
        user (dict): Raw user Object

    Returns:
        bool: Boolean (true if we SHOULD augment a user)
    """
    # if we don't have an accountId, or we got an email already,
    # then this instance isn't GPDR-ified; just use what we've got
    email = user.get("emailAddress")
    account_id = user.get("accountId")
    account_type = user.get("accountType")

    if email or not account_id:
        return False

    # OJ-6900: Skip Jira users that are of type "customer". These
    # are not particularly useful to Jellyfish (they are part of
    # Jira Service Desk) so skip fetching emails for them.
    elif account_type == "customer":
        return False

    return True


def augment_jira_user_with_email(
    jira_atlassian_connect_connection: JIRA, jira_users: list
) -> dict:
    """Attempts to augment a raw user object with an email, pulled from the
    atlassian direct connect JIRA connection. IF we do augment a user, we
    will add a new dictionary key to the raw user called 'email_pulled', which
    represents a UTC datetime of when we used the atlassian direct connect API.
    We need this timestamp to submit reports to Atlassian of when we used this
    API endpoint, see: https://developer.atlassian.com/cloud/jira/platform/user-privacy-developer-guide/#reporting-user-personal-data-for-your-apps

    Args:
        jira_atlassian_connect_connection (JIRA): A connection to Atlassian via their AtlassianConnect authentication
        jira_users (list): A list of raw users

    Yields:
        dict: A list of raw users with the 'email_pulled' key added, as well as their 'emailAddress' key potentially updated
    """

    for u in tqdm(jira_users, desc="augmenting users with emails..."):
        account_id = u.get("accountId")
        u["email_pulled"] = None
        if not _should_augment_email(u):
            yield u
        else:
            # hit the email API to retrieve an email for this user
            try:
                u["emailAddress"] = jira_atlassian_connect_connection._get_json(
                    "user/email", params={"accountId": account_id}
                )["email"]
                u["email_pulled"] = datetime.datetime.utcnow()
            except JIRAError as e:
                # 404s are normal; don't log them
                if getattr(e, "status_code", 0) != 404:
                    logger.exception(
                        f"Error retrieving email for {account_id}, skipping..."
                    )
            yield u


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_resolutions(jira_connection: JIRA) -> list[dict]:
    logger.info("downloading jira resolutions... [!n]")
    result = [r.raw for r in retry_for_429s(jira_connection.resolutions)]
    logger.info("✓")
    return result


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def download_issuetypes(jira_connection: JIRA, project_ids: list[str],) -> list[dict]:
    """
    For Jira next-gen projects, issue types can be scoped to projects.
    For issue types that are scoped to projects, only extract the ones
    in the extracted projects.

    Args:
        jira_connection (JIRA): Jira Connection
        project_ids (list[str]): List of Project IDs to include, if we
        are dealing with a 'next-gen' Jira Project

    Returns:
        list[dict]: List of Raw Issue Types pulled direct from Jira API
    """
    logger.info("downloading jira issue types...  [!n]",)
    result = []
    for it in retry_for_429s(jira_connection.issue_types):
        if "scope" in it.raw and it.raw["scope"]["type"] == "PROJECT":
            if it.raw["scope"]["project"]["id"] in project_ids:
                result.append(it.raw)
        else:
            result.append(it.raw)
    logger.info("✓")
    return result


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
def download_statuses(jira_connection: JIRA) -> list[dict]:
    """Fetches a list of Jira Statuses returned from the Jira status API endpoint

    Args:
        jira_connection (JIRA): A Jira connection, through their jira Python module

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains a 'status_id' key and a 'raw_json' field
    """
    logger.info("downloading jira statuses... [!n]")
    result = [
        {"status_id": status.id, "raw_json": status.raw}
        for status in retry_for_429s(jira_connection.statuses)
    ]
    logger.info("✓")
    return result


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
