from flask import jsonify

def handle_error(status_code, message):
    return jsonify({"error": message}), status_code

def not_found_error(error):
    return handle_error(404, "Not Found")

def internal_error(error):
    return handle_error(500, "Internal Server Error")

def bad_request_error(message="Bad Request"):
    return handle_error(400, message)

def unauthorized_error(message="Unauthorized"):
    return handle_error(401, message)

def forbidden_error(message="Forbidden"):
    return handle_error(403, message)

def conflict_error(message="Conflict"):
    return handle_error(409, message)

def init_app(app):
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)
    # Custom error handlers can be registered here if needed
    # For example:
    # app.register_error_handler(AuthError, handle_auth_error)
