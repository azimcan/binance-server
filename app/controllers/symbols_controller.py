from flask import jsonify

from app.models import Symbol

symbols = ['BNB', 'BTC', 'ETH', 'AAVE', 'RUNE',
           'COMP', 'NEO', 'DOGE', 'ETC', 'BAND', 
           'MATIC',  'SRM', 'BAL', 'QTUM', 'DOT',
           'XRP',  'FTT', 'AVAX', 'STRAX', 'ADA',
           'MANA', 'SLP', 'IDEX', 'WAN', 'XTZ',
           'ENJ', 'FTM', 'MASK', 'QTUM', 'DOT']


class SymbolsController():
  def GetSymbols():
    parities = []
    sym = Symbol()
    for symbol in symbols:
      parities.append(sym.find(symbol)[0])
    return jsonify(parities)

  def GetSymbol(symbol):
    if len(symbol) == 0:
      return jsonify({'symbol': 'Not found'}), 404
    
    sym = Symbol()    
    return jsonify(sym.find(symbol = symbol)[0])

  def SetSymbol(symbol):
    sym = Symbol(symbol)
    if sym.save():
      return jsonify({"status": True})

  def SetSymbols():
    parities = []
    for symbol in symbols:
      sym = Symbol(symbol)
      parities.append(sym.save())
    return jsonify(parities)

  def SellSymbol(symbol, price, quantity):
    sym = Symbol()
    sym.GetSymbol(symbol) 
    return sym.sell(price, quantity)
  '''    
  def half_sell(self):
      symbols = self.GetSymbols()
      
      for symbol in symbols:'''
            