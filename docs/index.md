# Welcome to python-nestdeviceaccess's documentation!

## Overview 
This Python library seeks to allow easy access to Google Nest devices using the Nest Device Access Smart Management API.
It allows interfacing with:

- Nest Hello doorbell

Coming soon:

- Nest thermostat

## Demo

### Access Devices
```
nda = NestDeviceAccess(
    project_id="PROJECT_ID",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    code="OAUTH_CODE",
)
nda.login()
for device in nda.devices():
    print(device.name)
```

### Access Camera Stream

```
nda = NestDeviceAccess(
    project_id="PROJECT_ID",
    client_id="CLIENT_ID",
    client_secret="CLIENT_SECRET",
    code="OAUTH_CODE",
)
nda.login()
for device in nda.get_devices():
    camera_stream = nda.get_camera_stream(device)
    print(camera_stream.rtsp_stream_url)
    print(camera_stream.stream_token)
    print(camera_stream.expires_at)
```