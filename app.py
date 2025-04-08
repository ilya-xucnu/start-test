import redis
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/ping')
def ping():
    return jsonify({"status": "ok"})

@app.route('/health')
def health():
    try:
        redis_client.ping()
        logging.info('handling /health: {"status": "ok", "redis": "alive"}')
        return jsonify({"status": "ok", "redis": "alive"})
    except redis.exceptions.RedisError:
        logging.info('handling /health: {"status": "degraded", "redis": "dead"}')
        return jsonify({"status": "degraded", "redis": "dead"}), 503

@app.route('/count')
def count():
    try:
        visits = redis_client.incr('visits')
        logging.info(f'handling /count: {{"visits": {visits}}}')
        return jsonify({"visits": visits})
    except redis.exceptions.RedisError as e:
        logging.info(f'handling /count: {"error": "Redis is down, we are doomed"}')
        return jsonify({"error": "Redis is down, we are doomed"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
