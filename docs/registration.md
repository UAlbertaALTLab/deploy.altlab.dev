# Application Registration

## How to register an application

To register an ALTLab application with the deployment server:

1. Check the [application registry][registry] to select an unused ports and unused UID/GID!
1. SSH into the `altlab-gw` server.
1. `cd` into `/opt/deploy.altlab.dev`.
1. Generate a secret key for the app: `sudo python3 generate-secret.py {app_name}`.
1. This will create a key file at `{app_name}.key`. Use this key as the app secret when sending a POST request to that app's endpoint. (See the [API][] notes.)
1. Update [`app/configuration.py`][config] by adding code to run the deployment script for the app.
1. Update [`docs/application-registry.tsv`][registry] by adding the name, ports, and UID/GID for your application.

[config]: ../app/configuration.py
[registry]: ./application-registry.tsv
[API]: ./API.md

## Existing applications

The [application registry][registry] is a spreadsheet that contains the
following fields:

### Application

The is the `{app_name}`.

### UID/GID

The Unix User ID and Group ID. Both the user ID and the group ID should
be the same integer, and kept consistent on both `altlab-gw` and
whichever servers have the application deployed.

The integer _should_ be greater than 60000.

### Listening on...

The hostname and port being used by the application. The port _should_
be based on the UID/GID (same last 3 decimal digits).
