# API

`deploy.altlab.dev` exposes a small API consisting of webhooks that trigger deployment for each application.

Each ALTLab application has its own endpoint:

`https://deploy.altlab.dev/{app-name}`

You can trigger deployment of the application by sending a POST request to the app's endpoint. `deploy.altlab.dev` will then run the deployment script for that application.

The body of the POST request should be a JSON object with a single parameter `secret`, whose value is the secret key generated when you registered the app with the API. (See [app registration](./registration.md).)

Because the webhook triggers long-running deployment processes, the request will likely time out. This is currently expected behavior.

Other errors currently all return a 401 status code.
