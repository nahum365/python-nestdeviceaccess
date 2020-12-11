import pytest
import nestdeviceaccess
from datetime import datetime


def test_require_all_arguments():
    with pytest.raises(nestdeviceaccess.ArgumentsMissingError):
        _ = nestdeviceaccess.NestDeviceAccess(project_id="", client_secret="", client_id="", code="")


def test_auth_code_not_present_prints_url(capsys):
    try:
        _ = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="")
    except nestdeviceaccess.ArgumentsMissingError:
        pass
    captured = capsys.readouterr()
    assert captured.out == "Go to this link to get OAuth token: " \
                           "https://nestservices.google.com/partnerconnections/123/auth?redirect_uri=https://www" \
                           ".google.com&access_type=offline&prompt=consent&client_id=123&response_type=code&scope" \
                           "=https://www.googleapis.com/auth/sdm.service\n"


def test_devices_call_without_login_fails():
    with pytest.raises(nestdeviceaccess.AuthorizationError):
        nda = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="123")
        nda.get_devices()


def test_failed_login_prints_error(capsys):
    nda = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="123")
    nda.login()
    captured = capsys.readouterr()
    assert captured.out == "Authorization Error\n"


def test_failed_refresh_prints_url(capsys):
    nda = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="123")
    nda.auth.refresh()
    captured = capsys.readouterr()
    assert captured.out == "Go to this link to get OAuth token: " \
                           "https://nestservices.google.com/partnerconnections/123/auth?redirect_uri=https://www" \
                           ".google.com&access_type=offline&prompt=consent&client_id=123&response_type=code&scope" \
                           "=https://www.googleapis.com/auth/sdm.service\n"


def test_create_camera_stream():
    response = {
        "results": {
            "streamUrls": {
                "rtspUrl": "rtsp://123.com"
            },
            "streamToken": "token",
            "expiresAt": "2020-01-01T00:00:01.000Z",
        }
    }

    camera_stream = nestdeviceaccess.CameraStream(response)
    assert camera_stream.rtsp_stream_url == "rtsp://123.com"
    assert camera_stream.stream_token == "token"
    assert camera_stream.expires_at == datetime.strptime("2020-01-01T00:00:01.000Z", "%Y-%m-%dT%H:%M:%S.%fZ")


def test_create_device():
    response = {
        "name": "0/1/2/device_id",
        "type": "type",
        "traits": {"trait": "trait"}
    }

    device = nestdeviceaccess.Device(response)
    assert device.name == "0/1/2/device_id"
    assert device.device_id == "device_id"
    assert device.type == "type"
    assert device.traits == {"trait": "trait"}
