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

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [message.to_dict() for message in messages]
    return make_response(jsonify(messages_list), 200)
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    try:
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return make_response(new_message.to_dict(), 201)
    except Exception as e:
        return make_response({"error": str(e)}, 400)
@app.route('/messages/<int:id>', methods=['PATCH'])
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555)
