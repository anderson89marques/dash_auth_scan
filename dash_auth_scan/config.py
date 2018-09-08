"""Configure routes and google authentication"""

import dash
import dash_auth_scan
import dash_core_components as dcc
import dash_html_components as html
import requests
from dash.dependencies import Input, Output
from flask import redirect, session, url_for
from flask_dance.contrib.google import google, make_google_blueprint

from dash_auth_scan.scan import Scan


class GoogleAuthParams:
    def __init__(self, client_id, client_secret, domain='127.0.0.1:8050', allowed_domains=None, https=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.domain = domain
        self.https = https
        self.allowed_domains = allowed_domains


class GoogleAuthentication:
    def __init__(self, dash_app, googleAuthParams: GoogleAuthParams = None, allowed_domains=None):
        self.googleAuthParams = googleAuthParams
        self.href = self._href()
        self.dash_app = dash_app
        self.blueprint = self._make_google_blueprint()
        self.allowed_domains = googleAuthParams.allowed_domains or []

        self._register_blueprint()

    def _make_google_blueprint(self):
        """Create the blueprint"""
        return make_google_blueprint(
            client_id=self.googleAuthParams.client_id,
            client_secret=self.googleAuthParams.client_secret,
            scope=[
                "https://www.googleapis.com/auth/plus.me",
                "https://www.googleapis.com/auth/userinfo.email",
            ],
            offline=True
        )

    def _register_blueprint(self):
        """Register blueprint in dash app"""
        self.dash_app.server.register_blueprint(
            self.blueprint, url_prefix="/login")

    def _href(self):
        href_ = ''
        if self.googleAuthParams.https:
            href_ = f'https://{self.googleAuthParams.domain}'
        else:
            href_ = f'http://{self.googleAuthParams.domain}'

        return href_

    def logout(self):
        print('logout')
        requests.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": self.blueprint.token["access_token"]}
        )
        session.clear()


class ControlRoutes:
    def __init__(self):
        pass

    @staticmethod
    def init_route_control(app, scan, googleAuthentication):
        @app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
        )
        def display_page(pathname):
            print(f'Path: {pathname}')
            if not google.authorized:
                return html.Div([html.A("Login with google", href=googleAuthentication.href + url_for('google.login'))])
            else:
                resp_json = google.get("/oauth2/v2/userinfo").json()
                has_permission = [domain not in resp_json["email"]
                                  for domain in googleAuthentication.allowed_domains]
                if googleAuthentication.allowed_domains and all(has_permission):
                    googleAuthentication.logout()
                    return "You aren't unautherized!"
                if pathname == '/logout':
                    googleAuthentication.logout()
                    return html.Div([html.Link("Go to Login", href="/")])
                elif pathname in scan.routes:
                    return scan.routes[pathname]
                else:
                    return '404'


class Configuration:
    def __init__(self, dash_app, googleAuthParams: GoogleAuthParams = None):
        self.googleAuthentication = GoogleAuthentication(
            dash_app, googleAuthParams)
        self.controlRoutes = ControlRoutes()

    def scan(self, apps_path):
        scan = Scan(apps_path)
        scan.scan()
        self.controlRoutes.init_route_control(self.googleAuthentication.dash_app,
                                              scan,
                                              self.googleAuthentication)
