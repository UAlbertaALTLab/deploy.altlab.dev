import hmac
import logging
import os
from pathlib import Path
from subprocess import check_call

from flask import Flask, request, abort

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

logger.debug("flask started")

app = Flask(__name__)

KEY_DIR = Path(__file__).parent / '..'

def get_app_secret(app_name: str) -> str:
    try:
        secret_key_file = KEY_DIR / (app_name + ".key")
        return secret_key_file.read_text()
    except FileNotFoundError:
        return None


@app.before_request
def fix_transfer_encoding():
    """
    Sets the "wsgi.input_terminated" environment flag, thus enabling
    Werkzeug to pass chunked requests as streams.  The gunicorn server
    should set this, but it's not yet been implemented.
    """

    transfer_encoding = request.headers.get("Transfer-Encoding", None)
    if transfer_encoding == u"chunked":
        request.environ["wsgi.input_terminated"] = True


@app.route('/')
def hello_world():
   return "deploy.altlab.dev is running!"


@app.route('/<app_name>', methods=["POST"])
def secret_assert(app_name):
    if '..' in app_name or '/' in app_name:
        return abort(401)

    body = request.get_json()
    if not isinstance(body, dict):
        return abort(401)

    provided_secret = body.get('secret', None)
    expected_secret = get_app_secret(app_name)
    if expected_secret is None:
        return abort(401)

    # constant-time compare with compare_digest; it accepts ASCII strings or
    # byte string, so encode to bytes to prevent TypeError
    if not hmac.compare_digest(provided_secret.encode("UTF-8"), expected_secret.encode('UTF-8')):
        return abort(401)

    logger.info(f"Accepted secret for {app_name}")

    if app_name == 'korp-frontend-dev':
        check_call(['ssh', 'kor.altlab.dev', '/etc/docker/compose/korp/deploy'])
        logger.info("deployment done")
        return "deploy script completed successfully"
    elif app_name == 'korp-frontend-prod':
        check_call(['ssh', 'kor.altlab.dev', '/etc/docker/compose/korp-prod/deploy'])
        logger.info("deployment done")
        return "deploy script completed successfully"
    elif app_name == 'itwewina':
        check_call(['ssh', 'itwewina@itw.altlab.dev', '/opt/docker-compose/itwewina/cree-intelligent-dictionary/docker/deploy'])
        logger.info("deployment done")
        return "deploy script completed successfully"

    return "Secret accepted, but deploy mechanism not yet configured.\n"


if __name__ == '__main__':
    app.run()
