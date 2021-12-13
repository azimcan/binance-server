#!flask/bin/python
from flask import jsonify, make_response
from flask import Flask, request

from app.controllers import SymbolsController as sc

app = Flask(__name__)


@app.route('/binance/api/getSymbols', methods=['GET'])
def get_symbols():
  return sc.GetSymbols()

@app.route('/binance/api/getSymbol/<string:symbol>', methods=['GET'])
def get_symbol(symbol):
  return sc.GetSymbol(symbol)

@app.route('/binance/api/setSymbol/<string:symbol>', methods=['GET'])
def set_symbol(symbol):
  return sc.SetSymbol(symbol)

# @app.route('/binance/api/setSymbol', methods=['POST'])
# def set_symbol(symbol):
#   return sc.SetSymbol(request.json['symbol'])

@app.route('/binance/api/setSymbols', methods=['GET'])
def set_symbols():
  return sc.SetSymbols()


@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)
 