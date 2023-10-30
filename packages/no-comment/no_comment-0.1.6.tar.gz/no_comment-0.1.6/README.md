# NoComment

Comment any resource on the web!


## Install

NoComment is available on PyPI under the name `no-comment`.
To install, just run `python -m pip install no-comment`.


## Configure

NoComment is configured using environment variables.
See [the `settings` module](no_comment/infrastructure/settings.py) for
a comprehensive list of configuration variables.

All the variable names must be prefixed with `NO_COMMENT_`. For instance :

```console
# The secret can be generated using the `secrets.token_hex()` function.
$ export NO_COMMENT_SECRET_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

# Additional Python database drivers might be required depending on the DSN.
$ export NO_COMMENT_DSN="sqlite:///data.sqlite"
```


## Authentication

TOTP authentication is provided to be able to login on servers that do not (yet) support
the `cryptography` module. You must install extra dependencies (`no-comment[totp]`)
and enable it explicitly by setting a base32 random secret:

```console
# The secret can be generated using the `pyotp.random_base32()` function.
$ export NO_COMMENT_TOTP_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Note that it is a highly insecure way of authenticating, as anyone gaining access to your
OTP generator would be able to login.


## Initialise

Once configured, you must initialise NoComment's database with the dedicated command:

```console
$ no-comment init-db
```


## Run

NoComment being a Flask application, it can be run using any WSGI server,
for instance, with [Gunicorn](https://gunicorn.org):

```console
$ gunicorn --access-logfile="-" -w 4 -b 127.0.0.1:3000 "no_comment.configuration.wsgi:app()"
```

You can now access the service at <http://127.0.0.1:3000/MY_STREAM_NAME>.


## Contributing

See [CONTRIBUTING.md]() to set up a development environment.
