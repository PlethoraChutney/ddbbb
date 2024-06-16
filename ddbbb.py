#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room
import datetime
import pytz
import os
import sys
import json
import couchdb
import re

pacific = pytz.timezone('US/Pacific')
ddbbb_year = os.environ['DDBBB_YEAR']

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
        comment_list = self.comments_db['comments']

        if comment_list is None:
            comment_list = {ddbbb_year: []}
            self.comments_db['comments'] = comment_list
        elif ddbbb_year not in comment_list:
            comment_list[ddbbb_year] = {}
            self.comments_db['comments'] = comment_list

        return comment_list
    
    def get_comments(self, year) -> list:
        return list(self.comments[year].values())
    

    def new_comment(self, data : dict) -> None:
        comment = data['comment']
        year = data['year']
        timestamp = datetime.datetime.now(tz = pacific).strftime("%Y/%m/%d, %H:%M:%S:%f")

        comment['timestamp'] = timestamp
        comment['parsed_timestamp'] = datetime.datetime.now(tz = pacific).strftime('%b %-d at %-I:%M %p')
        
        comment_list = self.comments_db['comments']
        comment_list[year][timestamp] = comment
        self.comments_db['comments'] = comment_list

    def delete_comment(self, data: dict) -> None:
        timestamp = data["comment"]['timestamp']
        year = data['year']

        comment_list = self.comments_db['comments']
        del comment_list[year][timestamp]
        self.comments_db['comments'] = comment_list

    @property
    def years_available(self) -> list:
        keys = self.comments_db['comments'].keys()
        return [key for key in keys if re.match(r'[0-9]{4}', key)]

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
    return redirect(url_for('year', year = ddbbb_year))

@app.route('/<year>/', methods = ['GET'], endpoint = 'year')
def year_index(year):
    if not os.path.exists(os.path.join('ddbbb_years', f"{year}.json")):
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route('/api', methods = ['POST'])
def api():
    rj = request.get_json()
    if rj['action'] == 'get_year_info':
        with open(os.path.join('ddbbb_years', f"{rj['year']}.json")) as f:
            year_info = json.load(f)
        return json.dumps(year_info), 200, {'ContentType': 'application/json'}
    elif rj['action'] == 'get_comments':
        return (
            json.dumps(comment_db.get_comments(rj['year'])),
            200,
            {'ContentType': 'application/json'}
        )

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
def new_comment(comment_info):
    comment_db.new_comment(comment_info)
    emit('new_comment', comment_info, broadcast = True)

@socketio.on('deleteComment')
def delete_comment(comment_info):
    comment_db.delete_comment(comment_info)
    emit('delete_comment', comment_info, broadcast = True)

if __name__ == '__main__':
    socketio.run(app, port=44444)
