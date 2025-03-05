# Stock Trading Engine

### Overview
This is a stock trading engine solution that matches Buy and Sell orders for multiple stocks. It supports **multi-threading** and uses queue.PriorityQueue() to handle concurrent order processing.
---
### 1. Adding Orders
- Orders are stored in **priority queues** (PriorityQueue) for efficient access.
  - **Buy orders** are stored in a **max-heap** (highest price first).
  - **Sell orders** are stored in a **min-heap** (lowest price first).

### 2. Matching Orders
- The match_orders function continuously checks if the highest Buy price is greater than or equal to the lowest Sell price.
- If a match is found, a trade is executed, and quantities are updated.
- If an order is partially filled, the remaining quantity is added back to the queue.
- If no match is found, unmatched orders remain in the system.

### 3. Multi-Threading
- Each stock has its own **OrderBook**, and multiple threads process order matching simultaneously.
- PriorityQueue is thread-safe, so no explicit locks are required.

--- 

- **For testing**, the program runs for a **finite time** (20 orders) and doesn't hang.  
- In a **real-world system**, we would continuously check for new incoming orders instead.

---

1. **Run the script** (`python trading_engine.py`).

