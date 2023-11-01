from dataclasses import dataclass
from typing import AnyStr

from nicegui import ui
from nicegui.awaitable_response import AwaitableResponse


@dataclass
class KeycloakConfig:
    url: AnyStr
    realm: AnyStr
    client_id: AnyStr


class Keycloak(ui.element, component='keycloak.js'):
    config: KeycloakConfig = None
    require_login: bool = None

    def __init__(self,
                 config: KeycloakConfig,
                 js_source: AnyStr = '/static/keycloak.js',
                 require_login: bool = True):
        super().__init__()

        ui.add_head_html('<script src="'
                         f'{js_source}'
                         '"></script>')
        ui.add_head_html(
            f"""<script>const keycloakConfig = {{
                url: '{config.url}',
                realm: '{config.realm}',
                clientId: '{config.client_id}'
            }}</script>""")
        ui.add_head_html(
            "<script>const globalKeycloakInstance = new Keycloak(keycloakConfig);</script>")

        self.require_login = require_login

    def initialize(self) -> AwaitableResponse:
        init_config = {}
        if self.require_login:
            init_config['onLoad'] = 'login-required'
        return self.run_method('initialize', init_config)

    def get_token(self) -> AwaitableResponse:
        return self.run_method('getToken')

    def is_authenticated(self) -> AwaitableResponse:
        return self.run_method('isAuthenticated')
