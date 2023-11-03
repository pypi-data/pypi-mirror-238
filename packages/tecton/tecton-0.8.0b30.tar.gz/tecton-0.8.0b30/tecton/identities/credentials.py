import sys
import urllib
from typing import Optional
from typing import Union

import attrs
import requests

from tecton._internals.sdk_decorators import sdk_public_method
from tecton.cli import printer
from tecton.cli import workspace
from tecton.cli.workspace_utils import switch_to_workspace
from tecton.identities import api_keys
from tecton.identities import okta
from tecton_core import conf
from tecton_core import errors
from tecton_core.id_helper import IdHelper


@attrs.frozen
class ServiceAccountProfile:
    id: str
    name: str
    description: str
    created_by: str
    is_active: bool
    obscured_key: str


def set_credentials(tecton_api_key: Optional[str] = None, tecton_url: Optional[str] = None) -> None:
    """Explicitly override tecton credentials settings.

    Typically, Tecton credentials are set in environment variables, but you can
    use this function to set the Tecton API Key and URL during an interactive Python session.

    :param tecton_api_key: Tecton API Key
    :param tecton_url: Tecton API URL
    """
    if tecton_api_key:
        conf.set("TECTON_API_KEY", tecton_api_key)
    if tecton_url:
        conf.validate_api_service_url(tecton_url)
        conf.set("API_SERVICE", tecton_url)


def clear_credentials() -> None:
    """Clears credentials set by 'set_credentials' and 'login' (clearing any locally saved Tecton API key, user token and Tecton URL)"""
    for key in (
        "TECTON_API_KEY",
        "API_SERVICE",
        "OAUTH_ACCESS_TOKEN",
        "OAUTH_REFRESH_TOKEN",
        "OAUTH_ACCESS_TOKEN_EXPIRATION",
    ):
        try:
            conf.unset(key)
        except KeyError:
            pass


def test_credentials() -> None:
    """Test credentials and throw an exception if unauthenticated."""
    # First, check if a Tecton URL is configured.
    api_service = conf.get_or_none("API_SERVICE")
    if not api_service:
        msg = "Tecton URL not set. Please configure API_SERVICE or use tecton.set_credentials(tecton_url=<url>)."
        raise errors.TectonAPIInaccessibleError(msg)
    tecton_url = api_service[:-4] if api_service.endswith("/api") else api_service

    # Next, determine how the user is authenticated (Okta or Service Account).
    profile = who_am_i()
    auth_mode = None
    if isinstance(profile, ServiceAccountProfile):
        auth_mode = f"Service Account {profile.id} ({profile.name})"
    elif isinstance(profile, okta.UserProfile):
        auth_mode = f"User Profile {profile.email}"
    else:
        # profile can be None if TECTON_API_KEY is set, but invalid.
        if conf.get_or_none("TECTON_API_KEY"):
            msg = f"Invalid TECTON_API_KEY configured for {tecton_url}. Please update TECTON_API_KEY or use tecton.set_credentials(tecton_api_key=<key>)."
            raise errors.TectonAPIInaccessibleError(msg)
        msg = f"No user profile or service account configured for {tecton_url}. Please configure TECTON_API_KEY or use tecton.set_credentials(tecton_api_key=<key>)."
        raise errors.FailedPreconditionError(msg)

    print(f"Successfully authenticated with {tecton_url} using {auth_mode}.")


def who_am_i() -> Optional[Union[ServiceAccountProfile, okta.UserProfile]]:
    """Introspect the current User or API Key used to authenticate with Tecton.

    Returns:
      The UserProfile or ServiceAccountProfile of the current User or API Key (respectively) if the introspection is
      successful, else None.
    """
    user_profile = okta.get_user_profile()
    if user_profile:
        return user_profile
    else:
        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            try:
                introspect_result = api_keys.introspect(token)
            except PermissionError:
                print("Permissions error when introspecting the Tecton API key")
                return None
            if introspect_result is not None:
                return ServiceAccountProfile(
                    id=IdHelper.to_string(introspect_result.id),
                    name=introspect_result.name,
                    description=introspect_result.description,
                    created_by=introspect_result.created_by,
                    is_active=introspect_result.active,
                    obscured_key=f"****{token[-4:]}",
                )
    return None


@sdk_public_method
def login(url: str) -> None:
    # use BROWSER_MANUAL for now, can always make it nicer later
    _login_helper(url, okta.AuthFlowType.BROWSER_MANUAL)


def _login_helper(host: str, auth_flow_type: okta.AuthFlowType, okta_session_token: Optional[str] = None):
    """
    Common implementation for CLI `tecton login` and Notebook SDK `tecton.login()`.

    :param url: URL of Tecton deployment, e.g. https://staging.tecton.ai
    :param auth_flow_type: okta.AuthFlowType (browser, manual, or session token)
    :param okta_session_token: Optional string for auth_flow_type SESSION_TOKEN.
    :return:
    """
    try:
        urllib.parse.urlparse(host)
    except Exception:
        printer.safe_print("Tecton Cluster URL must be a valid URL")
        sys.exit(1)
    # add this check for now since it can be hard to debug if you don't specify https and API_SERVICE fails
    if host is None or not (host.startswith(("https://", "http://localhost:"))):
        if host is not None and "//" not in host:
            host = f"https://{host}"
        else:
            printer.safe_print("Tecton Cluster URL must start with https://")
            sys.exit(1)

    login_configs_url = urllib.parse.urljoin(host, "api/v1/metadata-service/get-login-configs")
    try:
        response = requests.post(login_configs_url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)
    configs = response.json()["key_values"]
    cli_client_id = configs["OKTA_CLI_CLIENT_ID"]

    flow = okta.OktaAuthorizationFlow(auth_flow_type=auth_flow_type, okta_session_token=okta_session_token)
    auth_code, code_verifier, redirect_uri = flow.get_authorization_code(cli_client_id)
    access_token, _, refresh_token, access_token_expiration = flow.get_tokens(
        auth_code, code_verifier, redirect_uri, cli_client_id
    )
    if not access_token:
        printer.safe_print("Unable to obtain Tecton credentials")
        sys.exit(1)

    if conf.get_or_none("API_SERVICE") != urllib.parse.urljoin(host, "api"):
        switch_to_workspace(workspace.PROD_WORKSPACE_NAME)

    conf.set("API_SERVICE", urllib.parse.urljoin(host, "api"))
    # FEATURE_SERVICE and API_SERVICE are expected to have the same base URI: <host>/api
    conf.set("FEATURE_SERVICE", conf.get_or_none("API_SERVICE"))
    conf.set("CLI_CLIENT_ID", cli_client_id)
    conf.set("OAUTH_ACCESS_TOKEN", access_token)
    if refresh_token is not None:
        conf.set("OAUTH_REFRESH_TOKEN", refresh_token)
    conf.set("OAUTH_ACCESS_TOKEN_EXPIRATION", access_token_expiration)

    if "ALPHA_SNOWFLAKE_COMPUTE_ENABLED" in configs:
        conf.set("ALPHA_SNOWFLAKE_COMPUTE_ENABLED", configs["ALPHA_SNOWFLAKE_COMPUTE_ENABLED"])
    else:
        conf.set("ALPHA_SNOWFLAKE_COMPUTE_ENABLED", False)

    conf.save_tecton_configs()
    conf.save_okta_tokens(access_token, access_token_expiration, refresh_token)
    printer.safe_print(f"✅ Updated configuration at {conf._LOCAL_TECTON_CONFIG_FILE}")
