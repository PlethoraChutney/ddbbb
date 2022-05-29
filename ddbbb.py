from flask import Flask, render_template, request
import os
import sys
import json

app = Flask(
    __name__,
    static_folder = os.path.join('dist', 'static'),
    template_folder = 'dist'
)

try:
    app.secret_key = os.environ['SECRET_KEY']
except KeyError:
    if app.debug:
        app.logger.warning('$SECRET_KEY not in environment.')
        app.secret_key = 'BAD_SECRET_KEY_FOR_DEVELOPMENT'
    else:
        app.logger.error('Must include secret key for production mode')
        sys.exit(1)

comments = [
    {
        'author': 'Rich',
        'content': ['Hi everyone. Time for another year of riding around to celebrate my birth.']
    },
    {
        'author': 'Rich',
        'content': ['As always, there are a few rules.']
    },
    {
        'author': 'Rich',
        'content': ['You must:', 'Have fun.', 'Be nice', 'Invite anyone you think would enjoy this, and that I \'d like.']
    },
    {
        'author': 'Rich',
        'content': ['You are encouraged to:', 'Ride a bike or scooter or other person-powered vehicle (if you wanna bus or lyft or w/e go for it)', 'Come to as many or few bars as you like (don\'t feel obligated to be there all day! It\'s...a lot)', 'Drink whatever you want. It doesn\'t have to be alcohol!']
    },
    {
        'author': 'Rich',
        'content': ['You may NOT:', 'Drink and drive. If you\'re planning on having more than one beer don\'t drive!!! I don\'t care what your tolerance is!']
    }
]

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/api', methods = ['POST'])
def api():
    rj = request.get_json()
    if rj['action'] == 'get_comments':
        return json.dumps(comments), 200, {'ContentType': 'application/json'}