def build_response(message="", data=[]):
    """
    Base API signature
    """
    responses = {
        "message": message,
        "data": data,
    }

    return responses


def records_to_json(records):
    """
    Convert SQLAlchemy records to JSON
    """
    data = [
        {
            key: value
            for key, value in record.__dict__.items()
            if key != "_sa_instance_state"
        }
        for record in records
    ]

    return data
