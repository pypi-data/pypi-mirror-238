from enum import Enum
import logging
from dataclasses import dataclass, field
from datetime import datetime
from itertools import chain
import traceback
from jf_ingest import diagnostics, logging_helper
from jf_ingest.jf_jira.auth import JiraAuthConfig, JiraAuthMethod, get_jira_connection
from jf_ingest.jf_jira.downloaders import (
    IssueMetadata,
    detect_issues_needing_re_download,
    detect_issues_needing_sync,
    download_all_issue_metadata,
    download_boards_and_sprints,
    download_customfieldoptions,
    download_fields,
    download_issuelinktypes,
    download_issuetypes,
    download_necessary_issues,
    download_priorities,
    download_projects_and_versions,
    download_resolutions,
    download_statuses,
    download_users,
    download_worklogs,
)

from jf_ingest.utils import IngestIOHelper

logger = logging.getLogger(__name__)


@dataclass
class JiraIngestionConfig:
    s3_bucket: str
    s3_path: str
    local_file_path: str
    company_slug: str

    # Jira Auth Info
    auth_config: JiraAuthConfig

    # Jira Server Information
    gdpr_active: bool

    # Fields information
    # NOTE: I assumed these are all strs
    include_fields: list[str]
    exclude_fields: list[str]

    # User information
    force_search_users_by_letter: bool
    search_users_by_letter_email_domain: str
    required_email_domains: list[str]
    is_email_required: bool

    # Projects information
    # NOTE: I assumed these are all strs
    include_projects: list[str]
    exclude_projects: list[str]
    include_project_categories: list[str]
    exclude_project_categories: list[str]

    # Boards/Sprints
    download_sprints: bool

    # Issues
    earliest_issue_dt: datetime
    issue_download_concurrent_threads: int
    issue_jql: str
    jellyfish_issue_metadata: dict
    jellyfish_project_ids_to_keys: dict

    # worklogs
    download_worklogs: bool
    # Potentially solidify this with the issues date, or pull from
    work_logs_pull_from: int

    # Jira Ingest Feature Flags
    feature_flags: dict = field(default_factory={})


class JiraObject(Enum):
    JiraFields = "jira_fields"
    JiraProjectsAndVersions = "jira_projects_and_versions"
    JiraUsers = "jira_users"
    JiraResolutions = "jira_resolutions"
    JiraIssueTypes = "jira_issuetypes"
    JiraLinkTypes = "jira_linktypes"
    JiraPriorities = "jira_priorities"
    JiraBoards = "jira_boards"
    JiraSprints = "jira_sprints"
    JiraBoardSprintLinks = "jira_board_sprint_links"
    JiraIssues = "jira_issues"
    JiraIssuesRedownloaded = "jira_issues_re_downloaded"
    JiraIssuesIdsDownloaded = "jira_issue_ids_downloaded"
    JiraIssuesIdsDeleted = "jira_issue_ids_deleted"
    JiraWorklogs = "jira_worklogs"
    JiraCustomFieldOptions = "jira_customfieldoptions"
    JiraStatuses = "jira_statuses"


@diagnostics.capture_timing()
@logging_helper.log_entry_exit()
def load_and_push_jira_to_s3(config: JiraIngestionConfig):
    try:
        # For JF Ingest logic, logger should always be set at debug!
        # This is for better log management when deal with agent,
        # where we sometimes want to hide stack traces from clients,
        # but also NOT upload their sensitive information
        original_log_level = logger.level
        logger.setLevel(level=logging.DEBUG)

        #######################################################################
        # SET UP JIRA CONNECTIONS (Basic and Potentially Atlassian Connect)
        #######################################################################
        jira_basic_connection = get_jira_connection(
            config=config.auth_config, auth_method=JiraAuthMethod.BasicAuth
        )
        jira_atlas_connect_connection = (
            get_jira_connection(
                config=config.auth_config, auth_method=JiraAuthMethod.AtlassianConnect
            )
            if JiraAuthMethod.AtlassianConnect
            in config.auth_config.available_auth_methods
            else None
        )
        # There is an ongoing effort to cut all things over to Atlassian Connect only,
        # but it is a piece wise migration for now.
        # OJ-29745
        jira_connect_or_fallback_connection = jira_basic_connection
        if config.feature_flags.get(
            "lusca-auth-always-use-connect-for-atlassian-apis-Q423"
        ):
            jira_connect_or_fallback_connection = jira_atlas_connect_connection

        #######################################################################
        # Init IO Helper
        #######################################################################
        ingest_io_helper = IngestIOHelper(
            s3_bucket=config.s3_bucket,
            s3_path=config.s3_path,
            local_file_path=f"{config.local_file_path}/jira",
        )

        #######################################################################
        # Jira Fields
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraFields.value,
            json_data=download_fields(
                jira_connect_or_fallback_connection,
                config.include_fields,
                config.exclude_fields,
            ),
        )

        #######################################################################
        # Jira Projects
        #######################################################################
        projects_and_versions = download_projects_and_versions(
            jira_connection=jira_basic_connection,  # Always use BasicAuth because we want to respect permission restrictions on projects
            jellyfish_project_ids_to_keys=config.jellyfish_project_ids_to_keys,
            jellyfish_issue_metadata=config.jellyfish_issue_metadata,
            include_projects=config.include_projects,
            exclude_projects=config.exclude_projects,
            include_categories=config.include_project_categories,
            exclude_categories=config.exclude_project_categories,
        )

        project_ids = {proj["id"] for proj in projects_and_versions}
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraProjectsAndVersions.value,
            json_data=projects_and_versions,
        )

        #######################################################################
        # Jira Users
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraUsers.value,
            json_data=download_users(
                jira_basic_connection=jira_basic_connection,  # Use BasicAuth because /users/search is not supported by Connect apps.
                jira_atlas_connect_connection=jira_atlas_connect_connection,  # Use AtlasConnect for 'augment with email' subtask
                gdpr_active=config.gdpr_active,
                force_search_users_by_letter=config.force_search_users_by_letter,
                search_users_by_letter_email_domain=config.search_users_by_letter_email_domain,
                required_email_domains=config.required_email_domains,
                is_email_required=config.is_email_required,
            ),
        )

        #######################################################################
        # Jira Resolutions
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraResolutions.value,
            json_data=download_resolutions(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Issue Types
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssueTypes.value,
            json_data=download_issuetypes(
                jira_connect_or_fallback_connection, project_ids
            ),
        )

        #######################################################################
        # Jira Link Types
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraLinkTypes.value,
            json_data=download_issuelinktypes(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Priorities
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraPriorities.value,
            json_data=download_priorities(jira_connect_or_fallback_connection),
        )

        #######################################################################
        # Jira Custom Field Options
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraCustomFieldOptions.value,
            json_data=download_customfieldoptions(jira_basic_connection, project_ids),
        )

        #######################################################################
        # Jira Statuses
        #######################################################################
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraStatuses.value,
            json_data=download_statuses(jira_basic_connection),
        )

        #######################################################################
        # Jira Boards, Sprints, and Links
        #######################################################################
        boards, sprints, links = download_boards_and_sprints(
            jira_basic_connection,  # Always use BasicAuth because we want to respect permission restrictions on projects
            project_ids,
            config.download_sprints,
        )
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraBoards.value, json_data=boards
        )
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraSprints.value, json_data=sprints
        )
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraBoardSprintLinks.value, json_data=links
        )

        #######################################################################
        # Jira Issues
        #######################################################################
        issue_metadata_from_jira = download_all_issue_metadata(
            jira_connect_or_fallback_connection,
            project_ids,
            config.earliest_issue_dt,
            config.issue_download_concurrent_threads,
            config.issue_jql,
        )

        issue_metadata_from_jellyfish = {
            int(issue_id): IssueMetadata(
                issue_info["key"],
                datetime.fromisoformat(
                    issue_info["updated"]
                ),  # already includes TZ info
            )
            for issue_id, issue_info in config.jellyfish_issue_metadata.items()
        }

        issue_metadata_addl_from_jellyfish = {
            int(issue_id): (
                issue_info.get("epic_link_field_issue_key"),
                issue_info.get("parent_field_issue_key"),
            )
            for issue_id, issue_info in config.jellyfish_issue_metadata.items()
        }

        (
            missing_issue_ids,
            _,
            out_of_date_issue_ids,
            deleted_issue_ids,
        ) = detect_issues_needing_sync(
            issue_metadata_from_jira, issue_metadata_from_jellyfish
        )

        issue_ids_to_download = list(missing_issue_ids.union(out_of_date_issue_ids))

        # TODO: Double check this approach makes sense....
        # This downloaded_issue_id_and_key_tuples could definitely be improved
        downloaded_issue_id_and_key_tuples = set()
        for batch_number, issue_batch in enumerate(
            download_necessary_issues(
                jira_basic_connection,
                issue_ids_to_download,
                config.include_fields,
                config.exclude_fields,
                config.issue_download_concurrent_threads,
            ),
            start=0,
        ):
            for issue in issue_batch:
                downloaded_issue_id_and_key_tuples.add(issue["id"], issue["key"])
            ingest_io_helper.write_json_data_to_local(
                object_name=JiraObject.JiraIssues.value,
                json_data=issue_batch,
                batch_number=batch_number,
            )

        issue_ids_needing_re_download = detect_issues_needing_re_download(
            downloaded_issue_id_and_key_tuples,
            issue_metadata_from_jellyfish,
            issue_metadata_addl_from_jellyfish,
        )

        # TODO: Double check this approach makes sense....
        # This downloaded_issue_id_and_key_tuples could definitely be improved
        redownloaded_issue_id_and_key_tuples = set()
        for batch_number, issue_batch in enumerate(
            download_necessary_issues(
                jira_basic_connection,
                list(issue_ids_needing_re_download),
                config.include_fields,
                config.exclude_fields,
                config.issue_download_concurrent_threads,
            ),
            start=0,
        ):
            for issue in issue_batch:
                redownloaded_issue_id_and_key_tuples.add(issue["id"], issue["key"])
            ingest_io_helper.write_json_data_to_local(
                object_name=JiraObject.JiraIssuesRedownloaded.value,
                json_data=issue_batch,
                batch_number=batch_number,
            )

        all_downloaded_issue_ids = [
            int(i[0])
            for i in chain(
                redownloaded_issue_id_and_key_tuples,
                redownloaded_issue_id_and_key_tuples,
            )
        ]

        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssuesIdsDownloaded.value,
            json_data=all_downloaded_issue_ids,
        )
        ingest_io_helper.write_json_data_to_local(
            object_name=JiraObject.JiraIssuesIdsDeleted.value,
            json_data=list(deleted_issue_ids),
        )

        #######################################################################
        # Jira Work Logs
        #######################################################################
        if config.download_worklogs:
            ingest_io_helper.write_json_data_to_local(
                object_name=JiraObject.JiraWorklogs.value,
                json_data=download_worklogs(
                    jira_basic_connection,
                    all_downloaded_issue_ids,
                    config.work_logs_pull_from,
                ),
            )

        #######################################################################
        # Upload files to S3
        #######################################################################
        ingest_io_helper.upload_files_to_s3()

        return True
    except Exception as e:
        logger.exception(f"Exception Encountered: {e}")
        logger.debug(traceback.format_exc())
        return False
    finally:
        # Reset log level
        logger.setLevel(level=original_log_level)
