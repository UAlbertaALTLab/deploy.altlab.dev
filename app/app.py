from pathlib import Path

from flask import Flask, request

from subprocess import call

import os

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


logger.debug("flask started")


app = Flask(__name__)

ENV = os.getenv("FLASK_ENV")
if ENV == "development":
    KEY_DIR = Path("/home/serena/PycharmProjects/deploy.altlab.dev")
else:
    KEY_DIR = Path("/opt/deploy.altlab.dev")

def get_app_secret(app_name: str) -> str:
    """
    get the secret of the app
    """


    # Note: Pathlib.with_suffix function fails when `app_name` has periods in it
    # as it strips the last suffix and changes it
    # for example Path("hello.altlab.dev").with_suffix(".key") will evaluate to Path("hello.altlab.key")
    # while what we want is actually Path("hello.altlab.dev.key")
    # so we shouldn't use Pathlib.with_suffix here:
    secret_key_file = Path((KEY_DIR / (app_name + ".key")))

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
    logger.debug("getting raw secret:")
    logger.debug(raw_secret)
    if raw_secret.startswith(start):
        secret_content = raw_secret[len(start):]
    else:
        raise ValueError("Secret expected in request data but not found")

    return secret_content

def get_port() -> str:
    """
    get port from request
    """

    raw_port = request.get_data().decode('utf-8')
    # we expect raw_secret looks like "secret=xxxxxx"

    start = "port="
    logger.debug("getting raw port:")
    logger.debug(raw_port)
    if raw_port.startswith(start):
        real_port = raw_port[len(start):]
    else:
        raise ValueError("The port of app expected in request data but not found")

    return real_port


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
    logger.debug("This is env vars:")
    logger.debug(os.environ)

    received_secret = get_secret()      #The secret received from the POST request
    app_port = get_port()
    logger.debug(received_secret)
    logger.debug(app_name)

    real_secret = get_app_secret(app_name)  #The secret stored in the server exp. /opt/secret

    logger.debug(real_secret)

    app_list_itw = ["hello.altlab.dev", "gunaha"]
    app_list_kor = ["korp"]

    if real_secret == received_secret:
        if app_name in app_list_itw:

            if ENV == "development":
                call(["ssh","altlab.dev","ssh","deploy@altlab-itw","docker","pull","docker.pkg.github.com/ualbertaaltlab/hellotest/hellotest:latest","docker","run","--rm","docker.pkg.github.com/ualbertaaltlab/hellotest/hellotest"])
                # call(["ssh", "altlab.dev", "ssh", "deploy@altlab-itw", "docker", "pull",
                #       "docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest:latest", "systemctrl", "restart",
                #       "hello.altlab.service"])
            else:
                call(["ssh", "deploy@altlab-itw",
                      "docker", "pull", "docker.pkg.github.com/ualbertaaltlab/" + app_name + "/" + app_name + ":latest", "&&",
                      "docker", "run", "--rm", "--name=" + app_name, "-d", "-p", app_port + ":" + app_port , "docker.pkg.github.com/ualbertaaltlab/" + app_name + "/" + app_name])
                # call(["ssh","deploy@altlab-itw", "docker", "pull", "docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest:latest","&&", "docker", "run", "--rm","--name=hellotest", "-d", "-p", "5000:5000", "docker.pkg.github.com/ualbertaaltlab/hello.altlab.dev/hellotest"])
                # TODO: Configeration automation for docker login
                # Every image in GItHub packeges is associated with a user and a TOKEN. Usually it can be setup by automation, see an example here: https://github.com/UAlbertaALTLab/hellotest/blob/production/.github/workflows/test-and-publish.yml#L59-L70
                # The following command have to be run as user deploy before used for a new repository:
                # cat /path/to/TOKEN.txt | docker login https://docker.pkg.github.com -u USERNAME --password-stdin
        elif app_name in app_list_kor:
            call(["ssh", "deploy@altlab-kor",
                  "docker", "pull", "docker.pkg.github.com/ualbertaaltlab/" + app_name + "/" + app_name + ":latest", "&&",
                  "docker", "run", "--rm", "--name=" + app_name, "-d", "-p", app_port + ":" + app_port, "docker.pkg.github.com/ualbertaaltlab/" + app_name + "/" + app_name
                  ])
            #TODO: setup user deploy on kor
        else:
            raise NameError ("name" + app_name + "is not defined! Please see https://github.com/UAlbertaALTLab/deploy.altlab.dev/blob/master/docs/how-to-configure-the-servers.md")


        result = "secret is correct! app deployed!"
    else:
        result = "secret is incorrect!"

    return result




# sysremctl restart hello.altlab.service


if __name__ == '__main__':

    app.run()

