# CeSI (Centralized Supervisor Interface)

CeSI is a web interface for managing multiple [supervisors][1] from the same
place.

Supervisor has its own web UI but managing multiple supervisor installations is
hard with seperate UIs (If you are using the UI of course :). CeSI aims to solve
this problem by creating a centralized web UI, based on the RPC interface of
Supervisor.

## Installation Methods

- [Chef Cookbook][2]
- [Package managers][3]
- [Docker][4] (unavailable)
- [Manuel Instructions](#manuel-instructions)

## Manuel Instructions

**Install Dependencies For Cesi Api**

```bash
$ # On Ubuntu [18.04, 16.04, 14.04]
$ sudo apt install -y git python3 python3-pip
$ # On Centos 7
$ sudo yum install -y git epel-release
$ sudo yum install -y python34 python34-pip
$ # On Fedora 28
$ sudo dnf install -y git python3 python3-pip
```

**Install Cesi**

```bash
$ export CESI_SETUP_PATH=~/cesi
$ mkdir ${CESI_SETUP_PATH}
$ cd ${CESI_SETUP_PATH}

$ # Download the project to ~/cesi directory
$ git clone https://github.com/zhenialeks/cedi_ldap_auth.git

$ # Create virtual environment and install requirement packages
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt

$ # Run with command line
(venv) $ python3 ${CESI_SETUP_PATH}/cesi/run.py --config-file ${CESI_SETUP_PATH}/defaults/cesi.conf.toml
```

**Running Cesi with uWSGI**

You may want to run Cesi using uWSGI (or any other WSGI deamon). Configure your system in the similiar way to running as a service and use `uwsgi` to start app. Check `defaults/cesi-uwsgi.ini` for details.

While running with uWSGI Cesi config host and port are ignored.

## First Login

Please change LDAP-options in run.py file to yours

## TODO
- [ ] Check passwords with special characters
- [x] Refactor some places (like, remove decorators)
- [x] Test LDAP-login
- [ ] Separate app's config and ldap's config

[1]: http://supervisord.org/
[2]: https://github.com/gamegos/cesi-cookbook/
[3]: https://github.com/gamegos/cesi-packaging/
[4]: https://hub.docker.com/r/gamegos/cesi/
