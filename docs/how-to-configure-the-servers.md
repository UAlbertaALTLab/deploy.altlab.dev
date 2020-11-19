How to configure the servers
============================

The deployment infrastructure defines two types of machines:

 - the host server — the machine that runs <https://deploy.altlab.dev/> proper
 - application server — any machine that runs an application managed by
   the deployment infrastructure

As of 2020-11-19, the **host server** is `altlab-gw`. The application
server is `altlab-itw` but we will want to add `altlab-kor` and
`altlab-db` as **application servers**.

This documentation assumes an **Ubuntu/Debian Linux distribution**.
Details may vary for other distributions of Linux.


How to configure the host server
--------------------------------

> As of 2020-11-19, this machine is `altlab-gw`

The **host server** listens for requests on the internet, with the end goal
to reload and restart an application on the **application server**.

Since the **host server** needs to run privileged commands on
application servers, we make use of a [Unix system user][system-user]
than can use its own SSH public/private key pair to login to
**application servers**.

[system-user]: https://unix.stackexchange.com/a/80279/398081


### Setting up the system user

The Flask application should run as a system user with a home folder and
an SSH key pair.

We'll call this user **`deploy`**.

<aside>
In hindsight, a more descriptive user name would have been `deploy-host`.
</aside>


#### Create a system user called `deploy`

```sh
sudo useradd --system \
    --create-home --home /var/lib/deploy \
    --shell $(which nologin) \
    deploy
```

The `deploy` user's home directory is `/var/lib/deploy`. [`/var/lib` is
where state information for packages is stored in Linux][fhs-var-lib].

[fhs-var-lib]: https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch05s08.html

The shell is `nologin`, which, as its name implies, forbids the user
from logging in. Indeed, system users do not have valid passwords.
`nologin` will also write a log entry in `/var/log/auth.log` of any
attempts to login with this account.

Then how will the `deploy` user authenticate themselves via SSH?

#### Create an SSH key pair for the deploy user

We will setup an SSH directory in the deploy user's home directory.

Set a convenient variable to avoid typing `/var/lib/deploy` all the
time:

```sh
DEPLOYHOME=/var/lib/deploy
```

Now let's create the private SSH directory for the `deploy` user:

```sh
sudo mkdir -m 700 $DEPLOYHOME/.ssh
sudo chown deploy:deploy $DEPLOYHOME/.ssh
```

Now create the SSH key pair in this folder:

```
sudo -u deploy ssh-keygen -C "deploy@$HOST" -N '' -f $DEPLOYHOME/.ssh/id_rsa
```

This creates a new password-less (`-N ''`) RSA key pair in
`$DEPLOYHOME/.ssh/id_rsa`. You may now view the public key:

```sh
sudo cat $DEPLOYHOME/.ssh/id_rsa.pub
```

Copy this file, as we'll need it for setup on the **application
servers**.


#### Ensure the deploy application is running as the `deploy` user

This depends on the environment. If you are created a systemd unit file for
the deploy.altlab.dev application, make sure [to set its user
appropriately][systemd.exec]:

```
User=deploy
```

[systemd.exec]: https://www.freedesktop.org/software/systemd/man/systemd.exec.html#Credentials
