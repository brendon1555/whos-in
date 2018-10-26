import json
from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whos_in.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
sio = SocketIO(app)

@sio.on('connect')
def connect():
    print("connect ", request.sid)

@sio.on('login')
def login(data):
    from whos_in.data import User, users_schema
    print("login ", request.sid)
    print(data)
    json_data = json.loads(data)
    user = db.session.query(User).filter(User.name==json_data['name']).first()
    if user is None:
        user = User(name=json_data['name'])
        print(user)
        db.session.add(user)
        db.session.commit()
    users = db.session.query(User).all()
    print(users)
    json_users = users_schema.dump(users).data
    print(json_users)
    emit('update', json_users, broadcast=True)

@sio.on('inout')
def inout(data):
    from whos_in.data import User, users_schema
    print("inout ", data)
    json_data = json.loads(data)
    user = db.session.query(User).filter(User.name==json_data['name']).first()
    user.is_in = json_data['is_in']
    db.session.commit()

    users = db.session.query(User).all()
    json_users = users_schema.dump(users).data
    emit('update', json_users, broadcast=True)

@sio.on('disconnect')
def disconnect():
    print('disconnect ', request.sid)

@app.route('/')
def index():
    return render_template('index.html')

with app.test_request_context():
    url_for('static', filename='scripts.js')
    url_for('static', filename='socket.io.js')

if __name__ == '__main__':
    sio.run(
        app, 
        debug=True, 
        use_reloader=True,
        host='0.0.0.0'
    )