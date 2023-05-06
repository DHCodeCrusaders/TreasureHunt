def build_response(message="", data=None):
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
    if not records:
        return None

    is_single = False
    if not isinstance(records, list):
        records = [records]
        is_single = True

    data = [
        {
            key: value
            for key, value in record.__dict__.items()
            if key != "_sa_instance_state"
        }
        for record in records
    ]

    if is_single:
        data = data[0]
    return data
