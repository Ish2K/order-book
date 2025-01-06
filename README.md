# Limit Order Book

## Overview

This repository implements a **Limit Order Book** using **FastAPI**, with **MongoDB** as the database and **Docker** to containerize the application. It efficiently handles order management, trade execution, and real-time updates via **WebSocket communication**. Built on a **microservices architecture**, the system is modular, scalable, and maintainable.

---

## Key Components

1. **Order Service**: Manages order placement, modification, and cancellation, updates MongoDB with order details, and interfaces with the matching engine.
2. **Trade Service**: Handles trade execution and fetching of trade history.
3. **Snapshot Service**: Generates and serves snapshots of the current order book and trade history.
4. **WebSocket Service**: Streams real-time updates of orders, trades, and order book changes.

---

## Features

- **Order Management**: Place, modify, and cancel orders.
- **Trade Matching**: Match buy and sell orders, execute trades, and update the database.
- **Real-Time Updates**: Provide instant feedback on order and trade status using WebSockets.
- **Order Book Snapshots**: Fetch real-time snapshots of the top 5 bids and asks.

---

## Architecture

The application is divided into microservices, each with a dedicated responsibility, enabling independent operation and inter-service communication via REST APIs and WebSockets.

### Microservices Breakdown

| Service            | Endpoint                  | Description                                                                                  |
|--------------------|--------------------------|----------------------------------------------------------------------------------------------|
| **Order**          | `/orders`                | Handles order placement (`/place`), modification (`/modify`), and cancellation (`/cancel`).  |
| **Trade**          | `/trades`                | Fetches trade history.                                                                       |
| **Snapshot**       | `/orders/order_book_snapshot` | Provides the current order book snapshot.                                 |
| **WebSocket**      | `/ws`                    | Streams real-time updates:                                                                  |
|                    |                          | - `/ws/orderbook`: Top 5 bid-ask orders.                                                    |
|                    |                          | - `/ws/trades`: Realtime trade events.                                                      |
| **Reset Session**  | `/orders/reset`          | Resets the database and starts a fresh order book session.                                   |

---

### URLs for Interaction

- **Swagger UI**: `http://localhost:8000/docs`
- **Landing Page**: `http://localhost:8000/`
- **Base API URL**: `http://localhost:8000`
- **WebSocket URL**: `ws://localhost:8000/ws`

---

## Design Decisions

1. **Microservices Architecture**: 
   - Ensures modularity, scalability, and ease of maintenance.
   - Supports independent operation and asynchronous processing for efficiency.
   
2. **FastAPI**:
   - High-performance framework for building REST APIs with support for asynchronous operations.
   
3. **MongoDB**:
   - Flexible and scalable NoSQL database for storing orders, trades, and snapshots.
   
4. **WebSockets**:
   - Used for real-time communication, reducing client polling overhead.
   
5. **Docker**:
   - Containerizes the application for consistent deployment across environments.

---

## Data Flow

1. **Order Placement**:
   - Users place orders via `/orders`.
   - Orders are stored in MongoDB and matched with existing orders in the book.
   - If matched, a trade is executed and updates are made to both orders.

2. **Trade Execution**:
   - Matches trigger trade creation in MongoDB.
   - The order book is updated with the trade details.

3. **Order Book Snapshots**:
   - The `/orders/order_book_snapshot` endpoint provides real-time snapshots of the top 5 bids and asks.

4. **Real-Time Updates**:
   - WebSocket services stream updates for order status, trade events, and order book changes.

---

## Running the Application with Docker

### 1. **Clone the Repository**
```bash
git clone https://github.com/Ish2K/order-book.git
cd order-book
```
### 2. **Run Docker Command**
```bash
docker-compose up --build
```

### 3. **Interact with Frontend**

  - Access the application at `localhost:8000`
  - Interact with each section based on the pdf provided

### 4. **Shut down the application**
  
  - Use `docker-compose down` to delete every service

## Possible improvements

Although each service is working fine, here are few additional steps that we can take to make
this project better

### 1. **Better matching algorithm**
  - As of now, we using sequential matching using queues. Maybe heaps or priority queue are a better data structure to match orders. It may require some thought on how to implement that

### 2. **Better Frontend**
  - More user friendly frontend would be nice, maybe we can use react to make frontend better.

### 3. **Adding Test Cases**
  - We could use Pytest to check each endpoint's functionality and add that process in github workflow.
  This will help greatly in collaborative project development. 

### 4. **Refering to Deliverables point 5**
  - The app state is backed up in mongoDB, we can make multiple db instances to store the current state (by scaling).
    Currently, if the application stops and the docker containers are not deleted, the app would start from
    the last saved state

