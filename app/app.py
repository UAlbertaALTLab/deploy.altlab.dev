import hmac
import logging
import os
from pathlib import Path
from http import HTTPStatus

from flask import Flask, request, abort

from .commands import ConnectTo, NotConfigured

# Add/change the deployments here!
DEPLOYMENTS = {
    "gunaha": NotConfigured(),
    "hello": ConnectTo("itw.altlab.dev").command("/opt/hello.altlab.dev/deploy"),
    "itwewina": ConnectTo("itwewina@itw.altlab.dev").command(
        "/opt/docker-compose/itwewina/cree-intelligent-dictionary/docker/deploy"
    ),
    "korp-frontend-dev": ConnectTo("kor.altlab.dev").command(
        "/etc/docker/compose/korp/deploy"
    ),
    "korp-frontend-prod": ConnectTo("kor.altlab.dev").command(
        "/etc/docker/compose/korp-prod/deploy"
    ),
    "speech-db": NotConfigured(),
}

KEY_DIR = Path(__file__).parent / ".."

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def get_app_secret(app_name: str) -> str:
    try:
        secret_key_file = KEY_DIR / (app_name + ".key")
        return secret_key_file.read_text()
    except FileNotFoundError:
        return ""


@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == "chunked":
        request.environ["wsgi.input_terminated"] = True


@app.route("/<app_name>", methods=["POST"])
def deploy_app(app_name: str):
    # Attempt to prevent a path traversal attack:
    # (See: https://owasp.org/www-community/attacks/Path_Traversal)
    if ".." in app_name or "/" in app_name:
        return abort(HTTPStatus.BAD_REQUEST)

    body = request.get_json()
    if not isinstance(body, dict):
        return abort(HTTPStatus.BAD_REQUEST)

    provided_secret = body.get("secret", None)
    expected_secret = get_app_secret(app_name)
    if expected_secret == "":
        return abort(HTTPStatus.NOT_FOUND)

    # constant-time compare with compare_digest; it accepts ASCII strings or
    # byte string, so encode to bytes to prevent TypeError
    if not hmac.compare_digest(
        provided_secret.encode("ASCII"), expected_secret.encode("ASCII")
    ):
        return abort(HTTPStatus.UNAUTHORIZED)

    logger.info("%s: accepted secret", app_name)

    if command := DEPLOYMENTS.get(app_name):
        command.run()
        logger.info("%s: successfully redeployed", app_name)
        return "deploy script completed successfully"

    return "Secret accepted, but deploy mechanism not yet configured."


if __name__ == "__main__":
    app.run()
