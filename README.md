# ecommerce-cart-api

A FastAPI backend for a simple e-commerce shopping cart: products, per-session carts, and order checkout, backed by SQLAlchemy and SQLite.

## Features

- Product catalog with stock tracking
- Per-cart line items with quantity management
- Automatic cart total calculation
- Checkout endpoint that converts a cart into an order and decrements stock

## Tech Stack

Python, FastAPI, SQLAlchemy, Pydantic, SQLite

## Getting Started

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Overview

- `POST /products` - create a product
- `GET /products` - list products
- `POST /carts` - create a new cart
- `POST /carts/{cart_id}/items` - add an item to a cart
- `GET /carts/{cart_id}` - view a cart with its total
- `POST /carts/{cart_id}/checkout` - convert a cart into an order
- 
