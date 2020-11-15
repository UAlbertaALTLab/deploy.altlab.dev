from flask import Flask, request

app = Flask(__name__)


def get_app_secret(app_name: str) -> str:
    """
    get the secret of the app
    """
    # todo: actually get the secret of the app
    return "123456abc"


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


@app.route('/<app_name>', methods=["POST"])
def hello_world(app_name):
    received_secret = get_secret()

    real_secret = get_app_secret(app_name)

    if real_secret == received_secret:
        result = "secret is correct! app deployed!"
    else:
        result = "secret is incorrect!"

    return result


if __name__ == '__main__':
    app.run()
