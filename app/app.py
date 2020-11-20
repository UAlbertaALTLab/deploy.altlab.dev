from pathlib import Path

from flask import Flask, request, render_template

from subprocess import call

import os

app = Flask(__name__)


def get_app_secret(app_name: str) -> str:
    """
    get the secret of the app
    """
    # todo: actually get the secret of the app from server
    secret_key_file = Path(Path(app_name).parents[0], Path(app_name).stem).with_suffix(
        ".key"
    )

    f = open(secret_key_file)
    real_key = f.read()
    return real_key




def get_secret() -> str:
    """
    get secret from request
    """

    raw_secret = request.get_data().decode('utf-8')
    # we expect raw_secret looks like "secret=xxxxxx"

    start = "secret="
    if raw_secret.startswith(start):
        secret_content = raw_secret[len(start):]
    else:
        raise ValueError("Secret expected in request data but not found")

    return secret_content


@app.route('/')
def hello_world():
   return "deploy.altlab.dev is running!"


@app.route('/<app_name>', methods=["POST"])
def secret_assert(app_name):
    received_secret = get_secret()      #The secret received from the POST request

    real_secret = get_app_secret(app_name)  #The secret stored in the server exp. /opt/secret

    if real_secret == received_secret:
        env = os.getenv("FLASK_ENV")
        if env == "development":
            call(["ssh","altlab.dev","ssh","deploy@altlab-itw","docker","pull","docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest:latest","docker","run","--rm","docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest"])
            # call(["ssh", "altlab.dev", "ssh", "deploy@altlab-itw", "docker", "pull",
            #       "docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest:latest", "systemctrl", "restart",
            #       "hello.altlab.service"])
        else:
            call(["ssh","deploy@altlab-itw","docker","pull","docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest:latest","systemctrl","restart","hello.altlab.service"])


        result = "secret is correct! app deployed!"
    else:
        result = "secret is incorrect!"

    return result




# sysremctl restart hello.altlab.service


if __name__ == '__main__':

    app.run()

