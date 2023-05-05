from flask import Blueprint

from app.database.models import Hunts, db_session
from app.utils.utils import build_response, records_to_json

hunt_blueprint = Blueprint("hunts", __name__)


@hunt_blueprint.route("/list", methods=["GET"])
def get_hunts():
    hunts = db_session.query(Hunts).all()
    data = records_to_json(hunts)

    response = build_response(data=data)

    return response, 200
