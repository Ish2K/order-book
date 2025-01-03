const baseURL = "http://localhost:8000";

// Place Order
document.getElementById("place-order-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const side = parseInt(document.getElementById("side").value);
  const price = parseFloat(document.getElementById("price").value);
  const quantity = parseFloat(document.getElementById("quantity").value);

  const params = new URLSearchParams({ side, price, quantity });
  const response = await fetch(`${baseURL}/orders/place`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString(),
  });

  const result = await response.json();
  document.getElementById("place-order-result").textContent = JSON.stringify(result);
});

// Modify Order
document.getElementById("modify-order-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const order_id = document.getElementById("order-id-modify").value;
  const updated_price = parseFloat(document.getElementById("updated-price").value);

  const params = new URLSearchParams({ order_id, updated_price });
  const response = await fetch(`${baseURL}/orders/modify`, {
    method: "PUT",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString(),
  });

  const result = await response.json();
  document.getElementById("modify-order-result").textContent = JSON.stringify(result);
});

// Cancel Order
document.getElementById("cancel-order-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const orderId = document.getElementById("order-id-cancel").value;

  const params = new URLSearchParams({ order_id: orderId });
  const response = await fetch(`${baseURL}/orders/cancel`, {
    method: "DELETE",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString(),
  });

  const result = await response.json();
  document.getElementById("cancel-order-result").textContent = JSON.stringify(result);
});

// Fetch Order Info
document.getElementById("fetch-order-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const orderId = document.getElementById("order-id-fetch").value;

  const response = await fetch(`${baseURL}/orders/fetch_order?order_id=${orderId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  const result = await response.json();
  document.getElementById("fetch-order-result").textContent = JSON.stringify(result);
});

// Fetch All Orders
document.getElementById("fetch-all-orders-btn").addEventListener("click", async () => {
  const response = await fetch(`${baseURL}/orders/fetch_all_orders`);
  const result = await response.json();
  const tbody = document.getElementById("all-orders-table").querySelector("tbody");

  tbody.innerHTML = "";
  result.forEach((order) => {
    var status = "Alive";
    if(order.remaining_quantity === 0) {
      status= "Filled";
    }
    else if(order.is_alive === false && order.remaining_quantity > 0) {
      status = "Cancelled";
    }
    const row = `<tr>
      <td>${order.order_id}</td>
      <td>${order.side}</td>
      <td>${order.price}</td>
      <td>${order.quantity}</td>
      <td>${order.traded_quantity}</td>
      <td>${order.average_traded_price}</td>
      <td>${order.remaining_quantity}</td>
      <td>${status}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
});

// WebSocket for Trades
const tradesSocket = new WebSocket("ws://localhost:8000/ws/trades");
tradesSocket.onmessage = (event) => {
  
  const tradeData = JSON.parse(event.data); // Assuming the trade data is JSON
  // console.log(tradeData);
  // Clear current trade data
  document.getElementById("trades-table-body").innerHTML = "";

  // Populate Trade Data

  tradeData.forEach((trade) => {
    trade = JSON.parse(trade);
    const row = `<tr>
      <td>${trade.execution_timestamp}</td>
      <td>${trade.trade_id}</td>
      <td>${trade.price}</td>
      <td>${trade.quantity}</td>
      <td>${trade.bid_order_id}</td>
      <td>${trade.ask_order_id}</td>
    </tr>`;
    document.getElementById("trades-table-body").innerHTML += row;
  });
};

// WebSocket for Order Book
const orderBookSocket = new WebSocket("ws://localhost:8000/ws/orderbook");
orderBookSocket.onmessage = (event) => {
  
  // console.log(event.data);
  const orderBookData = JSON.parse(JSON.parse(event.data)); // Assuming the order book data is in JSON format
  // console.log(orderBookData);
  
  // Clear current order book data
  document.getElementById("bid-table-body").innerHTML = "";
  document.getElementById("ask-table-body").innerHTML = "";

  if(Array.isArray(orderBookData.bid) && Array.isArray(orderBookData.ask)) {
    // console.log("Both Bid and Ask are arrays");
  }

  orderBookData.bid.forEach((order) => {
    // console.log(order.price, order.quantity);
    }
  );
  orderBookData.ask.forEach((order) => {
    // console.log(order.price, order.quantity);
    }
  );
  // Populate Bid Orders
  orderBookData.bid.forEach((order) => {
    const row = `<tr>
      <td>${order.order_id}</td>
      <td>${order.price}</td>
      <td>${order.quantity}</td>
    </tr>`;
    document.getElementById("bid-table-body").innerHTML += row;
  });

  // Populate Ask Orders
  orderBookData.ask.forEach((order) => {
    const row = `<tr>
      <td>${order.order_id}</td>
      <td>${order.price}</td>
      <td>${order.quantity}</td>
    </tr>`;
    document.getElementById("ask-table-body").innerHTML += row;
  });
};

// Reset Session
document.getElementById("reset-session-btn").addEventListener("click", async () => {
  await fetch(`${baseURL}/orders/reset`, { method: "POST" });
  alert("Session Reset Successfully");
});
