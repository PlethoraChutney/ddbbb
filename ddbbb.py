from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import datetime
import pytz
import os
import sys
import json
import couchdb

pacific = pytz.timezone('US/Pacific')

class Database:
    def __init__(self) -> None:
        host = os.environ['COUCHDB_HOST']
        username = os.environ['COUCHDB_USERNAME']
        password = os.environ['COUCHDB_PASSWORD']
        self.server = couchdb.Server(f'http://{username}:{password}@{host}:5984')

        if 'ddbbb_comments' in self.server:
            self.comments_db = self.server['ddbbb_comments']
        else:
            self.comments_db = self.server.create('ddbbb_comments')

    @property
    def comments(self) -> list:
        comment_list = self.comments_db.get('comments')

        if comment_list is not None:
            return comment_list['comments']
        else:
            return []

    def new_comment(self, comment : dict) -> None:
        comment['timestamp'] =  datetime.datetime.now(tz = pacific).strftime("%Y/%m/%d, %H:%M:%S:%f")

        
        comment_list = self.comments_db['comments']
        comment_list['comments'].append(comment)
        self.comments_db['comments'] = comment_list

    def delete_comment(self, comment: dict) -> None:
        comment_list = self.comments_db['comments']
        print(comment_list['comments'])
        comment_list['comments'].remove(comment)
        self.comments_db['comments'] = comment_list

app = Flask(
    __name__,
    static_folder = os.path.join('dist', 'static'),
    template_folder = 'dist'
)

comment_db = Database()

try:
    app.secret_key = os.environ['SECRET_KEY']
except KeyError:
    if app.debug:
        app.logger.warning('$SECRET_KEY not in environment.')
        app.secret_key = 'BAD_SECRET_KEY_FOR_DEVELOPMENT'
    else:
        app.logger.error('Must include secret key for production mode')
        sys.exit(1)

socketio = SocketIO(app)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/api', methods = ['POST'])
def api():
    rj = request.get_json()
    if rj['action'] == 'get_comments':
        return json.dumps(comment_db.comments), 200, {'ContentType': 'application/json'}

    elif rj['action'] == 'new_comment':
        comment_db.new_comment(rj['comment'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    elif rj['action'] == 'delete_comment':
        comment_db.delete_comment(rj['comment'])
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@socketio.on('connect')
def connect():
    emit('write_to_log', {'data': 'New user connected!'})

@socketio.on('newComment')
def new_comment(json):
    comment_db.new_comment(json)
    emit('new_comment', json, broadcast = True)

@socketio.on('deleteComment')
def delete_comment(json):
    print('Deleting comment\n\n')
    print(json)
    comment_db.delete_comment(json)
    emit('delete_comment', json, broadcast = True)

if __name__ == '__main__':
    socketio.run(app)
