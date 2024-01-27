from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.serialize() for message in messages])
    elif request.method == 'POST':
        body = request.json.get('body')
        username = request.json.get('username')
        if not body or not username:
            return jsonify({'error': 'Body and username are required'}), 400
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.serialize()), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)
    if request.method == 'PATCH':
        body = request.json.get('body')
        if not body:
            return jsonify({'error': 'Body is required'}), 400
        message.body = body
        db.session.commit()
        return jsonify(message.serialize())
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted'})

if __name__ == '__main__':
    app.run(port=5555)
