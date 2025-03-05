
import threading
import random
import time
import queue

class Order:
    #stock order
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # 'BUY' or 'SELL'
        self.ticker = ticker
        self.quantity = quantity
        self.price = price

class OrderBook:
    #Managing Buy & Sell orders using priorityQueues
    def __init__(self):
        self.buy_orders = queue.PriorityQueue()  # Max-Heap for descending buy order
        self.sell_orders = queue.PriorityQueue()  # Min-Heap for ascending sell order

    def add_order(self, order_type, ticker, quantity, price):
        #Adds a new Buy/Sell order
        new_order = Order(order_type, ticker, quantity, price)

        if order_type == "BUY":
            self.buy_orders.put((-price, new_order))  # Negate price for max-heap
        else:
            self.sell_orders.put((price, new_order))

    def match_orders(self):
        #Matching Buy & Sell orders
        while not self.buy_orders.empty() and not self.sell_orders.empty():
            _, buy_order = self.buy_orders.get()  # Get highest buy price
            sell_price, sell_order = self.sell_orders.get()  # Get lowest sell price

            if -buy_order.price >= sell_price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                print(f"Trade Executed: {trade_quantity} shares of {buy_order.ticker} at ${sell_price}")

                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity

                if buy_order.quantity > 0:
                    self.buy_orders.put((-buy_order.price, buy_order))  # Put back remaining buy order

                if sell_order.quantity > 0:
                    self.sell_orders.put((sell_order.price, sell_order))  # Put back remaining sell order
            else:
                # If no match, put back orders and break
                self.buy_orders.put((-buy_order.price, buy_order))
                self.sell_orders.put((sell_order.price, sell_order))
                break

class StockExchange:
    #Handles multiple stock order books with threading
    def __init__(self):
        self.order_books = {
            "AAPL": OrderBook(),
            "GOOGL": OrderBook(),
            "TSLA": OrderBook()
        }

    def add_order(self, order_type, ticker, quantity, price):
        #Adds an order to the order book
        if ticker in self.order_books:
            self.order_books[ticker].add_order(order_type, ticker, quantity, price)

    def match_orders(self):
        #Runs matching in multiple threads
        threads = []
        for book in self.order_books.values():
            thread = threading.Thread(target=book.match_orders)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

# Creating a simulation for stock transactions from multiple brokers
def simulate_trading(exchange, num_orders=10):
    #Simulates multiple brokers adding orders
    tickers = ["AAPL", "GOOGL", "TSLA"]
    order_types = ["BUY", "SELL"]

    for _ in range(num_orders):
        order_type = random.choice(order_types)
        ticker = random.choice(tickers)
        quantity = random.randint(1, 50)
        price = round(random.uniform(100, 500), 2)

        exchange.add_order(order_type, ticker, quantity, price)
        print(f"Added Order: {order_type} {quantity} shares of {ticker} at ${price}")

        time.sleep(random.uniform(0.1, 0.3))  # simulating real-time trading

if __name__ == "__main__":
    exchange = StockExchange()

    # Start trading simulation in a separate thread
    trader_thread = threading.Thread(target=simulate_trading, args=(exchange, 20))  # Limit to 20 orders
    trader_thread.start()

    # Start matching orders
    while trader_thread.is_alive():
        exchange.match_orders()
        time.sleep(1)  # Match orders every second