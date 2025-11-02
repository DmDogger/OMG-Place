<p align="center">
	<img width="200px" src="https://img.shields.io/badge/OMG!Place-E--commerce%20API-blue?style=for-the-badge"/>
</p>

# 🛒 OMG!Place: E-commerce API Backend

A FastAPI-based project to explore and implement **Service Layer Architecture** and **Role-Based Access Control (RBAC)** in an e-commerce context.

## About this project

OMG!Place is an asynchronous, multi-role e-commerce backend service designed for high performance and architectural clarity. The codebase is structured using the **Service Layer pattern** to separate API routing from core business logic.
## 🚀 Key Architectural Features

This project utilizes modern Python development patterns to ensure reliability and scalability:

* **Clean Architecture (Service Layer):** Core business logic (e.g., handling reviews, product validation) is strictly separated into a **Service Layer**, keeping API routers thin and focused on HTTP concerns.
* **Asynchronous Stack:** Built on **FastAPI** and **Async SQLAlchemy (PostgreSQL)** for non-blocking database operations, maximizing API throughput and minimizing latency.
* **Data Integrity & Soft Delete:** Implements non-destructive deletion using the `is_active` flag across main models (products, categories, reviews) to preserve historical data and referential integrity.

## 🛡️ Business Logic & Security

* **Role-Based Access Control (RBAC):** Access to management endpoints (creating/deleting products) is restricted based on user roles (`seller`, `admin`) enforced by specialized dependency injections.
* **Automated Rating Engine:** Product ratings are dynamically updated: the average `rating` field is automatically recalculated and "pushed" to the product record immediately following any creation or deletion of a review.
* **Authentication Flow:** Uses standard JWT implementation with token expiration and dedicated dependencies for secure credential validation.
## 🧱 Tech Stack

| Category | Component | Detail |
| :--- | :--- | :--- |
| **Backend** | **FastAPI** | High-performance ASGI framework |
| **Database** | **PostgreSQL** | Primary database (Async mode) |
| **ORM** | **SQLAlchemy 2.0+** | Modern Async ORM features |
| **Tooling** | **Alembic** | Database migrations |
| **Auth** | **PyJWT / Bcrypt** | JSON Web Tokens for authentication |
| **Standards** | **Pydantic** | Data validation (schemas and DTOs) |

## 🚀 Setup & Installation

### 1. Prerequisites

* Python 3.10+
* PostgreSQL running (or SQLite for development)

### 2. Configuration

* Create a `.env` file in the root directory.

| Variable | Example Value | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@host:port/dbname` | Async PostgreSQL connection string. |
| `SECRET_KEY` | `strong_secret_key_for_jwt` | Secret key for signing JWTs. |

### 3. Installation Steps

1.  **Clone the repository** and navigate to the project directory.
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Apply database migrations:**
    ```bash
    alembic upgrade head
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

### 4. API Documentation

The interactive documentation will be available upon launch:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`
