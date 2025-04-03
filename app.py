import redis
from flask import Flask, jsonify

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/count')
def count():
    visits = redis_client.incr('visits')
    return jsonify({"visits": visits})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
