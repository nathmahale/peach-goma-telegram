from flask import Flask, jsonify, request, make_response, session, flash, render_template
import jwt
import datetime
from functools import wraps
import os

app = Flask(__name__)

app.config['SERVER_NAME'] = os.environ['LOCAL_SERVER']
app.config['SECRET_KEY'] = os.environ['API_KEY']
app.config['DEBUG'] = True


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return (jsonify({'message': 'Token is missing'}), 403)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return (jsonify({'message': 'Token is invalid'}), 403)

        return (f(*args, **kwargs))
    return (decorated)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Currently logged in'


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == os.environ['TEST_USER'] and request.form['password'] == os.environ['TEST_PASSWORD']:
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        },
            app.config['SECRET_KEY'])

        return (render_template('home.html'))
    else:
        return make_response('Could verify', 403, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
