from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    print(cf, final_amount)
    response = {'fulfillmentText': "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)}
    print(response)
    return jsonify(response)


def fetch_conversion_factor(source_currency, target_currency):
    url = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_fapPjtJIgrRBWM9GYhlqytGbiq0GF7PXLYtyerJb&currencies={}&base_currency={}".format(
        target_currency, source_currency)
    response = requests.get(url)
    response = response.json()
    print(response)

    return response['data'][target_currency]


if __name__ == '__main__':
    app.run(debug=True)
