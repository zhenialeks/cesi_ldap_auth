# CeSI (Centralized Supervisor Interface) with LDAP authentication

CeSI is a web interface for managing multiple [supervisors][1] from the same
place.

It's fork of [CeSi repo][0] modified for purpose of using only LDAP authentication

Tested only on Ubuntu 14.04

## Installation Methods

- [Manuel Instructions](#manuel-instructions)

## Manuel Instructions

**Install Dependencies For Cesi Api and compiling**

```bash
$ # On Ubuntu [18.04, 16.04, 14.04]
$ sudo apt install -y python3-pip build-essential libsasl2-dev python3-dev libldap2-dev libssl-dev libpq-dev python3.4-venv
```

**Install Cesi**

```bash
$ export CESI_SETUP_PATH=/opt/cesi
$ mkdir ${CESI_SETUP_PATH}
$ cd ${CESI_SETUP_PATH}

$ # Download the project to ~/cesi directory
$ git clone https://github.com/zhenialeks/cesi_ldap_auth.git

$ # Create virtual environment and install requirement packages
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt

$ # Installing Yarn to build GUI:
$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
$ sudo apt-get update && sudo apt-get install yarn

$ # Building UI:
$ cd ${CESI_SETUP_PATH}/cesi/ui
$ yarn install
$ yarn build


# If yarn doesn't worked out, you should update npm and reinstall yarn, then try again

$ # Run with command line
(venv) $ python3 ${CESI_SETUP_PATH}/cesi/run.py --config-file ${CESI_SETUP_PATH}/defaults/cesi.conf.toml
```

**Running Cesi with mod_wsgi**

You may want to run Cesi using Apache2, with mod_wsgi.

First of all, you should install mod_wsgi:
``` 
sudo apt-get install libapache2-mod-wsgi-py3
```

After that you have to make `cesi.wsgi` file and place it nearby `run.py`. You can see it at `/etc/cesi.wsgi`'

Also, you have to put `activate_this.py` from `/etc/activate_this.py` to `${CESI_SETUP_PATH}/venv/bin/activate_this.py`

Then, add apache2 configuration file (from `/etc/cesi_conf.conf`) to `sites-available` folder

And finally, 
```
$ cd /etc/apache2/sites-enabled
$ sudo ln -s ../sites-available/cesi_conf.conf cesi_conf.conf

$ # Restarting apache
$ sudo service apache2 restart
```
That's it! 


[0]: https://github.com/gamegos/cesi
[1]: http://supervisord.org/
[2]: https://github.com/gamegos/cesi-cookbook/
[3]: https://github.com/gamegos/cesi-packaging/
[4]: https://hub.docker.com/r/gamegos/cesi/
