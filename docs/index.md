# Welcome to python-nestdeviceaccess's documentation!

## Overview 
This Python library seeks to allow easy access to Google Nest devices using the Nest Device Access Smart Management API.
It allows interfacing with:

- Nest Hello doorbell

Coming soon:

- Nest thermostat

## Demo

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
