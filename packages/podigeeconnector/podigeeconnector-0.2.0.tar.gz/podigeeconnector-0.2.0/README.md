# Podigee Connector

This is a simple library for connecting to the Podigee API.  
It can be used to export data from your dashboard at
https://app.podigee.com/analytics

## Supported Endpoints

- `/podcasts/{podcast_id}/analytics`
- `/podcasts/{podcast_id}/analytics/episodes`
- `/episodes/{episode_id}/analytics`

See `__main.py__` for all endpoints.

## Credentials

Before you can use the library, you must extract your Podigee session cookie;
they are **not** exposed through your Podigee settings.

Alternatively, you can call the login endpoint with your username and password
to get a new session cookie:

```python
from podigeeconnector import PodigeeConnector

connector = PodigeeConnector.from_credentials(
   base_url=BASE_URL,
   podcast_id=PODCAST_ID,
   username=USERNAME,
   password=PASSWORD,
)
```

## Installation

```
pip install podigeeconnector
```

## Usage as a library

```python
from podigeeconnector import PodigeeConnector

connector = PodigeeConnector(
   base_url=BASE_URL,
   podcast_id=PODCAST_ID,
   podigee_session_v5=PODIGEE_SESSION_V5,
)

end = datetime.now()
start = end - timedelta(days=30)

podcast_analytics = connector.podcast_analytics(start, end)
logger.info("Podcast Analytics = {}", json.dumps(podcast_analytics, indent=4))
```

See `__main.py__` for all endpoints.

## Development

We use [Pipenv] for virtualenv and dev dependency management. With Pipenv
installed:

1. Install your locally checked out code in [development mode], including its
   dependencies, and all dev dependencies into a virtual environment:

```sh
pipenv sync --dev
```

2. Create an environment file and fill in the required values:

```sh
cp .env.sample .env
```

3. Run the script in the virtual environment, which will [automatically load
   your `.env`][env]:

```sh
pipenv run podigeeconnector
```

To add a new dependency for use during the development of this library:

```sh
pipenv install --dev $package
```

To add a new dependency necessary for the correct operation of this library, add
the package to the `install_requires` section of `./setup.py`, then:

```sh
pipenv install
```

To publish the package:

```sh
python setup.py sdist bdist_wheel
twine upload dist/*
```

or

```sh
make publish
```

[pipenv]: https://pipenv.pypa.io/en/latest/index.html#install-pipenv-today
[development mode]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[env]: https://pipenv.pypa.io/en/latest/advanced/#automatic-loading-of-env
