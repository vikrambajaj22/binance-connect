from flask import Flask, request
from flask.templating import render_template
from dotenv import load_dotenv

from util import connect_to_binance


app = Flask(__name__)
load_dotenv()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-balances', methods=['POST'])
def get_balances():
    results = {}
    error = ''
    if request.method == 'POST':
        try:
            connect_to_binance.compute_balances()
        except Exception as e:
            error = '{}'.format(repr(e))
            return render_template('index.html', results=results, error=error)
    return render_template('index.html', results=results, error=error)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
