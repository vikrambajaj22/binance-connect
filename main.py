from flask import Flask, request, jsonify
from flask.templating import render_template
from dotenv import load_dotenv

from util import connect_to_binance


app = Flask(__name__)
load_dotenv()


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
