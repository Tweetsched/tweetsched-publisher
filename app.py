import os
import logging
from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth
from twython import Twython

logging.basicConfig(filename='tweetsched-publisher.log', level=logging.INFO)
auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_password(username):
    if username == os.environ['SERVICE_KEY']:
        return os.environ['SERVICE_PASS']
    return None

@auth.error_handler
def unauthorized():
    logging.info('Unauthorized access')
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/api/v1/tweets', methods=['POST'])
@auth.login_required
def publish_tweet():
    if not request.json or not 'profileId' or not 'message' in request.json:
        logging.info('Not valid request')
        abort(400)
    twitter = Twython(os.environ['APP_KEY'],
                      os.environ['APP_SECRET'],
                      os.environ['OAUTH_TOKEN'],
                      os.environ['OAUTH_TOKEN_SECRET'])
    try:
        twitter.update_status(status=request.json['message'])
        logging.info('Tweet was posted')
        return jsonify({'status': 'Tweet was posted'}), 200
    except TwythonError as e:
        logging.error('Tweet was not posted. Error: ' + str(e))
        return jsonify({'status': 'Tweet was not posted'}), 502

@app.errorhandler(404)
@auth.login_required
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=False)
