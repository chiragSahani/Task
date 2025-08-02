from flask import Flask, jsonify, request, redirect, abort
from .models import url_store
from .utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL not provided"}), 400

    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = generate_short_code()
    while url_store.get_url(short_code) is not None:
        short_code = generate_short_code()

    url_store.add_url(short_code, long_url)

    short_url = request.host_url + short_code
    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@app.route('/<string:short_code>', methods=['GET'])
def redirect_to_url(short_code):
    long_url = url_store.increment_clicks(short_code)
    if long_url:
        return redirect(long_url)
    else:
        abort(404)

@app.route('/api/stats/<string:short_code>', methods=['GET'])
def get_url_stats(short_code):
    stats = url_store.get_stats(short_code)
    if stats:
        return jsonify(stats), 200
    else:
        return jsonify({"error": "Short code not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)