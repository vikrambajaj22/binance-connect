import atexit
import google.appengine.api

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.templating import render_template
from google.appengine.api.mail import SendMail

from apscheduler.schedulers.background import BackgroundScheduler
from util import connect_to_binance

app = Flask(__name__)
app.wsgi_app = google.appengine.api.wrap_wsgi_app(app.wsgi_app)
load_dotenv()


def notify():
    print('sending notification')
    SendMail(sender='vikrambajaj220496@gmail.com', to='vikrambajaj@nyu.edu',
             subject="Binance_Connect Notification", body="Test",
             make_sync_call=google.appengine.api.apiproxy_stub_map.MakeSyncCall)


scheduler = BackgroundScheduler()
scheduler.add_job(func=notify, trigger="interval", seconds=60)
scheduler.start()

# shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/get-balances', methods=['POST'])
def get_balances():
    results = {}
    error = ''
    if request.method == 'POST':
        try:
            results = connect_to_binance.compute_balances()
            return jsonify(results)
        except Exception as e:
            error = 'an exception occurred: {}'.format(repr(e))
            print(error)
            return jsonify({'error': error})


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
