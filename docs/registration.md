# Application Registration

To register an ALTLab application with the deployment server:

1. ssh into the `altlab-gw` server.
1. cd to `/opt/deploy.altlab.dev`.
1. Generate a secret key for the app: `sudo python3 generate-secret.py {app_name}`.
1. This will create a key file at `{app_name}.key`. Use this key as the app secret when sending a POST request to that app's endpoint. (See the [API](./API.md) notes.)
1. Update `app/configuration.py` by adding code to run the deployment script for the app.
