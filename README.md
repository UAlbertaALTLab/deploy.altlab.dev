# deploy.altlab.dev
Enables web application redeployment via HTTPS.

## How deployment works

When a developer pushes to the default branch of one of our apps (e.g.,
gunaha), it starts a few GitHub workflows that build a Docker image of
the application; later, this app, <https://deploy.altlab.dev/> is used
to pull the image and redeploy the application in our private network:

![Sequence diagram of our deployment process](./docs/Deployment.svg)

## How to configure the servers

Please see [How to configure the servers](./docs/how-to-configure-the-servers.md).

## Notes about the production environment

The docker service should restart all running containers when restarted. See <https://stackoverflow.com/a/18797089/6626414>
