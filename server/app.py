from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    message_list = []
    for message in messages:
        message_list.append({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': message.updated_at.strftime('%Y-%m-%d %H:%M:%S') if message.updated_at else None
        })
    return jsonify(message_list)
    
@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': message.updated_at.strftime('%Y-%m-%d %H:%M:%S') if message.updated_at else None
    })

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({
        'id': new_message.id,
        'body': new_message.body,
        'username': new_message.username,
        'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': new_message.updated_at.strftime('%Y-%m-%d %H:%M:%S') if new_message.updated_at else None
    }), 201

# PATCH (update) a message by ID
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.json
    message.body = data['body']
    db.session.commit()
    return jsonify({
        'id': message.id,
        'body': message.body,
        'username': message.username,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': message.updated_at.strftime('%Y-%m-%d %H:%M:%S') if message.updated_at else None
    })

# DELETE a message by ID
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'})
    
if __name__ == '__main__':
    app.run(port=5555)
