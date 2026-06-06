# Production-Ready REST API with FastAPI

A production-style REST API built using FastAPI that demonstrates clean backend architecture patterns including JWT authentication, dependency injection, service-repository separation, pagination, and centralized exception handling.

# Features

* JWT Authentication
* Protected Endpoints
* OAuth2 Bearer Token Flow
* Repository Pattern
* Service Layer Architecture
* Dependency Injection
* Pagination Support
* Custom Exceptions
* Global Exception Handling
* Interactive Swagger Documentation

## Architecture

```text
Client
  ↓
Route Layer
  ↓
Dependency Injection
  ↓
Service Layer
  ↓
Repository Layer
  ↓
Data Source
```

### Responsibilities

#### Route Layer

* Handles HTTP requests and responses
* Receives input from clients
* Delegates business operations to services

#### Service Layer

* Contains business logic
* Coordinates application behavior
* Raises business exceptions when required

#### Repository Layer

* Handles data access
* Retrieves and stores data
* Returns raw data without business decisions

## API Endpoints

### Authentication

#### Login

```http
POST /login
```

Returns a JWT access token.

### User

#### Get Current User

```http
GET /profile
```

Protected endpoint requiring a valid bearer token.

### Projects

#### Create Project

```http
POST /projects
```

Request:

```json
{
  "name": "Project Alpha"
}
```

#### Get All Projects

```http
GET /projects
```

Supports pagination:

```http
GET /projects?skip=0&limit=10
```

#### Get Project By ID

```http
GET /projects/{project_id}
```

Example:

```http
GET /projects/1
```

## Error Handling

Custom exceptions are converted into meaningful HTTP responses using centralized exception handlers.

Example:

```json
{
  "detail": "Project not found"
}
```

Response:

```http
404 Not Found
```

## Technologies Used

* Python
* FastAPI
* Pydantic
* JWT Authentication
* Uvicorn

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Learning Objectives

This project was built to practice:

* Clean Architecture Principles
* REST API Design
* JWT Authentication
* Dependency Injection
* Service and Repository Patterns
* Exception Handling
* Pagination
* FastAPI Development

```
```
