# Python SDK

Python SDK for the AirborneRF Aviation API.

## Using the Python SDK in your code

The SDK is published to PyPI, so you can install it with `pip`:

```shell
pip install airbornerf-aviation-sdk
```

The project page is https://pypi.org/project/airbornerf-aviation-sdk/.

## Demo application

The repository comes with a demo application that uses the AirborneRF Aviation API and
demonstrates its general usage. You can run it directly from the command line.

To use the demo, you need to have available:
* The Aviation API endpoint URL
* The Aviation API auth token

To run the demo:

```shell
# replace "endpoint-url" and "auth-token" with the values you were provided
pipenv install --dev
pipenv run python3 main.py [endpoint-url] [auth-token]
```



