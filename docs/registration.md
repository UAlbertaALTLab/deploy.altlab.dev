# Application Registration

To register an ALTLab application with the deployment server:

1. ssh into the `altlab-gw` server.
1. cd to `opt/deploy.altlab.dev`.
1. Generate a secret key for the app: `sudo python3 generate-secret.py {app_name}`.
1. This will create a key file at `{app_name}.key`. Use this key as the app secret when sending a POST request to that app's endpoint. (See the [API](./API.md) notes.)
1. You will likely need to update the code in [`app.py`](https://github.com/UAlbertaALTLab/deploy.altlab.dev/blob/531422966d99806e13900fb17305c6cf1af55530/app/app.py#L68-L79) to handle the webhook request and run the appropriate deployment script on ALTLab's server.
