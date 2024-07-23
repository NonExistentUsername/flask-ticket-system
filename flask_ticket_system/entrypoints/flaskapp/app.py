from flask import Flask

from flask_ticket_system.entrypoints.flaskapp.endpoints import create_ticket

app = Flask(__name__)

app.add_url_rule("/ticket", view_func=create_ticket, methods=["POST"])

if __name__ == "__main__":
    app.run()
