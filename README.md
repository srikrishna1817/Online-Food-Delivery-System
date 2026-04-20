# QuickBite — Online Food Delivery System

A full-stack web application built as a Software Engineering academic project.  
Supports **5 user roles** with dedicated dashboards and role-based access control.

## Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript    |
| Backend  | Python 3 + Flask                   |
| Database | SQLite (via Python's `sqlite3`)    |

---

## Folder Structure

```
Online-Food-Delivery-System/
├── backend/
│   ├── app.py          ← Flask entry point & route registration
│   ├── database.py     ← SQLite connection + schema + migrations
│   ├── auth.py         ← /api/register, /api/login, /api/logout, /api/me
│   ├── menu.py         ← /api/menu  (CRUD, admin-gated writes)
│   ├── orders.py       ← /api/orders  (place, view, update status)
│   ├── delivery.py     ← /api/delivery  (agent pickup + status updates)
│   ├── admin.py        ← /api/admin/orders, /api/admin/users
│   └── food_delivery.db  ← SQLite DB (auto-created on first run)
│
├── frontend/
│   ├── index.html              ← Login / Register landing page
│   ├── css/style.css           ← Shared design system
│   ├── js/api.js               ← Shared fetch helper + utilities
│   ├── customer/
│   │   ├── dashboard.html      ← Browse menu, search, add to cart, place order
│   │   └── orders.html         ← View order history + live status tracker
│   ├── restaurant/
│   │   └── dashboard.html      ← Accept / Reject / Prepare orders + stats
│   ├── delivery/
│   │   └── dashboard.html      ← Pick up orders + proof-of-delivery upload
│   ├── admin/
│   │   └── dashboard.html      ← System-wide orders + users + revenue
│   └── inventory/
│       └── dashboard.html      ← Stock levels + low-stock alerts
│
├── sample_data.py      ← Seeds DB with 5 demo users + 12 menu items
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- `pip` package manager

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the database with sample data

```bash
python sample_data.py
```

This creates **5 demo user accounts** (one per role) and **12 food menu items**.

### 4. Start the server

```bash
python backend/app.py
```

### 5. Open the app

Navigate to **http://localhost:5000** in your browser.

---

## Demo Login Credentials

All demo accounts use the password: **`password123`**

| Role              | Email                     | What they can do                                              |
|-------------------|---------------------------|---------------------------------------------------------------|
| Customer          | `customer@demo.com`       | Search menu, filter by category/veg, add to cart, place & track orders |
| Restaurant Staff  | `restaurant@demo.com`     | Accept/reject/prepare orders, view order stats                |
| Delivery Agent    | `delivery@demo.com`       | Pick up orders, upload proof-of-delivery photo, mark delivered |
| Admin             | `admin@demo.com`          | View all orders, all users, total revenue                     |
| Inventory Manager | `inventory@demo.com`      | Monitor stock levels, respond to low-stock alerts, update quantities |

---

## Features by Role

### 🛒 Customer
- Real-time **search bar** — filter menu items by name
- **Category filter tabs** — Burgers, Pizza, Biryani, Drinks, etc.
- **Pure Veg toggle** — show only vegetarian items
- **Cart sidebar** — slide-out cart with item quantities and subtotals
- Inline **`− qty +` controls** on menu cards after adding an item
- **Order progress tracker** — visual step-by-step status: Placed → Accepted → Preparing → Out for Delivery → Delivered

### 🍳 Restaurant Staff
- **Pending orders** highlighted separately for immediate action
- Per-order **Accept / Reject / Start Preparing** buttons
- **Stats row** — live counts of Total, Pending, Accepted, Delivered orders
- Auto-refresh every **30 seconds**

### 🛵 Delivery Agent
- **Available Pickups** tab — orders ready for collection
- **My Deliveries** tab — orders currently assigned
- **Proof-of-delivery photo upload** before marking an order delivered
- Auto-switches to My Deliveries tab on pickup

### 📦 Inventory Manager
- **Stock table** — all menu items with current stock quantities
- **Stat cards** — Total Items, Sufficient Stock, Low Stock Alerts, Out of Stock
- **Orange alert banner** — lists all items below the low-stock threshold (< 10 units)
- **Inline update** — set new stock quantity per item and save instantly

### ⚙️ Admin
- System-wide **orders table** with customer, items, total, status, and agent
- **Users table** — all registered users with roles
- **Total revenue** from delivered orders

### 🔐 Login / Register
- **Show/hide password** — eye icon toggle on both Sign In and Register fields
- Role-based **automatic redirect** to the correct dashboard after login
- Inline success and error messages

---

## API Reference

### Authentication

| Method | Endpoint        | Description                     |
|--------|-----------------|---------------------------------|
| POST   | `/api/register` | Create a new user account       |
| POST   | `/api/login`    | Log in (returns a session)      |
| POST   | `/api/logout`   | Log out (clears session)        |
| GET    | `/api/me`       | Get current logged-in user info |

**Allowed roles:** `customer` | `restaurant` | `delivery` | `admin` | `inventory`

**Register body:**
```json
{ "name": "Alice", "email": "alice@example.com", "password": "secret", "role": "customer" }
```

---

### Menu

| Method | Endpoint         | Auth       | Description              |
|--------|------------------|------------|--------------------------|
| GET    | `/api/menu`      | Public     | List all available items |
| POST   | `/api/menu`      | Admin only | Add a menu item          |
| PUT    | `/api/menu/<id>` | Admin only | Update a menu item       |
| DELETE | `/api/menu/<id>` | Admin only | Delete a menu item       |

---

### Orders

| Method | Endpoint                   | Auth                      | Description               |
|--------|----------------------------|---------------------------|---------------------------|
| POST   | `/api/orders`              | Customer                  | Place a new order         |
| GET    | `/api/orders`              | Customer                  | Get own orders            |
| GET    | `/api/orders/all`          | Restaurant, Admin         | Get all orders            |
| PUT    | `/api/orders/<id>/status`  | Restaurant / Delivery / Admin | Update order status   |

**Place order body:**
```json
{ "items": [{ "menu_item_id": 1, "quantity": 2 }, { "menu_item_id": 5, "quantity": 1 }] }
```

---

### Delivery

| Method | Endpoint                    | Auth     | Description                               |
|--------|-----------------------------|----------|-------------------------------------------|
| GET    | `/api/delivery/available`   | Delivery | Orders accepted but no agent assigned     |
| GET    | `/api/delivery/assigned`    | Delivery | Orders assigned to this agent             |
| PUT    | `/api/delivery/<id>/status` | Delivery | Update: "Out for Delivery" or "Delivered" |

---

### Admin

| Method | Endpoint            | Auth  | Description                    |
|--------|---------------------|-------|--------------------------------|
| GET    | `/api/admin/orders` | Admin | All orders with full details   |
| GET    | `/api/admin/users`  | Admin | All users (passwords excluded) |

---

## Order Status Lifecycle

```
Customer places order
        │
        ▼
    [ Placed ]
        │
    Restaurant
   ┌────┴────┐
   ▼         ▼
[Accepted] [Rejected]
   │
   ▼
[Preparing]
   │
Delivery Agent picks up
   │
   ▼
[Out for Delivery]
   │
   ▼
[Delivered]
```

---

## SE Design Notes

- **Modular structure** — each concern (auth, menu, orders, delivery, admin) is a separate Flask Blueprint
- **Role-based access control** — every API endpoint checks the session role before responding
- **Passwords** — stored as SHA-256 hex digests, never plain-text
- **Price integrity** — order totals calculated server-side to prevent client tampering
- **Single-origin deployment** — Flask serves both API and frontend, no CORS needed
- **Database migrations** — `migrate_db()` and `migrate_users_role()` safely patch existing DBs on startup without data loss
- **Session** — server-side Flask sessions (signed cookie), stateless clients
- **SQLite FK enforcement** — `PRAGMA foreign_keys = ON` on every connection