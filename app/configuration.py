"""
Add and configure the deployments here!

To add an app called {app_name}:

 1. In the parent directory generate a secret key for {app_name}:
    sudo python3 generate-key.py {app_name}
 2. Add a line like this to DEPLOYMENTS:
    "{app_name}": ConnectTo("server").command("/path/to/redeployment-script"),

"""

from .commands import ConnectTo, NotConfigured, RedeploySelf

DEPLOYMENTS = {
    # gunaha.altlab.app
    # TODO: configure Gunaha (Tsuut'ina dictionary) for deployment
    "gunaha": NotConfigured(),
    # hello.altlab.dev
    "hello": ConnectTo("itw.altlab.dev").command("/opt/hello.altlab.dev/deploy"),
    # morphodict: itwewina, {itwiwina,gunaha,srseng}.altlab.dev
    "itwewina": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict/docker/deploy"
    ),
    # morphodict api: api.{itwewina, gunaha, itwiwina, arapaho, guusaaw}.altlab.dev
    "morphodict-backend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-backend/docker/deploy"
    ),
    # itwewina front-end
    "crkeng-frontend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-frontend/crkeng/docker/deploy"
    ),
    # itwiwina front-end
    "cwdeng-frontend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-frontend/cwdeng/docker/deploy"
    ),
    # gunaha front-end
    "srseng-frontend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-frontend/srseng/docker/deploy"
    ),
    # guusaaw front-end
    "hdneng-frontend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-frontend/hdneng/docker/deploy"
    ),
    # arapaho front-end
    "arpeng-frontend": ConnectTo("morphodict@itw.altlab.dev").command(
        "/opt/morphodict/home/morphodict-frontend/arpeng/docker/deploy"
    ),
    # Korp
    "korp-frontend": ConnectTo("korp@itw.altlab.dev").command(
        "/data_local/home/korp/docker-compose/deploy"
    ),
    # speech-db.altlab.app
    "speech-db": ConnectTo("speech-db@itw.altlab.dev").command("/opt/speech-db/deploy"),
    # speech-db.altlab.dev
    "speech-db-dev": ConnectTo("speech-db@itw.altlab.dev").command("/opt/speech-db-dev/deploy"),
    # semanticexplorer.altlab.dev
    "semantic-explorer": ConnectTo("morphodict@itw.altlab.dev").command("/opt/morphodict/home/vocabulary-explorer/deploy"),
    # deploy.altlab.dev
    "deploy": RedeploySelf(),
}
