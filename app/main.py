import os, time, redis
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@db:5432/flask_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cache = redis.Redis(host='redis', port=6379)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Пытаемся создать таблицы, пока база не ответит
for i in range(10):
    try:
        with app.app_context():
            db.create_all()
        break
    except Exception:
        print(f"Waiting for DB... attempt {i+1}")
        time.sleep(3)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cached = cache.get(f"user:{id}")
    if cached:
        return jsonify({"username": cached.decode('utf-8'), "source": "redis_cache"})

    user = User.query.get(id)
    if user:
        cache.setex(f"user:{id}", 60, user.username)
        return jsonify({"username": user.username, "source": "database"})
    return jsonify({"error": "Not found"}), 404