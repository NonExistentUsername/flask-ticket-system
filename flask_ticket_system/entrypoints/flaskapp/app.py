from flask import Flask

from flask_ticket_system.entrypoints.flaskapp.endpoints import (
    create_ticket,
    login,
    view_ticket,
)

app = Flask(__name__)

app.add_url_rule("/login/", view_func=login, methods=["POST"])

app.add_url_rule("/ticket/", view_func=create_ticket, methods=["POST"])
app.add_url_rule("/ticket/<int:ticket_id>/", view_func=view_ticket, methods=["GET"])


if __name__ == "__main__":
    app.run()
