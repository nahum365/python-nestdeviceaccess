import requests
import pickle
import os

AUTH_URI = "https://www.googleapis.com/oauth2/v4/token"
DEFAULT_BASE_URI = "https://smartdevicemanagement.googleapis.com/v1"
DEFAULT_REDIRECT_URI = "https://www.google.com"
DEVICES_URI = (
    "https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices"
)


class ArgumentsMissingError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class NestDeviceAccessAuth(requests.auth.AuthBase):
    def __init__(
        self,
        project_id,
        client_id,
        client_secret,
        code,
        session=None,
        redirect_uri=DEFAULT_REDIRECT_URI,
    ):
        if client_id == "" or client_secret == "" or project_id == "":
            raise ArgumentsMissingError()

        if not code or code == "":
            self.invalid_token()
            raise ArgumentsMissingError()

        self._res = {}
        self.access_token = None
        self.refresh_token = None

        self.project_id = project_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code
        self.redirect_uri = redirect_uri
        self._session = session

    def login(self):
        if os.path.exists("auth.bak"):
            with open("auth.bak", "rb") as token:
                creds = pickle.load(token)
                self.access_token = creds["access"]
                self.refresh_token = creds["refresh"]
                return

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(AUTH_URI, params=data)
        if response.status_code != 200:
            if response.status_code == 400:
                self.invalid_token()
            raise AuthorizationError(response)
        self._res = response.json()
        self.access_token = self._res["access_token"]
        self.refresh_token = self._res["refresh_token"]

        with open("auth.bak", "wb") as token:
            pickle.dump(
                {"access": self.access_token, "refresh": self.refresh_token}, token
            )

    def __call__(self, r):
        if self.access_token is not None:
            r.headers["authorization"] = "Bearer " + self.access_token
            return r
        else:
            self.login()
            r.headers["authorization"] = "Bearer " + self.access_token
            return r

    def invalid_token(self):
        print(
            f"Go to this link to get OAuth token: https://nestservices.google.com/partnerconnections/{self.project_id}"
            f"/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id={self.client_id}"
            f"&response_type=code&scope=https://www.googleapis.com/auth/sdm.service"
        )


class Device(object):
    def __init__(self, dict):
        self.name = dict["name"]
        self.type = dict["type"]
        self.traits = dict["traits"]


class NestDeviceAccess(object):
    def __init__(
        self,
        project_id,
        client_id,
        client_secret,
        code,
        redirect_uri=DEFAULT_REDIRECT_URI,
    ):
        self.auth = NestDeviceAccessAuth(
            project_id, client_id, client_secret, code, redirect_uri
        )
        self.access_token = None
        self.refresh_token = None

        self.project_id = project_id
        self.client_id = client_id
        self.client_secret = client_secret

    def login(self):
        try:
            self.auth.login()
        except AuthorizationError:
            print("Authorization Error")
            pass

    def devices(self):
        response = requests.get(
            DEVICES_URI.format(project_id=self.project_id), auth=self.auth
        )
        if response.status_code != 200:
            if response.status_code == 400:
                raise AuthorizationError(response)
        devices_dict = response.json()

        devices = []
        for device in devices_dict["devices"]:
            devices.append(Device(device))
        return devices


if __name__ == "__main__":
    nda = NestDeviceAccess(
        project_id="2a7ad63f-af0f-414a-b218-23dd6b39d0c5",
        client_id="484808906646-a9tche4b03q56u47fiojh04tbf7r56m8.apps.googleusercontent.com",
        client_secret="uS-rH6Fqcr_d_vsTHpZOZd6l",
        code="4/0AY0e-g6INJsCbfeHVxZV_Eg1jSEdWaxI22DgTfxUFTbPSBMXAEexjT_4VY9Rf1H5jht-hQ",
    )
    nda.login()
    for device in nda.devices():
        print(device.name)
