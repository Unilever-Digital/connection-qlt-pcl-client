from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)
from app.models.dbmodel import *
from app.controls.control import *

event = Blueprint("event", __name__)


@event.route("/button_click",  methods=["POST", "GET"])
def event_schedule():
    if request.method == "POST":
        conn = connectToSqlServer(
            "localhost", "Vision_Mas140", "sa", "Password.1")
        data = tableSqlServerFetch(conn, "Table_ResultCarton", columns=[
                                   "ID", "DateTime", "Line", "SKUID", "ProductName", "Barcode", "Status", "Reject"])
        return jsonify(data)
