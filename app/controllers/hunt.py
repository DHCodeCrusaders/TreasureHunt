from flask import Blueprint

from app.database.schema import Hunts, db_session
from app.utils.decorators import login_required
from app.utils.utils import build_response, records_to_json

hunt_blueprint = Blueprint("hunts", __name__)


@hunt_blueprint.route("/list", methods=["GET"])
@login_required
def get_hunts():
    hunts = db_session.query(Hunts).all()
    data = records_to_json(hunts)

    response = build_response(data=data)

    return response, 200
