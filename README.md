# Limit Order Book

## Overview

This repository contains a Limit Order Book built using **FastAPI**, with **MongoDB** as the database and **Docker** to containerize the application. The application handles order management, trade processing, and provides real-time updates via WebSocket communication. It is designed in a **microservices architecture** to ensure modularity, scalability, and maintainability.

### Key Components
1. **Order Service**: Manages order placement, modification, and cancellation. It communicates with the order book and updates MongoDB with order details.
2. **Trade Service**: Handles the fetching of all trades
3. **Snapshot Service**: Generates and serves snapshots of the current order book and the trade history.
4. **WebSocket Service**: Provides real-time updates on order and trade status over WebSocket connections.

### Functionalities:
- **Order Management**: Place, modify, and cancel orders.
- **Trade Matching**: Match buy and sell orders, execute trades, and commit them to the database.
- **Real-Time Updates**: Communicate order and trade data via WebSocket.
- **Data Snapshots**: Generate real-time snapshots of the order book (top 5 bids and asks)

## Architecture

The application is broken down into microservices, each of which is responsible for a specific set of operations. Each service operates independently and communicates with other services through APIs.

### Microservices Breakdown:
1. **Order Microservice** (`/orders`): 
   - Responsible for accepting, modifying, and canceling orders.
   - Interfaces with MongoDB to store and retrieve orders.
   - It triggers the matching service to check if the orders can be matched.
  
2. **Trade Microservice** (`/trades`):
   - Helps in fetching the trade history

3. **Snapshot Microservice** (`/snapshots`):
   - Provides snapshots of the current state of the order book and trade history.
   - It fetches the current state of the order book and recent trades from MongoDB.

4. **WebSocket Microservice** (`/ws`):
   - Provides real-time updates of order status, trade execution, and order book updates through WebSocket communication.

## Design Decisions

1. **Microservices Architecture**:
   - The system is designed using microservices to allow for better scalability, easier maintenance, and isolation of functionality.
   - Each service is independent, allowing for asynchronous processing where possible, and efficient data flow through REST APIs and WebSockets.
   
2. **FastAPI**:
   - FastAPI is chosen for its high performance and ease of use in building REST APIs. It supports asynchronous programming, which is crucial for handling I/O-bound operations like order and trade matching.
   
3. **MongoDB**:
   - MongoDB is used for its flexible schema and scalability. Orders, trades, and snapshots are stored as documents, making it easy to query and update the system in real time.
   
4. **WebSockets**:
   - WebSockets are used for real-time communication, allowing the system to push updates to connected clients without the need for constant polling.

5. **Docker**:
   - Docker is used to containerize the application, making it easier to deploy and scale. Each microservice runs in its own container, and the database is also containerized to maintain consistency across environments.

## Data Flow

1. **Order Placement**:
   - A user places an order via the `/orders` endpoint.
   - The order is added to MongoDB.
   - The system checks if the order can be matched with existing orders in the order book.
   - If a match is found, a trade is executed, and both orders are updated.

2. **Trade Execution**:
   - When a match is found, a trade is executed, and a new `Trade` document is created in MongoDB.
   - The matched orders are updated with the traded quantity and price.

3. **Order Book Snapshot**:
   - Users can fetch the current order book using the `/snapshots` endpoint. This will return the top 5 bids and asks, sorted by price.

4. **Real-Time Updates**:
   - WebSockets push updates to the client regarding order status, trades, and order book changes.

## Running the Application with Docker

### 1. **Clone the Repository**
```bash
git clone <repository_url>
cd <repository_directory>
```
