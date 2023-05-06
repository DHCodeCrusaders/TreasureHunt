from datetime import datetime

from flask import Blueprint, request

from app.database.models import Hunts, Riddles, Treasures, Winners, db_session
from app.utils.decorators import login_required
from app.utils.openai import gpt
from app.utils.utils import build_response, records_to_json

treasure_blueprint = Blueprint("treasures", __name__)


@treasure_blueprint.route("/treasure/list", methods=["POST"])
@login_required
def get_treasures():
    request_data = request.get_json()
    hunt_id = request_data.get("hunt_id")

    hunt = db_session.query(Hunts).get(hunt_id)

    if not hunt:
        response = build_response(message="Hunt not found.")
        return response, 404

    if hunt.start_date > datetime.now():
        response = build_response(message="The Hunt has not started yet.")
        return response, 403

    elif hunt.end_date < datetime.now():
        response = build_response(message="The Hunt has already ended.")
        return response, 403

    hunts = db_session.query(Treasures).filter(Treasures.hunt_id == hunt_id).all()

    data = records_to_json(hunts)

    response = build_response(data=data)

    return response, 200


@treasure_blueprint.route("/treasure/<int:treasure_id>", methods=["GET"])
@login_required
def treasure_info(treasure_id):
    treasure = db_session.query(Treasures).filter_by(treasure_id=treasure_id).all()

    data = records_to_json(treasure)
    if not data:
        response = build_response(message="Treasure not found.")
        return response, 404

    response = build_response(data=data[0])

    return response, 200


@treasure_blueprint.route("/treasure/claim", methods=["POST"])
@login_required
def treasure_claim():
    request_data = request.get_json()
    treasure_id = request_data.get("treasure_id")
    riddle_answer = request_data.get("riddle_answer")

    treasure = (
        db_session.query(Treasures).filter(Treasures.treasure_id == treasure_id).first()
    )

    if not treasure:
        response = build_response(message="Treasure not found.")
        return response, 404

    winner = (
        db_session.query(Winners)
        .filter(Winners.treasure_id == treasure.treasure_id)
        .first()
    )

    if winner:
        response = build_response(message="This treasure has already been claimed.")
        return response, 403

    riddle = (
        db_session.query(Riddles)
        .filter(Riddles.riddle_id == treasure.riddle_id)
        .first()
    )

    if riddle:
        gpt_response = gpt.riddle_verify(riddle.riddle, riddle.answer, riddle_answer)
        if not gpt_response.get("correct"):
            response = {
                "message": gpt_response.get("message"),
                "success": False,
            }
            return response, 403

    new_winner = Winners(treasure_id=treasure_id, user_id=123)
    db_session.add(new_winner)
    db_session.commit()

    response = build_response(message=treasure.win_message)

    return response, 200
