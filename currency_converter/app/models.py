from flask       import jsonify, request
from flask.views import MethodView

from .core.manager import convert


class CurrencyAPI(MethodView):
    def get(self):
        amount          = request.args.get('amount', None)
        input_currency  = request.args.get('input_currency', None)
        output_currency = request.args.get('output_currency', None)

        if amount is None:
            return (jsonify({'message':"Missing 'amount' argument"}), 500)

        if input_currency is None:
            return (jsonify({'message':"Missing 'input_currency' argument"}), 500)

        try:
            return jsonify(convert(input_currency,
                                   output_currency,
                                   amount))
        except Exception as e:
            return str(e)
            return (jsonify({'message':"Something happened. Please contact your administrator. And thank you for fish."}), 500)
