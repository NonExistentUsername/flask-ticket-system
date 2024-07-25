from flask import Flask

from flask_ticket_system.entrypoints.flaskapp.admin_endpoints import (
    add_permission_to_group,
    add_user_to_group,
    create_group,
)
from flask_ticket_system.entrypoints.flaskapp.endpoints import (
    create_ticket,
    login,
    view_ticket,
)

app = Flask(__name__)


app.add_url_rule("/login/", view_func=login, methods=["POST"])

app.add_url_rule("/ticket/", view_func=create_ticket, methods=["POST"])
app.add_url_rule("/ticket/<int:ticket_id>/", view_func=view_ticket, methods=["GET"])


app.add_url_rule("/admin/group/", view_func=create_group, methods=["POST"])
app.add_url_rule("/admin/group/user/", view_func=add_user_to_group, methods=["POST"])
app.add_url_rule(
    "/admin/group/permission/",
    view_func=add_permission_to_group,
    methods=["POST"],
)

if __name__ == "__main__":
    app.run()
