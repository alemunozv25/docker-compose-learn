from flask import Flask
import redis
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0) # 'redis' is the service name in docker-compose

# define metrics usage
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='0.0.2')

@app.route('/')
def hello():
    count = r.incr('visits')
    return f"Hello from Flask! You are visitor number {count}."

@app.route('/metrics')
def main():
    pass  # requests tracked by default

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
