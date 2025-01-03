document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("order-form");
  const responseDiv = document.getElementById("response");

  const baseURL = "http://localhost:8000";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const quantity = document.getElementById("quantity").value;
    const price = document.getElementById("price").value;
    const side = document.getElementById("side").value;

    // Validate inputs (optional)
    if (quantity <= 0 || price <= 0) {
      responseDiv.textContent = "Quantity and price must be greater than zero.";
      return;
    }

    // Prepare the data
    const orderData = new URLSearchParams({
      side: side,
      price: price,
      quantity: quantity,
    });

    console.log("Sending payload:", orderData.toString()); // Log payload to console

    try {
      // Send POST request to /orders/place endpoint
      const response = await fetch(`${baseURL}/orders/place`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded", // Form data encoding
        },
        body: orderData.toString(), // Send form data
      });

      if (response.ok) {
        const result = await response.json();
        responseDiv.textContent = `Order placed successfully! Order ID: ${result.order_id}`;
      } else {
        const error = await response.json();
        responseDiv.textContent = `Error: ${error.detail}`;
      }
    } catch (error) {
      responseDiv.textContent = `Request failed: ${error.message}`;
    }
  });
});
