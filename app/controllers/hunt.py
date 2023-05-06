from datetime import datetime

from flask import Blueprint

from app.database.schema import Hunts, Riddles, Treasures, Winners, db_session
from app.utils.decorators import login_required
from app.utils.utils import build_response, records_to_json

hunt_blueprint = Blueprint("hunts", __name__)


@hunt_blueprint.route("/list", methods=["GET"])
@login_required
def get_hunts():
    now = datetime.utcnow()
    hunts = db_session.query(Hunts).filter(Hunts.end_date > now).all()

    for hunt in hunts:
        hunt.has_started = False
        if hunt.start_date < now:
            hunt.has_started = True

    data = records_to_json(hunts)

    response = build_response(data=data)

    return response, 200


@hunt_blueprint.route("/<int:hunt_id>", methods=["GET"])
@login_required
def hunt_details(hunt_id):
    now = datetime.utcnow()
    hunt = db_session.query(Hunts).filter(Hunts.hunt_id == hunt_id).first()

    if not hunt:
        return build_response(message="Hunt not found"), 404

    if hunt.start_date < now:
        hunt.has_started = True
    else:
        hunt.has_started = False

    treasures_data = []
    if hunt.has_started:
        treasures = (
            db_session.query(Treasures).filter(Treasures.hunt_id == hunt_id).all()
        )

        for treasure in treasures:
            riddle = (
                db_session.query(Riddles)
                .filter(Riddles.riddle_id == treasure.riddle_id)
                .first()
            )

            if riddle:
                riddle_data = {
                    "riddle": riddle.riddle,
                    "hints": riddle.hints,
                }
            else:
                riddle_data = None

            winner = (
                db_session.query(Winners)
                .filter(Winners.treasure_id == treasure.treasure_id)
                .first()
            )

            winner_id = winner.user_id if winner else None

            treasures_data.append(
                {
                    "title": treasure.title,
                    "description": treasure.description,
                    "photo_url": treasure.photo_url,
                    "token": treasure.treasure_secret,
                    "winner_id": winner_id,
                    "riddle": riddle_data,
                }
            )

    data = records_to_json(hunt)
    data["treasures"] = treasures_data

    response = build_response(data=data)

    return response, 200
