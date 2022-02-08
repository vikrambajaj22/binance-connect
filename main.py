import atexit

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.templating import render_template

from apscheduler.schedulers.background import BackgroundScheduler
from util import connect_to_binance

app = Flask(__name__)
load_dotenv()


def notify():
    print('not sending notification')


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
    # cron job runs twice if debug=True
    app.run(debug=False, port=8080, host='0.0.0.0')
