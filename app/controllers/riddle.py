from flask import Blueprint, jsonify, make_response

from app.database.models import Riddles, db_session
from app.utils.openai import gpt
from app.utils.utils import build_response

riddle_blueprint = Blueprint("riddle", __name__)


@riddle_blueprint.route("/riddle/generate", methods=["GET"])
def riddle_generate():
    data = gpt.riddle_generate()

    riddle = Riddles(
        riddle=data.get("riddle"), hints=data.get("hints"), answer=data.get("answer")
    )
    db_session.add(riddle)
    db_session.commit()

    response = build_response(data=data)

    return response, 200
