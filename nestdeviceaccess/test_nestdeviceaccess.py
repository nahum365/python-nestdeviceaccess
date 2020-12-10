import pytest
import nestdeviceaccess


def callback():
    pass


def test_require_all_arguments():
    with pytest.raises(nestdeviceaccess.ArgumentsMissingError):
        _ = nestdeviceaccess.NestDeviceAccess(project_id="", client_secret="", client_id="", code="")


def test_url_printed_when_auth_code_not_present(capsys):
    with pytest.raises(nestdeviceaccess.ArgumentsMissingError):
        _ = nestdeviceaccess.NestDeviceAccess(project_id="123", client_secret="123", client_id="123", code="")
        captured = capsys.readouterr()
        assert captured.out == "Go to this link to get OAuth token: " \
                               "https://nestservices.google.com/partnerconnections/123/auth?redirect_uri=https://www" \
                               ".google.com&access_type=offline&prompt=consent&client_id=123&response_type=code&scope" \
                               "=https://www.googleapis.com/auth/sdm.service\n"
