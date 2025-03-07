import threading
import random

max_tickers = 1024

buy_orders = [[] for i in range(max_tickers)]
sell_orders = [[] for i in range(max_tickers)]
buy_lock = threading.Lock()
sell_lock = threading.Lock()

def binary_search_insert_position(orders, price):
    low, high = 0, len(orders)
    while low < high:
        mid = (low + high) // 2
        if orders[mid][1] < price:
            low = mid + 1
        else:
            high = mid
    return low

def addOrder(buying: bool, ticker: int, quantity: int, price: int):  # true = buying, ticker 0-1023, price is in cents
    order = (quantity, price)
    if buying:
        with buy_lock:
            index = binary_search_insert_position(buy_orders[ticker], price)
            buy_orders[ticker].insert(index, order)
    else:
        with sell_lock:
            index = binary_search_insert_position(sell_orders[ticker], price)
            sell_orders[ticker].insert(index, order)

def randomOrder():
    buying = random.choice([True, False])
    ticker = random.randint(0, max_tickers - 1)
    quantity = random.randint(1, 100)
    price = random.randint(1, 100000)
    addOrder(buying, ticker, quantity, price)

def matchOrder(ticker: int):  #attempts to match the cheapest sell order with a buy order for the given ticker.
    with buy_lock:
        with sell_lock:
            if len(buy_orders[ticker]) and len(sell_orders[ticker]):
                for k in range(len(buy_orders[ticker])):
                    buy_order = buy_orders[ticker][k]
                    buy_quantity, buy_price = buy_order
                    if buy_price >= sell_orders[ticker][0][1]:
                        if buy_quantity >= sell_orders[ticker][0][0]:
                            buy_quantity -= sell_orders[ticker][0][0]
                            buy_orders[ticker][0] = (buy_quantity, buy_price)
                            sell_orders[ticker].pop(0)
                        else:
                            sell_orders[ticker][0] = (sell_orders[ticker][0][0] - buy_quantity, sell_orders[ticker][0][1])
                            buy_orders[ticker].pop(k)
                        break

            
def displayOrderStatus():
    for i in range(max_tickers):
        print(f"Ticker {i}:")
        print("Buy Orders:")
        for buy_order in buy_orders[i]:
            print(buy_order)
        print("Sell Orders:")
        for sell_order in sell_orders[i]:
            print(sell_order)
        print()

def simpleTest():
    for k in range(20000):
        randomOrder()

    displayOrderStatus()

    for i in range(max_tickers):
        print(f"Matching orders for ticker {i}")
        matchOrder(i)
        
    displayOrderStatus()

simpleTest()