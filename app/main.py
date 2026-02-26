import os
import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

app = Flask(__name__)

# Настройки БД
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:pass@db:5432/flask_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Инициализируем миграции
cache = redis.Redis(host='redis', port=6379)

# Модель данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# CREATE
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({"error": "Bad request"}), 400
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created", "id": new_user.id}), 201

# READ
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cache_key = f"user:{id}"
    cached_user = cache.get(cache_key)
    
    if cached_user:
        return jsonify({"username": cached_user.decode('utf-8'), "source": "redis_cache"})

    user = User.query.get(id)
    if user:
        cache.setex(cache_key, 60, user.username) 
        return jsonify({"username": user.username, "source": "database"})
    return jsonify({"error": "Not found"}), 404

# UPDATE
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        # Используем session.get вместо query.get (современный стандарт)
        user = db.session.get(User, id) 
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if data and 'username' in data:
            user.username = data['username']
            db.session.commit()
            
            # Очищаем кеш
            cache.delete(f"user:{id}")
            return jsonify({"message": "User updated", "username": user.username})
        else:
            return jsonify({"error": "No username provided"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    # Удаляем кеш
    cache.delete(f"user:{id}")
    return jsonify({"message": "User deleted"})

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to Flask API",
        "endpoints": ["/user", "/user/<id>", "/stub_status"]
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0')