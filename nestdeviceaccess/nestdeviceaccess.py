from datetime import datetime

import requests
import pickle
import os

AUTH_URI = "https://www.googleapis.com/oauth2/v4/token"
REFRESH_URI = "https://www.googleapis.com/oauth2/v4/token?client_id={client_id}" \
              "&client_secret={client_secret}&refresh_token={refresh_token}" \
              "&grant_type=refresh_token"
DEFAULT_BASE_URI = "https://smartdevicemanagement.googleapis.com/v1"
DEFAULT_REDIRECT_URI = "https://www.google.com"
DEVICES_URI = (
    "https://smartdevicemanagement.googleapis.com/v1/enterprises/{project_id}/devices"
)
EXECUTE_COMMAND_URI = "https://smartdevicemanagement.googleapis.com/v1/enterprises/" \
                      "{project_id}/devices/{device_id}:executeCommand"


class ArgumentsMissingError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class InvalidActionError(Exception):
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

        self.project_id = project_id
        self.client_id = client_id
        self.client_secret = client_secret
        self._res = {}
        self.access_token = None
        self.refresh_token = None

        if not code or code == "":
            self.invalid_token()
            raise ArgumentsMissingError()

        self.code = code

        self.redirect_uri = redirect_uri
        self._session = session

    def login(self):
        if os.path.exists("auth.bak"):
            with open("auth.bak", "rb") as token:
                creds = pickle.load(token)
                self.access_token = creds["access"]
                self.refresh_token = creds["refresh"]
                self.refresh()
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
        if self.refresh_token:
            self.refresh()
            return
        print(
            f"Go to this link to get OAuth token: https://nestservices.google.com/partnerconnections/{self.project_id}"
            f"/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id={self.client_id}"
            f"&response_type=code&scope=https://www.googleapis.com/auth/sdm.service"
        )

    def refresh(self):
        if not self.refresh_token:
            self.invalid_token()
            return
        response = requests.post(REFRESH_URI.format(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    refresh_token=self.refresh_token))
        if response.status_code != 200:
            if response.status_code == 400:
                self.invalid_token()
            raise AuthorizationError(response)
        self.access_token = response.json()["access_token"]


class Device(object):
    def __init__(self, dict):
        self.name = dict["name"]
        self.device_id = self.name.split('/')[3]
        self.type = dict["type"]
        self.traits = dict["traits"]


class CameraStream(object):
    def __init__(self, dict):
        self.rtsp_stream_url = dict["results"]["streamUrls"]["rtspUrl"]
        self.stream_token = dict["results"]["streamToken"]
        self.expires_at = datetime.strptime(dict["results"]["expiresAt"], "%Y-%m-%dT%H:%M:%S.%fZ")


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

    def get_devices(self):
        if not self.auth.access_token:
            raise AuthorizationError()

        response = requests.get(
            DEVICES_URI.format(project_id=self.project_id), auth=self.auth
        )
        if response.status_code != 200:
            if response.status_code == 400:
                raise AuthorizationError(response)
        devices_dict = response.json()

        devices = []
        for device_dict in devices_dict["devices"]:
            device = Device(device_dict)
            devices.append(device)
        return devices

    def get_camera_stream(self, device):
        if device.type not in ["sdm.devices.types.DOORBELL", "sdm.devices.types.CAMERA"]:
            raise InvalidActionError()
        if not self.auth.access_token:
            raise AuthorizationError()

        data = {
            "command": "sdm.devices.commands.CameraLiveStream.GenerateRtspStream",
            "params": {}
        }
        response = requests.post(EXECUTE_COMMAND_URI.format(project_id=self.project_id,
                                                            device_id=device.device_id),
                                 json=data,
                                 auth=self.auth)
        return CameraStream(response.json())
