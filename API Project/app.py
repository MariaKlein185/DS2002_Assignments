from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

# Token for authorization
AUTHORIZED_TOKEN = "mysecrettoken"

# Dictionary of some capital cities and their timezones
capital_timezones = {
    "Washington": "America/New_York",
    "Brasilia": "America/Sao_Paulo",
    "New Delhi": "Asia/Kolkata"
}

@app.route('/time')
def get_time():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token != AUTHORIZED_TOKEN:
        return jsonify({"error": "Unauthorized access. Invalid or missing token."}), 401

    city = request.args.get('city', '')
    if city not in capital_timezones:
        return jsonify({"error": f"City '{city}' not found in database."}), 404

    tz_name = capital_timezones[city]
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    offset = now.strftime('%z')
    offset_formatted = f"UTC{offset[:3]}:{offset[3:]}"  # Format UTC offset

    return jsonify({
        "city": city,
        "current_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": offset_formatted
    })

@app.route('/')
def home():
    return "Welcome to the Time API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)