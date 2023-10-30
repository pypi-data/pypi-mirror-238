# pylint: disable=locally-disabled,suppressed-message,useless-suppression
# flake8: noqa: E371 -- lambda
"""
Vault Client class.
"""

import webbrowser
import os
from typing import Callable, Tuple, Optional
import urllib.parse
import logging
import tempfile
import json
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import hvac
import kubernetes
import jwt


# pylint: disable=too-few-public-methods
class EnvVarNames:
    """Reduce hardcoding by collecting env var names in this class."""

    VAULT_ADDR = 'VAULT_ADDR'
    GITHUB_TOKEN = 'GITHUB_TOKEN'
    ROLE_ID = 'ROLE_ID'
    KUBERNETES_SERVICE_HOST = 'KUBERNETES_SERVICE_HOST'
    VAULT_TOKEN = 'VAULT_TOKEN'


class VaultClient():
    """Connect to the vault and get secrets using different authentication methods."""
    def __init__(self,
                 vault_addr: str = None,
                 github_token: str = None,
                 k8s_serviceaccount_token: str = None,
                 vault_base_mount_point: str = None) -> None:

        if self.is_in_cluster():
            self._client, self._authenticate_func = self._use_kubernetes_auth(
                vault_addr, vault_base_mount_point, k8s_serviceaccount_token)
        elif EnvVarNames.ROLE_ID in os.environ:
            vault_addr = self._get_vault_addr(vault_addr)
            self._client, self._authenticate_func = self._use_approle_auth(vault_addr)
        elif EnvVarNames.VAULT_TOKEN in os.environ:
            vault_addr = self._get_vault_addr(vault_addr)
            self._client, self._authenticate_func = self._use_vaulttoken_auth(vault_addr)
        elif EnvVarNames.GITHUB_TOKEN in os.environ:
            vault_addr = self._get_vault_addr(vault_addr)
            self._client, self._authenticate_func = self._use_github_auth(
                vault_addr, github_token)
        else:
            vault_addr = self._get_vault_addr(vault_addr)
            self._client, self._authenticate_func = self._use_azuread_auth(vault_addr)
        self._authenticate_func(self._client)

    def get_value(self, secret_path: str) -> str:
        """Retrieve a secret value for a given secret path.

        Parameters
        ----------
        secret_path : str

        Returns
        -------
        str
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)

        secret = secret_path.split("/")[-1]
        mount_point = "/".join(secret_path.split("/")[:2])

        secret_path_array_length = len(secret_path.split("/"))
        path = "/".join(secret_path.split("/")[2:secret_path_array_length - 1])

        return self._client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point, path=path, raise_on_deleted_version=True
            )['data']['data'][secret]

    def encrypt_secret(self, transit_path: str, key_name: str, plaintext: str) -> str:
        """Encrypts a secret and returns the ciphertext

        Parameters
        ----------
        transit_path: str, {system}/transit (usually)
        key_name: str, name of the backend key
        plaintext: str, base64

        Returns
        -------
        str, format: vault:v1:{ciphertext}, the string that should be sent to vault for decryption
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)

        response = self._client.secrets.transit.encrypt_data(key_name, plaintext,
                                                             mount_point=transit_path)
        return response['data']['ciphertext']

    def decrypt_secret(self, transit_path: str, key_name: str, ciphertext: str) -> str:
        """Encrypts a secret and returns the ciphertext

        Parameters
        ----------
        transit_path: str, {system}/transit (usually)
        key_name: str, name of the backend key
        ciphertext: str, format: vault:v1:{ciphertext}

        Returns
        -------
        str, base64
        """
        if not self._client.is_authenticated():
            self._authenticate_func(self._client)

        response = self._client.secrets.transit.decrypt_data(key_name, ciphertext,
                                                             mount_point=transit_path)
        return response['data']['plaintext']

    @staticmethod
    def is_in_cluster() -> bool:
        """Tell whether the code is running in the cluster or not."""
        if EnvVarNames.KUBERNETES_SERVICE_HOST in os.environ:
            return True
        return False

    def _use_kubernetes_auth(
            self, vault_addr: str = None, vault_base_mount_point: str = None,
            jwt_token: str = None) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:

        if vault_base_mount_point is None:
            vault_addr, vault_base_mount_point = self._read_vault_addr()

        if jwt_token is None:
            jwt_token = self._read_serviceaccount_token()

        decoded_token = jwt.decode(jwt_token,
                                   options={"verify_signature": False})

        if "kubernetes.io/serviceaccount/namespace" in decoded_token:
            namespace = decoded_token["kubernetes.io/serviceaccount/namespace"]
            serviceaccount_name = decoded_token[
                "kubernetes.io/serviceaccount/service-account.name"]
        else:
            namespace = decoded_token['kubernetes.io']['namespace']
            serviceaccount_name = decoded_token["kubernetes.io"]["serviceaccount"]["name"]

        vault_client = hvac.Client(url=vault_addr)
        mount_point = f"{vault_base_mount_point}{namespace}/{serviceaccount_name}"

        # pylint: disable=unnecessary-lambda-assignment
        authenticate_func = lambda client, serviceaccount_name=serviceaccount_name, \
            jwt_token=jwt_token, mount_point=mount_point: \
            hvac.api.auth_methods.Kubernetes(client.adapter).login(
                role=serviceaccount_name, jwt=jwt_token, mount_point=mount_point)

        return vault_client, authenticate_func

    @staticmethod
    def _use_approle_auth(vault_addr: str) \
            -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        role_id = os.environ[EnvVarNames.ROLE_ID]

        vault_client = hvac.Client(url=vault_addr)

        # pylint: disable=unnecessary-lambda-assignment
        authenticate_func = lambda client, role_id=role_id: client.auth.approle.login(
            role_id)

        return vault_client, authenticate_func

    @staticmethod
    def _use_vaulttoken_auth(vault_addr: str) \
            -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        vault_token = os.environ[EnvVarNames.VAULT_TOKEN]

        vault_client = hvac.Client(url=vault_addr, token=vault_token)

        # pylint: disable=unnecessary-lambda-assignment
        authenticate_func = lambda client: client.is_authenticated()

        return vault_client, authenticate_func

    @staticmethod
    def _read_vault_addr() -> Tuple[str, str]:
        kubernetes.config.load_incluster_config()
        api_instance = kubernetes.client.CoreV1Api()

        response = api_instance.read_namespaced_config_map("vault", "vault")

        return response.data["vault_hostname"], response.data[
            "vault_base_mountpoint"]

    @staticmethod
    def _read_k8s_secret(path: str, err_msg: str) -> str:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as file_open:
                secret = file_open.read()
            if len(secret) > 0:
                return secret

        # OSError because involves I/O failure when reading a file
        raise OSError(err_msg)

    def _read_serviceaccount_token(self):
        return self._read_k8s_secret(
            "/var/run/secrets/kubernetes.io/serviceaccount/token",
            "If running on kubernetes, the pod must be running as a separate service \
             account with its token loaded at /var/run/secrets/kubernetes.io/serviceaccount/token"
        )

    @staticmethod
    def _get_vault_addr(vault_addr: str = None) -> str:
        if vault_addr is None:
            if EnvVarNames.VAULT_ADDR not in os.environ:
                raise AttributeError(f"The environment variable \
                    {EnvVarNames.VAULT_ADDR} must be set or vault_addr given")
            vault_addr = os.environ[EnvVarNames.VAULT_ADDR]
        return vault_addr

    @staticmethod
    def _use_github_auth(
        vault_addr: str = None,
        github_token: str = None
    ) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:
        if github_token is None:
            if EnvVarNames.GITHUB_TOKEN not in os.environ:
                raise AttributeError(f"The environment variable \
                    {EnvVarNames.GITHUB_TOKEN} must be set or github_token given")
            github_token = os.environ[EnvVarNames.GITHUB_TOKEN]

        vault_client = hvac.Client(vault_addr)

        # pylint: disable=unnecessary-lambda-assignment
        authenticate_func = lambda client, github_token=github_token: client.auth.github.login(
            github_token)

        return vault_client, authenticate_func



    OIDC_CALLBACK_PORT = 8250
    OIDC_REDIRECT_URI = f'http://localhost:{OIDC_CALLBACK_PORT}/oidc/callback'
    ROLE = None # Use None (not empty string) for the default Role
    SELF_CLOSING_PAGE = '''
    <!doctype html>
    <html>
    <head>
    <meta charset=utf-8>
    <title>Elvia Vault Authentication</title>
    <link id='favicon' rel='icon'
        href='https://cdn.elvia.io/npm/elvis-assets-trademark-1.0.2/dist/favicon/default/favicon.ico'
        type='image/x-icon'>
    <link rel='stylesheet' href='https://cdn.elvia.io/npm/elvis-7.6.0/css/elvis.min.css'
        integrity='sha512-9JMlf0XmTWrMPVzyeJsDdRRk+u2GOzwqlFvkTZnOR7rWzOlZTgeRmmsbX68DDZdIFf83ZcJrXI8gbWNqcW59CA=='
        crossorigin='anonymous'>
    <script>
    // Closes IE, Edge, Chrome, Brave
    window.onload = function load() {
    window.open('', '_self', '');
    window.close();
    };
    </script>
    </head>
    <body>
    <p>Authentication successful, you can close the browser now.</p>
    <script>
        // Needed for Firefox security
        setTimeout(function() {
            window.close()
        }, 5000);
    </script>
    </body>
    </html>
    '''
    @staticmethod
    def _use_azuread_auth(
        vault_addr: str = None
    ) -> Tuple[hvac.Client, Callable[[hvac.Client], None]]:

        vault_client = hvac.Client(vault_addr)

        authenticate_func = VaultClient._azuread_auth_login

        return vault_client, authenticate_func

    @staticmethod
    def _azuread_auth_login(client: hvac.Client):
        logging.info('Did not detect any environment variables to login to Vault; \
                     VAULT_TOKEN, GITHUB_TOKEN, etc.')
        logging.info('Using the default method of Azure AD login. A browser is required.')

        cached_auth_token = VaultClient._read_from_cache(client)
        if cached_auth_token is None:
            auth_url_response = client.auth.oidc.oidc_authorization_url_request(
                role=VaultClient.ROLE,
                redirect_uri=VaultClient.OIDC_REDIRECT_URI,
            )
            auth_url = auth_url_response['data']['auth_url']

            params = urllib.parse.parse_qs(auth_url.split('?')[1])
            auth_url_nonce = params['nonce'][0]
            auth_url_state = params['state'][0]

            webbrowser.open(auth_url)
            token = VaultClient._login_oidc_get_token()

            auth_result = client.auth.oidc.oidc_callback(
                code=token,
                path='oidc',
                nonce=auth_url_nonce,
                state=auth_url_state,
            )
            VaultClient._write_to_cache(auth_result)
        else:
            auth_result = cached_auth_token

        client.token = auth_result['auth']['client_token']

    @staticmethod
    def _login_oidc_get_token():
        class _HttpServ(HTTPServer):
            def __init__(self, *args, **kwargs):
                HTTPServer.__init__(self, *args, **kwargs)
                self.token = None

        class _AuthHandler(BaseHTTPRequestHandler):
            token = ''

            # pylint: disable=missing-function-docstring, invalid-name
            def do_GET(self):
                params = urllib.parse.parse_qs(self.path.split('?')[1])
                self.server.token = params['code'][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str.encode(VaultClient.SELF_CLOSING_PAGE))

        server_address = ('', VaultClient.OIDC_CALLBACK_PORT)
        httpd = _HttpServ(server_address, _AuthHandler)
        httpd.handle_request()
        return httpd.token

    @staticmethod
    def _write_to_cache(auth_result: dict):
        cache_file = os.path.join(tempfile.gettempdir(), 'elvia_vault_token_local_cache.json')
        with open(cache_file, 'w', encoding="utf-8") as file_handler:
            logging.debug('Writing Vault Token to local cache.')
            file_handler.write(json.dumps(auth_result))

    @staticmethod
    def _read_from_cache(client) -> Optional[dict]:
        logging.debug('Check cache for existing Vault Token.')
        try:
            temp_file = os.path.join(tempfile.gettempdir(), 'elvia_vault_token_local_cache.json')
            if not os.path.isfile(temp_file):
                logging.debug('Vault Token not found.')
                return None
            with open(temp_file, 'r', encoding="utf-8") as file_handler:
                auth_result = json.load(file_handler)
                if auth_result is not None:
                    token_accessor = auth_result['auth']['accessor']
                    lookup_response = client.auth.token.lookup_accessor(token_accessor)
                    expire_time_str = lookup_response['data']['expire_time']
                    expire_time = datetime.strptime(expire_time_str[0:19]+"Z", "%Y-%m-%dT%H:%M:%SZ")
                    if expire_time < datetime.now() + timedelta(minutes = 10):
                        logging.debug('Vault Token expired.')
                        return None
                    logging.debug('Vault Token valid and not expired.')
                return auth_result
        # pylint: disable=bare-except
        except:
            logging.debug('Unable to parse Vault Token from cache.')
            return None
