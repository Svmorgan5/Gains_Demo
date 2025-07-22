# Gains Intermediate Demo

## Overview

Gains Intermediate Demo is a containerized Flask web application for managing gyms, members, subscriptions, and payments. It features a RESTful API, a static HTML dashboard, Swagger API documentation, and automated testing with pytest. The project is fully Dockerized for easy deployment and development.

---

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy, Marshmallow, Flask-Limiter, Flask-Caching
- **Database:** MySQL (via Docker Compose)
- **API Docs:** Swagger UI (`flask-swagger-ui`)
- **Frontend:** Static HTML/CSS/JavaScript
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest, pytest-flask
- **CI/CD:** GitHub Actions

---

## Features

- **Gym & Member Management:** Register gyms and members, login, update profiles, and manage accounts.
- **Subscriptions:** Create, update, and cancel gym subscriptions for members.
- **Payments:** Record and view payments for subscriptions, gyms, and members.
- **Swagger API Docs:** Interactive API documentation available at `/api/docs`.
- **Static Dashboard:** Frontend dashboard served from `/static/index.html` and `/static/gym-dashboard.html`.
- **Automated Testing:** Pytest-based tests for endpoints and app health.
- **Dockerized:** Runs reliably anywhere with Docker and Docker Compose.

---

## Project Structure

```
Gains Intermediate Demo/
├── backend/
│   ├── __init__.py
│   ├── models.py
│   ├── extensions.py
│   ├── blueprints/
│   │   ├── gyms/
│   │   ├── members/
│   │   ├── gymSubscriptions/
│   │   └── payment/
│   ├── static/
│   │   ├── index.html
│   │   └── gym-dashboard.html
├── config.py
├── flask_app.py
├── requirements.txt
├── swagger.yaml
├── Dockerfile
├── docker-compose.yaml
├── tests/
│   └── test_basic.py
└── .github/
    └── workflows/
        └── main.yml
```

---

**Before running Docker Compose, it is recommended to test your API routes locally using Postman.**  
All routes in the provided `postman_collection.json` were tested against the local server at [http://127.0.0.1:5000](http://127.0.0.1:5000).

To do this:

1. Set up your environment:
```sh
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python flask_app.py
    
2. Use Postman to send requests to `http://127.0.0.1:5000` as shown in the collection.
```
**Testing locally first ensures all endpoints work as expected before deploying with Docker Compose.**

## Setup & Usage

### 1. **Clone the Repository**
```sh
git clone https://github.com/Svmorgan5/Gains_Demo.git
cd Gains Intermediate Demo
```

### 2. **Docker Compose**
Build and run the app and MySQL database:
```
docker-compose up --build
```
- App runs at [http://localhost:5000](http://localhost:5000)
- Swagger UI at [http://localhost:5000/api/docs](http://localhost:5000/api/docs)
- Static dashboard at [http://localhost:5000/static/index.html](http://localhost:5000/static/index.html)

### 3. **Manual Python Setup (optional)**
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python flask_app.py
```

### 4. **Testing**
Run all tests with:
```sh
pytest
```

---

## API Documentation

- **Swagger/OpenAPI Spec:** [`swagger.yaml`](swagger.yaml)
- **Swagger UI:** [http://localhost:5000/api/docs](http://localhost:5000/api/docs)

---

## Key Endpoints

- `POST /gyms/` — Register a gym
- `POST /gyms/login` — Gym login
- `POST /members/` — Register a member
- `POST /members/login` — Member login
- `GET /subscriptions/gym` — List gym subscriptions
- `GET /payments/gym` — List gym payments
- `POST /payments/subscription/<subscription_id>` — Record a payment
- See [`swagger.yaml`](swagger.yaml) for full details.

---

## Development & CI

- **Hot reload:** Code changes reflected in Docker container via volume mounts.
- **CI/CD:** GitHub Actions workflow in `.github/workflows/main.yml` builds, tests, and deploys the app.
- **Testing:** Pytest with Flask fixtures for endpoint and integration tests.

---

## Contributing

1. Fork the repo and clone locally.
2. Create a feature branch.
3. Commit your changes and push.
4. Open a pull request.

---


## Credits

Built with Flask, SQLAlchemy, Marshmallow, Docker, Pytest, Swagger UI, and
