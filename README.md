# core

The most amazing SaaS application the world has ever seen!

## Summary

- backend code is mainly under apps/web/views
- frontend code is under templates/web


## Installation

Setup a virtualenv and install requirements:

```bash
mkvirtualenv --no-site-packages core -p python3
pip install -r requirements.txt
```

## Running server

```bash
./manage.py runserver
```

## Running Celery

Celery can be used to run background tasks. To run it you can use:

```bash
celery -A core worker -l info
```


## Running Tests

To run tests simply run:

```bash
./manage.py test
```

Or to test a specific app/module:

```bash
./manage.py test apps.utils.tests.test_slugs
```


On Linux-based systems you can watch for changes using the following:

```bash
ack --python | entr python ./manage.py test
```
