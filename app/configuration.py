"""
Add and configure the deployments here!

To add an app called {app_name}:

 1. In the parent directory generate a secret key for {app_name}:
    sudo python3 generate-key.py {app_name}
 2. Add a line like this to DEPLOYMENTS:
    "{app_name}": ConnectTo("server").command("/path/to/redeployment-script"),

"""

from .commands import ConnectTo, NotConfigured

DEPLOYMENTS = {
    ############################## gunaha.altlab.app ################################
    # TODO: configure Gunaha (Tsuut'ina dictionary) for deployment
    "gunaha": NotConfigured(),
    ############################### hello.altlab.dev ###############################
    "hello": ConnectTo("itw.altlab.dev").command("/opt/hello.altlab.dev/deploy"),
    ############################# itwewina.altlab.app ##############################
    "itwewina": ConnectTo("itwewina@itw.altlab.dev").command(
        "/opt/docker-compose/itwewina/cree-intelligent-dictionary/docker/deploy"
    ),
    ##################################### Korp #####################################
    "korp-frontend-dev": ConnectTo("kor.altlab.dev").command(
        "/etc/docker/compose/korp/deploy"
    ),
    "korp-frontend-prod": ConnectTo("kor.altlab.dev").command(
        "/etc/docker/compose/korp-prod/deploy"
    ),
    ############################ speech-db.altlab.app ##############################
    "speech-db": ConnectTo("speech-db@itw.altlab.dev").command("/opt/speech-db/deploy"),
}
