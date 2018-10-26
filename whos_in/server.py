import json
from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO, emit

import whos_in.data as local_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
sio = SocketIO(app)

@sio.on('connect')
def connect():
    print("connect ", request.sid)

@sio.on('login')
def login(data):
    print("login ", request.sid)
    print(data)
    json_data = json.loads(data)
    user = local_data.session.query(local_data.User).filter(local_data.User.name==json_data['name']).first()
    if user is None:
        user = local_data.User(name=json_data['name'])
        print(user)
        local_data.session.add(user)
        local_data.session.commit()
    users = local_data.session.query(local_data.User).all()
    print(users)
    json_users = json.dumps(users, cls=local_data.AlchemyEncoder)
    print(json_users)
    emit('update', json_users, broadcast=True)

@sio.on('inout')
def inout(data):
    print("inout ", data)
    json_data = json.loads(data)
    user = local_data.session.query(local_data.User).filter(local_data.User.name==json_data['name']).first()
    user.is_in = json_data['is_in']
    local_data.session.commit()

    users = local_data.session.query(local_data.User).all()
    json_users = json.dumps(users, cls=local_data.AlchemyEncoder)
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