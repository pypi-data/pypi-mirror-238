from dataclasses import dataclass, field
import enum
import time
from jira import JIRA, JIRAError
from jira.resources import GreenHopperResource
import logging

from jf_ingest.jf_jira.exceptions import JiraRetryLimitExceeded
from jf_ingest.utils import get_wait_time

logger = logging.getLogger(__name__)


class JiraAuthMethod(enum.Enum):
    BasicAuth = 1
    AtlassianConnect = 2


@dataclass
class JiraAuthConfig:
    company_slug: str
    url: str
    # NOTE: Used in the User-Agent header. Not related
    # to the Jellyfish Agent
    user_agent: str = "jellyfish/1.0"
    # Used for Basic Auth
    user: str = None
    password: str = None
    personal_access_token: str = None
    # Used for Atlassian Direct Connect
    jwt_attributes: dict[str, str] = field(default_factory=dict)
    gdpr_active: bool = False
    bypass_ssl_verification: bool = False
    required_email_domains: bool = False
    is_email_required: bool = False
    auth_method: JiraAuthMethod = JiraAuthMethod.BasicAuth
    connect_app_active: bool = False


class JiraAuthenticationException(Exception):
    pass


def get_jira_connection(config: JiraAuthConfig, max_retries=3) -> JIRA:
    should_ssl_verify = not config.bypass_ssl_verification
    if config.auth_method == JiraAuthMethod.AtlassianConnect:
        if not config.connect_app_active:
            raise RuntimeError(
                f'Atlassian connect integration for {config.company_slug} is disabled. Check "connect_app_active" flag state.'
            )

        # The customer has installed our Atlassian Connect app; we authenticate to the Jira
        # API using the JWT attributes
        shared_secret = config.jwt_attributes.get("sharedSecret")
        client_key = config.jwt_attributes.get("clientKey")
        key = config.jwt_attributes.get("key")

        if not (shared_secret and client_key and key):
            raise RuntimeError(
                f"Atlassian connect integration for {config.company_slug} is misconfigured"
            )

        logger.info(f"Authenticating to Jira API at {config.url} using JWT attributes")

        jira_conn = JIRA(
            server=config.url,
            max_retries=max_retries,
            jwt={"secret": shared_secret, "payload": {"iss": key, "aud": client_key}},
            options={
                "agile_rest_path": GreenHopperResource.AGILE_BASE_REST_PATH,
                "verify": should_ssl_verify,
            },
        )

    elif config.auth_method == JiraAuthMethod.BasicAuth:

        jira_conn_kwargs = {}
        if config.user is not None:
            logger.info(
                f"Authenticating to Jira API at {config.url} "
                f"using the username and password secrets for {config.user} of company {config.company_slug}"
            )
            jira_conn_kwargs = {
                "server": config.url,
                "basic_auth": (config.user, config.password),
                "max_retries": max_retries,
                "options": {
                    "agile_rest_path": GreenHopperResource.AGILE_BASE_REST_PATH,
                    "verify": should_ssl_verify,
                },
            }
        elif config.personal_access_token:
            logger.info(
                f"Authenticating to Jira API at {config.url} "
                f"using the personal_access_token secret for {config.company_slug}"
            )
            jira_conn_kwargs = {
                "server": config.url,
                "max_retries": max_retries,
                "options": {
                    "agile_rest_path": GreenHopperResource.AGILE_BASE_REST_PATH,
                    "verify": should_ssl_verify,
                    "headers": {
                        "Authorization": f"Bearer {config.personal_access_token}",
                        "Cache-Control": "no-cache",
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "X-Atlassian-Token": "no-check",
                    },
                },
            }
        else:
            raise RuntimeError(
                f"No valid basic authentication mechanism for {config.url} - need a username/password combo or a personal access token"
            )

        retries = 0
        while True:
            try:
                jira_conn = JIRA(**jira_conn_kwargs)
                break
            except JIRAError as e:  # catch generic error raised from JIRA
                if hasattr(e, "status_code") and e.status_code in (401, 403):
                    raise JiraAuthenticationException(
                        f"Jira authentication (HTTP ERROR CODE {e.status_code}) failed for {config.url} using {config.user} and the jira_password secret for {config.company_slug}"
                    )
                elif hasattr(e, "status_code") and e.status_code == 429:
                    if retries < max_retries:
                        retries += 1
                        sleep_secs = get_wait_time(e, retries)
                        logger.info(
                            f"Caught JIRAError with a {e.status_code} return code during get_jira_connection. "
                            f"Hopefully transient; sleeping for {sleep_secs} secs then may retry ({retries} of {max_retries})."
                        )
                        time.sleep(sleep_secs)
                    else:
                        raise JiraRetryLimitExceeded(
                            f"Jira Authentication returned status code {e.status_code}. We attempted {retries} retries before raising this exception"
                        )
                else:
                    raise
    else:
        raise RuntimeError(f"No valid authentication mechanism for {config.url}")

    # set user-agent
    jira_conn._session.headers[
        "User-Agent"
    ] = f'{config.user_agent} ({jira_conn._session.headers["User-Agent"]})'

    return jira_conn
