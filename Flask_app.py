import Coins_conv as cV
from flask import Flask, jsonify
import json


app = Flask(__name__)
# ---------------------------------
# select data (reals or mockup)
# ---------------------------------
values = cV.reals_val()
# values = cV.mockup_val()
# ----------------------------------
idf = values.columns.values.tolist()


@app.route('/coin/<string:coin_name>')
def get_coin(coin_name):
    coin = coin_name.upper()
    match = filter(lambda x: coin in x, idf)
    data = values[match]
    data = json.dumps(json.loads(data.to_json(orient='split')), indent=2)
    cV.webhook(data)
    if len(data) < 10:
        data = jsonify({"message": "Coin not found"})
    return data


if __name__ == '__main__':
    app.run(debug=True, port=4000)
