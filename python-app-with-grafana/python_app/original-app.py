from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0) # 'redis' is the service name in docker-compose

@app.route('/')
def hello():
    count = r.incr('visits')
    return f"Hello from Flask! You are visitor number {count}."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
