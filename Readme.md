# Task Management Backend API

> A production-grade backend system built with **FastAPI**, **PostgreSQL**, **Redis**, **Docker**, and **GitHub Actions**, demonstrating modern backend engineering practices including layered architecture, asynchronous programming, automated testing, containerization, continuous integration, caching, and event-driven communication.



# Why This Project?

This project was built to move beyond a traditional CRUD application and explore how **production backend systems** are engineered.

Instead of focusing only on API development, the project demonstrates software engineering practices commonly used in real-world backend services:

- Layered (Clean) Architecture
- Repository & Service Pattern
- Dependency Injection
- JWT Authentication
- Redis Caching
- Redis Rate Limiting
- Event-Driven Communication
- Automated Testing
- Dockerized Development
- Continuous Integration
- Container Image Publishing

The goal is to build software that is **maintainable, testable, scalable, and production-oriented**.

---

# Architecture

![Architecture Diagram](images/clean-architecture-api-readme.png)

---

# Engineering Highlights

- Async-first FastAPI application
- PostgreSQL with SQLAlchemy 2.0 Async ORM
- Redis Cache-Aside Pattern
- Redis Pub/Sub Event System
- Redis-based Fixed Window Rate Limiting
- Repository & Service Layer Architecture
- Dependency Injection
- JWT Authentication
- Docker Multi-Container Deployment
- GitHub Actions Continuous Integration
- GitHub Container Registry (GHCR) Image Publishing
- Automated API, Integration and Service Tests
- Alembic Database Migrations

---

# Technology Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python 3.12 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 (Async) |
| Cache | Redis |
| Messaging | Redis Pub/Sub |
| Authentication | JWT + OAuth2 |
| Testing | Pytest, HTTPX, pytest-asyncio |
| Database Migration | Alembic |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions |
| Registry | GitHub Container Registry (GHCR) |

---

# Features

## Authentication & Security

- JWT Authentication
- OAuth2 Password Bearer
- Protected API Endpoints
- User Profile Endpoint
- Redis Rate Limiting
- HTTP 429 Protection

---

## User Management

- Create User
- Get User
- List Users
- Redis Cache-Aside Pattern
- Cache Invalidation
- Configurable Cache TTL

---

## Project Management

- Create Project
- Get Project
- List Projects
- User-Project Relationships

---

## Task Management

- Create Task
- Get Task
- List Tasks
- User-Task Relationships
- Project-Task Relationships

---

## Event-Driven Communication

Task creation automatically publishes an event using Redis Pub/Sub.

A dedicated background worker asynchronously consumes the event, demonstrating decoupled service communication.

---

# System Architecture

```text
                        Client
                           │
                           ▼
                    FastAPI Application
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 Authentication       Service Layer        Redis
        │                  │                  │
        ▼                  ▼                  │
 Repository Layer     Business Logic         │
        │                                     │
        ▼                                     ▼
 PostgreSQL                        Cache • Rate Limit • Pub/Sub
                                              │
                                              ▼
                                   Notification Worker
```

---

# Clean Architecture

The application follows a layered architecture where each layer has a single responsibility.

```text
                HTTP Request
                     │
                     ▼
                 API Router
                     │
                     ▼
               Service Layer
                     │
                     ▼
            Repository Layer
                     │
                     ▼
                PostgreSQL
```

### Responsibilities

| Layer | Responsibility |
|--------|----------------|
| Router | Request validation & routing |
| Service | Business logic |
| Repository | Database access |
| Database | Data persistence |

This separation improves maintainability, testing, and scalability.

---

# Request Lifecycle

A typical request flows through the application as follows:

```text
Client
   │
   ▼
FastAPI Router
   │
Dependency Injection
   │
   ▼
Service Layer
   │
Business Rules
   │
   ▼
Repository
   │
SQLAlchemy
   │
   ▼
PostgreSQL
```

This design keeps HTTP logic separate from business logic and database operations.

---

# Redis Architecture

Redis is used for three independent responsibilities.

## 1. Cache-Aside Pattern

```text
Client Request
      │
      ▼
 Redis Cache
  │        │
Hit      Miss
 │         │
 ▼         ▼
Return   PostgreSQL
             │
             ▼
      Store in Cache
```

Benefits:

- Faster response times
- Reduced database load
- Improved scalability

---

## 2. Fixed Window Rate Limiting

```text
Incoming Request
        │
        ▼
Redis Counter (INCR)
        │
        ▼
Limit Reached?
   │          │
 No         Yes
 │            │
 ▼            ▼
Allow     HTTP 429
```

Implemented using Redis atomic operations:

- INCR
- EXPIRE
- TTL

---

## 3. Event-Driven Messaging

Whenever a task is created:

```text
Task Created
      │
      ▼
Publisher
      │
      ▼
 Redis Channel
      │
      ▼
Notification Worker
```

This enables asynchronous communication between independent services.

---

# Project Structure

```text
project/
│
├── alembic/
├── tests/
│
├── auth.py
├── config.py
├── database.py
├── main.py
├── models.py
├── schemas.py
│
├── user_repository.py
├── project_repository.py
├── task_repository.py
│
├── user_service.py
├── project_service.py
├── task_service.py
│
├── publisher.py
├── subscriber.py
├── redis_client.py
├── rate_limiter.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Design Principles

This project emphasizes production-oriented engineering principles rather than simply implementing REST endpoints.

- Separation of Concerns
- Single Responsibility Principle
- Dependency Injection
- Repository Pattern
- Service Layer Architecture
- Async-First Programming
- Environment-Based Configuration
- Containerized Development
- Automated Quality Checks
- Scalable System Design

---

# Testing Strategy

Quality is enforced through automated testing at multiple levels to validate business logic, API behavior, and database interactions.

## Test Stack

| Tool | Purpose |
|------|---------|
| Pytest | Test framework |
| pytest-asyncio | Async test support |
| HTTPX AsyncClient | API integration testing |
| unittest.mock | Service mocking |
| PostgreSQL Test Database | Isolated integration tests |

---

## Current Test Coverage

- User API endpoints
- User repository
- Task service business logic
- Dependency injection overrides
- Async database sessions
- HTTP request lifecycle

---

## Test Architecture

```text
              Pytest
                 │
                 ▼
        HTTPX AsyncClient
                 │
                 ▼
          FastAPI Application
                 │
      Dependency Overrides
                 │
                 ▼
      PostgreSQL Test Database
```

Run the test suite:

```bash
pytest -v
```

---

# Continuous Integration (CI)

The project includes an automated GitHub Actions workflow that validates every change before it reaches the `main` branch.

## CI Pipeline

```text
Developer
    │
    ▼
Pull Request
    │
    ▼
GitHub Actions
    │
    ├── Install Dependencies
    ├── Ruff
    ├── Ruff Formatter
    ├── Black
    ├── Pytest
    ├── Docker Build
    └── Publish Image (main only)
```

### CI Features

- Automatic dependency installation
- Code quality checks
- Formatting verification
- Automated testing
- Docker image build validation
- GitHub Container Registry publishing
- Pull Request validation

---

# Containerization

The application is fully containerized using Docker and orchestrated with Docker Compose.

## Services

| Service | Description |
|----------|-------------|
| FastAPI API | REST API |
| PostgreSQL | Primary database |
| Redis | Cache, rate limiter, messaging |
| Notification Worker | Background event consumer |

---

## Docker Architecture

```text
                Docker Compose
                       │
     ┌─────────────────┼─────────────────┐
     │                 │                 │
     ▼                 ▼                 ▼
 FastAPI API      PostgreSQL         Redis
     │                                   │
     └──────────────► Worker ◄───────────┘
```

---

# GitHub Container Registry (GHCR)

Every successful push to the `main` branch automatically builds a Docker image and publishes it to GitHub Container Registry.

Image tags include:

- `latest`
- Commit SHA
- Semantic version (`v1.0.0`, etc.)

This mirrors the workflow used in modern production environments.

---

# API Overview

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/login` | Generate JWT token |
| GET | `/profile` | Authenticated profile |

---

## Users

| Method | Endpoint |
|--------|----------|
| POST | `/users` |
| GET | `/users` |
| GET | `/users/{id}` |

---

## Projects

| Method | Endpoint |
|--------|----------|
| POST | `/projects` |
| GET | `/projects` |
| GET | `/projects/{id}` |

---

## Tasks

| Method | Endpoint |
|--------|----------|
| POST | `/tasks` |
| GET | `/tasks` |
| GET | `/tasks/{id}` |

Task creation automatically publishes a Redis Pub/Sub event consumed by the notification worker.

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/<your-username>/fastapi-rest-api.git

cd fastapi-rest-api
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn main:app --reload
```

Open:

```
http://localhost:8000/docs
```

or

```
http://localhost:8000/redoc
```

---

# Running with Docker

Build and start all services:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

---

# Database Migrations

Generate a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/task_manager

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=task_manager

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Engineering Practices Demonstrated

This project focuses on engineering practices commonly found in production backend systems.

- Async Programming
- Layered (Clean) Architecture
- Repository Pattern
- Service Layer
- Dependency Injection
- Environment-Based Configuration
- JWT Authentication
- OAuth2 Security
- Redis Cache-Aside Pattern
- Cache Invalidation
- Fixed Window Rate Limiting
- Event-Driven Architecture
- Background Workers
- Docker Multi-Container Deployment
- GitHub Actions CI
- GitHub Container Registry
- Automated Testing
- Database Migrations

---

# What I Learned

This project provided hands-on experience with:

- Designing asynchronous backend systems
- Building maintainable application architecture
- Managing relational databases
- Implementing secure authentication
- Applying caching strategies
- Building event-driven services
- Writing automated tests
- Creating Dockerized applications
- Designing CI pipelines
- Publishing container images
- Working with production-oriented development workflows

---

# Roadmap

## Completed

- Async FastAPI Backend
- PostgreSQL Integration
- SQLAlchemy Async ORM
- JWT Authentication
- Redis Caching
- Redis Rate Limiting
- Redis Pub/Sub
- Repository Pattern
- Service Layer
- Dependency Injection
- Docker & Docker Compose
- Automated Testing
- GitHub Actions CI
- GitHub Container Registry (GHCR)

---

## In Progress

- Monitoring & Observability
- Structured Logging

---

## Planned

- Celery & Distributed Task Queue
- Redis Streams
- OpenTelemetry Tracing
- Prometheus Metrics
- Grafana Dashboards
- VPS Deployment
- Reverse Proxy (Nginx)
- HTTPS with Let's Encrypt
- Kubernetes Deployment
- Cloud Deployment (AWS / Azure / GCP)

---

# Contributing

Contributions, suggestions, and improvements are welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Submit a Pull Request.

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

This project was built as part of a journey to learn production-grade backend engineering by implementing real-world software engineering practices rather than focusing solely on CRUD functionality.

It continues to evolve with additional capabilities such as observability, distributed task processing, deployment automation, and cloud-native infrastructure.

If you found this repository useful, consider giving it a ⭐.