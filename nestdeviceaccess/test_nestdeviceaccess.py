import pytest
import nestdeviceaccess


def callback():
    pass


def test_require_all_arguments():
    with pytest.raises(nestdeviceaccess.ArgumentsMissingError):
        _ = nestdeviceaccess.NestDeviceAccess(project_id="", client_secret="", client_id="", code="")

