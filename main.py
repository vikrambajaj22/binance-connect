from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask.templating import render_template

from util import connect_to_binance, send_email

app = Flask(__name__)
load_dotenv()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/notify')
def notify():
    try:
        results = connect_to_binance.compute_balances()
        for ticker in results['assets']:
            if ticker != 'USD':
                current_price, average_purchase_price = results['assets'][ticker][
                    'current_price'], results['assets'][ticker]['average_purchase_price']
                if current_price >= average_purchase_price:
                    send_email.send(ticker, '''<p>Current {} price {} is greater than or equal to the average purchase price {}</p>
                    <p><a href="http://binance-connect-22.ue.r.appspot.com/">Binance-Connect</a></p>
                    <p><a href="https://www.binance.us/en/home">Binance US</a></p>'''.format(
                        ticker, current_price, average_purchase_price))
        return 'success'
    except Exception as e:
        return 'an exception occurred: {}'.format(repr(e))


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
    app.run(port=8080, host='0.0.0.0', debug=True)
