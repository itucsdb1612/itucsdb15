import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/authors',methods=['GET', 'POST'])
def authors_page():
    return render_template('authors.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    return render_template('profile.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
