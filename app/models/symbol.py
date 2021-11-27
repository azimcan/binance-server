from binance import Client
from binance.helpers import round_step_size

import pandas as pd
from numpy import average

symbols_file = 'data/symbols.csv'
orders_file = 'data/orders.csv'

api_json = pd.read_json("data/api.json", orient="index")

api_key = api_json[0]["api_key"]
api_secret = api_json[0]["api_secret"]

client = Client(api_key, api_secret)

class Symbol:
  def __init__(self, symbol = ''):
    self.symbol = symbol
    self.currency_pair = ''
    self.average_buy = 0
    self.average_sell = 0
    self.executed_buy = 0
    self.executed_sell = 0
    self.net_executed = 0
    self.profit = 0
    self.global_average = 0
    self.commission = 0
    self.tick_size = 0
    self.step_size = 0


  def find(self, symbol = None):
    data = pd.read_csv(symbols_file)

    for index, row in data.iterrows():
      if(row['symbol'] == symbol):
        self.symbol = row['symbol']
        self.currency_pair = row['currency_pair']
        self.average_buy = row['average_buy']
        self.average_sell = row['average_sell']
        self.executed_buy = row['executed_buy']
        self.executed_sell = row['executed_sell']
        self.net_executed = row['net_executed']
        self.profit = row['profit']
        self.global_average = row['global_average']
        self.commission = row['commission']
        self.tick_size = row['tick_size']
        self.step_size = row['step_size']
        break
    return self.to_dict()

  def buy(self, price, quantity):
    rounded_price = round_step_size(price, self.tick_size)
    rounded_quantity = round_step_size(quantity, self.step_size)

    order = client.order_limit_buy(
      symbol = self.currency_pair,
      price = rounded_price,
      quantity = rounded_quantity)

    self.save_order(order)
    return order

  def sell(self, price, quantity):
    print(self.symbol)
    rounded_price = round_step_size(price, self.tick_size)
    rounded_quantity = round_step_size(quantity, self.step_size)


    order = client.order_limit_sell(
      symbol = self.currency_pair,
      price = rounded_price,
      quantity = rounded_quantity)
    self.save_order(order)

    return order

  def save(self):
    self.Calculate()
    a = self.to_dict()
    data = pd.read_csv(symbols_file)
    data = data.merge(pd.DataFrame(a), how='outer')
    data.to_csv(symbols_file, index=False)
    return a

  def to_dict(self):
    return [{
      'symbol': self.symbol,
      'currency_pair': self.currency_pair,
      'average_buy': self.average_buy,
      'average_sell': self.average_sell,
      'executed_buy': self.executed_buy,
      'executed_sell': self.executed_sell,
      'net_executed': self.net_executed,
      'profit': self.profit,
      'global_average': self.global_average,
      'commission': self.commission,
      'tick_size': self.tick_size,
      'step_size': self.step_size
    }]

  def save_order(self, order):
    try:
      data = pd.read_csv(orders_file)
      orders = data.to_dict(orient='records')
    except Exception:
      orders = []

    orders.append(order)
    pd.DataFrame(orders).to_csv(orders_file, index=False)

  def Calculate(self):
    self.currency_pair = self.symbol + 'USDT'

    trades_df = pd.DataFrame(client.get_my_trades(symbol=self.currency_pair))
    symbol_info = client.get_symbol_info(symbol=self.currency_pair)

    self.tick_size = float(symbol_info['filters'][0]['tickSize'])
    self.step_size = float(symbol_info['filters'][2]['stepSize'])

    if(trades_df.size != 0):
      trades_df = trades_df[trades_df['time'] >= 1633972308381]

      trades_df['price'] = trades_df['price'].astype(float)
      trades_df['qty'] = trades_df['qty'].astype(float)
      trades_df['quoteQty'] = trades_df['quoteQty'].astype(float)
      trades_df['commission'] = trades_df['commission'].astype(float)


      try:
        self.average_buy = round_step_size(average(trades_df[trades_df['isBuyer'] == True]['price'], weights=trades_df[trades_df['isBuyer'] == True]['qty']), self.tick_size)
      except:
        self.average_buy = 0.0
      self.executed_buy = round_step_size(trades_df[trades_df['isBuyer'] == True]['qty'].sum(), self.step_size)


      try:
        self.average_sell = round_step_size(average(trades_df[trades_df['isBuyer'] == False]['price'], weights=trades_df[trades_df['isBuyer'] == False]['qty']), self.tick_size)
      except:
        self.average_sell = 0.0
      self.executed_sell = round_step_size(trades_df[trades_df['isBuyer'] == False]['qty'].sum(), self.step_size)


      self.profit = round_step_size(self.average_sell*self.executed_sell - self.average_buy*self.executed_buy, self.tick_size)

      self.net_executed = round_step_size(self.executed_buy - self.executed_sell, self.step_size)

      if(self.profit < 0 and self.net_executed > 0):
        self.global_average = round_step_size(abs(self.profit) / self.net_executed, self.tick_size)
      else:
        self.global_average = 0

      self.commission = trades_df['commission'].sum()

    return self.to_dict()


