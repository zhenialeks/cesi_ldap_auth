from flask import Blueprint, jsonify, session, request, g, current_app

from decorators import is_user_logged_in, is_admin
from loggers import ActivityLog
# from models import User
from extensions import ldap

auth = Blueprint("auth", __name__)
activity = ActivityLog.getInstance()


@auth.route("/login/", methods=["POST"])
def login():
    data = request.get_json()
    user_credentials = {}
    invalid_fields = []
    require_fields = ["username", "password"]
    for field in require_fields:
        value = data.get(field)
        if value is None:
            invalid_fields.append(field)

        user_credentials[field] = value

    if invalid_fields:
        return (
            jsonify(status="error", message="Please enter valid value for '{}' fields"
                    .format(",".join(invalid_fields)),
                    ),
            400,
            )
    ldap_test = None
    try:
        ldap_test = ldap.bind_user(user_credentials["username"], user_credentials["password"])
    except Exception as e:
        activity.logger.info("LDAP exception[{}]".format(e))
        print("During ldap.bind_user call an exception has occurred:{}".format(e))

    if ldap_test is not None:
        if user_credentials["password"] != "":
            session["groups"] = ldap.get_user_groups(user=user_credentials["username"])

            if session["groups"] and current_app.config['LDAP_ACCEPT_GROUP'] in session["groups"]:
                # success
                session["username"] = user_credentials["username"]
                session["logged_in"] = True
                session["ldap_login"] = True
                activity.logger.info("{} logged in through LDAP".format(session["username"]))
                return jsonify(status="success", message="Valid username/password")
            else:
                return jsonify(status="error", message="User doesn't have permission"), 403
        else:
            return jsonify(status="error", message="Accounts with empty password are not allowed to log in"), 403
    else:
        return jsonify(status="error", message="Invalid username/password"), 403


@auth.route("/logout/", methods=["POST"])
def logout():
    username = session.get("username")
    if username is None:
        return jsonify(status="error", message="You haven't already entered"), 403

    activity.logger.info("{} logged out".format(username))
    session.clear()
    return jsonify(status="success", message="Logout")
