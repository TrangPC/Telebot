from flask import jsonify


def error_handler(e):
    if isinstance(e, ValueError):
        return jsonify({"[ERROR]: Invalid input data!"}), 400
    else:
        return jsonify({"[ERROR] Server error!"}), 500
