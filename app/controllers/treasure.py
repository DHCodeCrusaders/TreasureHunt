from flask import Blueprint, g, request

from app.database.schema import Riddles, Treasures, Winners, db_session
from app.utils.decorators import login_required
from app.utils.openai import gpt
from app.utils.utils import build_response, records_to_json

treasure_blueprint = Blueprint("treasures", __name__)


@treasure_blueprint.route("/treasure/<string:treasure_secret>", methods=["GET"])
@login_required
def treasure_info(treasure_secret):
    treasure = (
        db_session.query(Treasures).filter_by(treasure_secret=treasure_secret).first()
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

    data = records_to_json(treasure)

    riddle_data = (
        db_session.query(Riddles.riddle, Riddles.hints)
        .filter(Riddles.riddle_id == treasure.riddle_id)
        .first()
    )

    data["riddle"] = None
    if riddle_data:
        riddle, hints = riddle_data
        data["riddle"] = {"riddle": riddle, "hints": hints}

    response = build_response(data=data)

    return response, 200


@treasure_blueprint.route("/treasure/claim", methods=["POST"])
@login_required
def treasure_claim():
    user_id = g.login_details.get("user_id")
    request_data = request.get_json()
    treasure_secret = request_data.get("treasure_secret")
    riddle_answer = request_data.get("riddle_answer")

    treasure = (
        db_session.query(Treasures)
        .filter(Treasures.treasure_secret == treasure_secret)
        .first()
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

    new_winner = Winners(treasure_id=treasure.treasure_id, user_id=user_id)
    db_session.add(new_winner)
    db_session.commit()

    response = build_response(message=treasure.win_message)

    return response, 200
