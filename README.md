# python-nestdeviceaccess

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Build Status](https://travis-ci.com/nahum365/python-nestdeviceaccess.svg?branch=master)](https://travis-ci.com/nahum365/python-nestdeviceaccess) [![Documentation Status](https://readthedocs.org/projects/python-nestdeviceaccess/badge/?version=latest)](https://python-nestdeviceaccess.readthedocs.io/en/latest/?badge=latest)
 [![codecov](https://codecov.io/gh/nahum365/python-nestdeviceaccess/branch/master/graph/badge.svg?token=ZC5F0CLBNJ)](undefined)


A Python wrapper around the Nest Device Access API. For use in integrating Nest Devices into other smart home systems.

## Project Proposal

### Background

Google acquired Nest in 2014, and has since been integrating Nest products, including the Nest Thermostat, Nest Protect, and Nest Hello into the Google ecosystem. As they migrated to Google infrastructure, they chose to shut down the Works With Nest API while they developed a new API, called Nest Device Access. It was released in September 2020 (a couple days before I'm writing this) and as such, there is no Python wrapper (or any wrappers) to allow users to connect to their Nest Devices.

### Project

My project would be to create a Python wrapper around the Nest Device Access REST API, which could then be used by other applications to provide integrations with Nest smart home products.

### Tech Stack

Python, with appropriate third party libraries (probably requests for REST requests.)

### References:

https://developers.google.com/nest/device-access
