from flask import jsonify

def not_found_error(error):
    return jsonify({"error": "Not Found"}), 404

def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

def init_app(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
