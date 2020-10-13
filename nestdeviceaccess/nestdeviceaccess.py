import requests
from requests import auth

AUTH_URI = "https://www.googleapis.com/oauth2/v4/token"
DEFAULT_BASE_URI = "https://smartdevicemanagement.googleapis.com/v1"
DEFAULT_REDIRECT_URI = "https://www.google.com"


class ArgumentsMissingError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class NestDeviceAccessAuth(auth.AuthBase):
    def __init__(self, auth_callback, client_id, client_secret, code, session=None, redirect_uri=DEFAULT_REDIRECT_URI):
        if not client_id or client_secret or not code or client_id == "" or client_secret == "" or code == "":
            raise ArgumentsMissingError()
        self._res = {}
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri
        self._session = session
        self.auth_callback = auth_callback

    def login(self, headers=None):
        data = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': self.code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.redirect_uri}
        post = requests.post
        response = post(AUTH_URI, params=data, headers=headers)
        if response.status_code != 200:
            print(response.content)
            raise AuthorizationError(response)
        self._res = response.json()
        self.auth_callback(self._res)


class NestDeviceAccess(object):
    def __init__(self, client_id, client_secret, code, redirect_uri=DEFAULT_REDIRECT_URI):
        auth = NestDeviceAccessAuth(client_id, client_secret, code, self.login_callback, redirect_uri)
        self._session = requests.Session()
        self._session.auth = auth

    def login_callback(self, res):
        print(res)

    def login(self):
        self._session.auth.login()


#nda = NestDeviceAccess(client_id="484808906646-a9tche4b03q56u47fiojh04tbf7r56m8.apps.googleusercontent.com", client_secret="uS-rH6Fqcr_d_vsTHpZOZd6l", code="4/5AE-0v8n60-tkng0pcvVhgviF1i77yUfpseFxiURRzPi_vdlHDRCe2KL8nOnUa0AcDF4a2aKHarqChm6SQC4FoQ")
#nda.login()
