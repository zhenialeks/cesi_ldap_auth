#!/usr/bin/env python3
import argparse
import signal
import os
import importlib

from flask import Flask, render_template, jsonify, g, session
from flask_sqlalchemy import SQLAlchemy
from extensions import ldap

from version import __version__

db = SQLAlchemy()


def register_extensions(app):
    ldap.init_app(app)

# what for?
def register_hooks(app):
    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            g.user = {}
            g.ldap_groups = ldap.get_user_groups(user=session["user_id"])


def create_app(cesi):
    from api.v2 import register_blueprints

    app = Flask(
        __name__,
        static_folder="ui/build",
        static_url_path="",
        template_folder="ui/build",
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = cesi.database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['LDAP_HOST'] = '192.168.56.6'
    app.config['LDAP_BASE_DN'] = 'CN=Users,dc=robot,dc=local'
    app.config['LDAP_USERNAME'] = 'ironman'
    app.config['LDAP_PASSWORD'] = 'ironTEA31415'
    app.config["LDAP_ACCEPT_GROUP"] = "Administrators"
    app.config["LDAP_DOMAIN"] = "robot.local"
    # app.config['LDAP_CUSTOM_OPTIONS'] = {ldap.OPT_REFERRALS: 0}

    app.secret_key = os.urandom(24)

    db.init_app(app)

    app.add_url_rule("/", "index", lambda: render_template("index.html"))
    app.add_url_rule(
        "/api/version",
        "version",
        lambda: jsonify(status="success", version=__version__),
    )

    @app.errorhandler(404)
    @app.errorhandler(400)
    def _(error):
        return jsonify(status="error", message=error.description), error.code

    register_hooks(app)
    register_blueprints(app)
    register_extensions(app)

    return app


def configure(config_file_path):
    from core import Cesi
    from loggers import ActivityLog
    from controllers import check_database

    cesi = Cesi(config_file_path=config_file_path)
    _ = ActivityLog(log_path=cesi.activity_log)

    app = create_app(cesi)

    # Check database
    with app.app_context():
        check_database()

    # signal.signal(signal.SIGHUP, lambda signum, frame: cesi.reload())

    return app, cesi


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cesi web server")

    parser.add_argument(
        "-c", "--config-file", "--config", help="config file", required=True
    )
    parser.add_argument("--host", help="Host of the cesi", default="0.0.0.0")
    parser.add_argument("-p", "--port", help="Port of the cesi", default="5000")
    parser.add_argument(
        "--debug", help="Actived debug mode of the cesi", action="store_true"
    )
    parser.add_argument(
        "--auto-reload",
        help="Reload if app code changes (dev mode)",
        action="store_true",
    )
    parser.add_argument("--version", action="version", version=__version__)

    args = parser.parse_args()
    app, cesi = configure(args.config_file)

    app.run(
        host=args.host, port=args.port, use_reloader=args.auto_reload, debug=args.debug
    )
