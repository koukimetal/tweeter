from flask import Flask, request
from jinja2 import Environment, PackageLoader
from twitter import *
import os

app = Flask(__name__)
env = Environment(autoescape=True, loader=PackageLoader('webapp', 'templates'))

APP_KEY = os.environ['APP_KEY']
APP_SECRET = os.environ['APP_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']
SCREEN_NAME = os.environ['SCREEN_NAME']

twitter = Twitter(
    auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, APP_KEY, APP_SECRET))


@app.route('/', methods=['GET'])
def page():
    template = env.get_template('home.html')
    return template.render()


@app.route('/', methods=['POST'])
def tweet():
    contents = request.form['contents']
    action = request.form['action']

    if action == 'tweet':
        twitter.statuses.update(status=contents)
    elif action == 'reply':
        res = twitter.statuses.user_timeline(screen_name=SCREEN_NAME, count=1)
        id = res[0].get('id')
        twitter.statuses.update(status="@" + SCREEN_NAME + ' ' + contents, in_reply_to_status_id=id)

    template = env.get_template('home.html')
    return template.render(action=action, contents=contents)

if __name__ == '__main__':
    app.run('0.0.0.0')
