import pytest
import nestdeviceaccess


def callback():
    pass


def test_require_all_arguments():
    with pytest.raises(nestdeviceaccess.ArgumentsMissingError):
        _ = nestdeviceaccess.NestDeviceAccess(project_id="", client_secret="", client_id="", code="")


def test_url_printed_when_auth_code_not_present(capsys):
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
        nda.devices()


def test_failed_login_prints_error(capsys):
    nda = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="123")
    nda.login()
    captured = capsys.readouterr()
    assert captured.out == "Authorization Error\n"
