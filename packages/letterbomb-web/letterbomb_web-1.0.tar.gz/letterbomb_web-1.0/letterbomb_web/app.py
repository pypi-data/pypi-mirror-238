#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""
This is the **Flask** component for ``letterbomb``, rebuilt for modern web-browsers.

Obtain the latest copy of LetterBomb at https://gitlab.com/whoatemybutter/letterbomb.

LetterBomb is licensed under the MIT license. You can obtain a copy at https://mit-license.org/.

.. note:: This exploit only works for System Menu 4.3. 4.2 and below will not work.
"""
import json
import logging
import io
import tomllib
import typing
import urllib.parse
import urllib.request

import flask
import letterbomb

__author__ = "WhoAteMyButter"
__version__ = (1, 0)
__license__ = "MIT"

app = flask.Flask(__name__)
app.config.from_file("config.toml", tomllib.load)

logging.basicConfig(filename=app.config["log_file"], level=app.config["log_level"])
app.logger.setLevel(app.config["log_level"])

if app.debug:
    logging.basicConfig(filename=app.config["log_file"], level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

CONFIG_USE_CAPTCHA = bool(app.config["captcha_public_key"]) or bool(app.config["captcha_private_key"])
CONFIG_SHOW_VERSION = bool(app.config["show_version"])
CONFIG_SHOW_SUBLINKS = bool(app.config["show_sublinks"])
CONFIG_SHOW_RIBBON = bool(app.config["show_ribbon"])


@app.route("/")
def index() -> flask.Response:
    """Index page."""
    flask.g.recaptcha_args = f'k={app.config["captcha_public_key"]}'
    return flask.make_response(
        flask.render_template(
            "index.html",
            version=letterbomb.__version__ if CONFIG_SHOW_VERSION else "",
        )
    )


def captcha_check(timeout: float = 20.0) -> bool:
    """Check Captcha."""
    try:
        oform = {
            "privatekey": app.config["captcha_private_key"],
            "secret": app.config["captcha_private_key"],
            "remoteip": flask.request.remote_addr,
            "challenge": flask.request.form.get("g-recaptcha-challenge-field", [""]),
            "response": flask.request.form.get("g-recaptcha-response", [""]),
        }

        with urllib.request.urlopen(
            "https://www.google.com/recaptcha/api/siteverify",
            json.dumps(oform).encode("utf-8"),
            timeout=timeout,
        ) as file:
            error = file.readline().replace("\n", "")
            serialized = json.load(file)
            result = serialized.get("success", False)

        if not result:
            if error != "incorrect-captcha-sol":
                app.logger.debug("Recaptcha fail: %r, %r", oform, serialized)
                flask.g.recaptcha_args += "&error=" + error
            return False

    except ValueError:
        flask.g.recaptcha_args += "&error=unknown"
        return False
    return True


@app.route("/", methods=["POST"])
def index_post() -> tuple[flask.Response, int] | flask.Response:
    """
    API endpoint, used by client.

    :return: A response or response with status code.
    """
    if CONFIG_USE_CAPTCHA and not captcha_check():
        return (
            flask.jsonify({"success": False, "message": "Failed or incomplete Captcha."}),
            403,
        )

    try:
        data = flask.request.form
        if not (mac := str(data.get("mac"))):
            raise letterbomb.MACError()
        if not (region := str(data.get("region"))) or region.upper() not in letterbomb.REGIONS:
            raise letterbomb.RegionError()
        hackmii = bool(data.get("hackmii", False))
        bomb = typing.cast(
            io.BytesIO,
            letterbomb.write(
                mac,
                region,
                hackmii,
            ),
        ).getvalue()

        return flask.Response(
            bomb,
            200,
            {
                "Content-Disposition": 'attachment; filename="LetterBomb.zip"',
                "Content-Type": "application/zip",
                "Content-Length": str(len(bomb)),
            },
            "application/zip",
        )
    except letterbomb.MACLengthError:
        app.logger.debug(
            "Rejected bad length MAC %s",
            letterbomb.serialize_mac(flask.request.form.get("mac", "000000000000")).upper(),
        )
        error = "Not a valid MAC address."
    except letterbomb.MACEmulatedError:
        app.logger.debug(
            "Rejected emulated MAC %s", letterbomb.serialize_mac(flask.request.form.get("mac", "000000000000")).upper()
        )
        error = "Not a real Wii MAC address."
    except letterbomb.MACError:
        app.logger.debug(
            "Rejected non-Wii MAC %s", letterbomb.serialize_mac(flask.request.form.get("mac", "000000000000")).upper()
        )
        error = "Not a valid MAC address."
    except letterbomb.RegionError:
        error = "Invalid region; must be U, E, J, K."
    except ValueError:
        error = "Invalid hackmii boolean value."
    return flask.jsonify({"success": False, "message": error}), 400


def start() -> None:
    """
    Start the web application.

    Not for WSGI server deployments.
    """
    app.logger.info("Starting LetterBomb web-service %s...", ".".join(str(x) for x in letterbomb.__version__))
    app.run()


if __name__ == "__main__":
    start()
