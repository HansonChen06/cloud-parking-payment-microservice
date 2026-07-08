# Cloud Parking Payment Microservice

[![CI](https://github.com/HansonChen06/cloud-parking-payment-microservice/actions/workflows/ci.yml/badge.svg)](https://github.com/HansonChen06/cloud-parking-payment-microservice/actions/workflows/ci.yml)

A small backend service for creating parking sessions, tracking payment status, and looking up parking transactions. The project is designed to demonstrate backend API development, automated testing, Docker packaging, CI validation, logging, health checks, and cloud deployment readiness.

## Why this project

This mirrors the kind of production work used by parking and mobility payment platforms: a customer starts a parking session, the service stores transaction details, a payment status is updated, and operations teams need health checks, logs, and deployment automation.

## Tech stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite for local development, Postgres-compatible configuration for cloud deployments
- Pytest
- Ruff
- Docker
- GitHub Actions CI

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health and environment status |
| `POST` | `/sessions` | Create a parking session |
| `GET` | `/sessions/{session_id}` | Look up a parking session by ID |
| `GET` | `/sessions` | List sessions with optional filters |
| `PATCH` | `/sessions/{session_id}/payment` | Update payment status |

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://localhost:8000/docs
```

## Example request

```bash
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{
    "license_plate": "ABC123",
    "zone_id": "VAN-YALETOWN-01",
    "duration_minutes": 90,
    "amount_cents": 550,
    "currency": "CAD"
  }'
```

## Run tests

```bash
pytest
ruff check .
```

## Docker

```bash
docker build -t parking-payment-service .
docker run -p 8000:8000 --env-file .env parking-payment-service
```

Or use Compose:

```bash
docker compose up --build
```

## CI/CD pipeline

The GitHub Actions workflow runs on pushes and pull requests to `main`:

1. Checks out the repository.
2. Installs Python 3.11 dependencies.
3. Runs Ruff linting.
4. Runs the Pytest suite with coverage.
5. Builds the Docker image.

This models the validation step of a deployment pipeline by ensuring code quality, test coverage, and container build health before release.

## Cloud deployment plan

This service is ready to deploy to AWS using a container-based workflow:

1. Build the Docker image.
2. Push it to Amazon Elastic Container Registry.
3. Deploy to ECS Fargate or Elastic Beanstalk.
4. Configure `DATABASE_URL` to point to Amazon RDS Postgres.
5. Send container logs to CloudWatch.
6. Monitor `/health`, API latency, error rates, and payment status transitions.

See [docs/deployment.md](docs/deployment.md) for a more detailed AWS deployment checklist.

Suggested production environment variables:

```text
APP_NAME=cloud-parking-payment-microservice
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/parking
LOG_LEVEL=INFO
```

## Monitoring and reliability

- `/health` endpoint for uptime checks and load balancer health checks.
- Structured JSON logs for easier searching in CloudWatch or another log platform.
- Input validation with clear API errors.
- Automated tests for core workflows and failure cases.

See [docs/test-plan.md](docs/test-plan.md) for acceptance criteria and test coverage.

## Architecture

```text
Client / Mobile App
        |
        v
FastAPI REST API
        |
        v
SQLAlchemy Data Access Layer
        |
        v
SQLite locally / Postgres in cloud
```

## Resume bullets

- Built a cloud-ready parking payment microservice with REST APIs for parking session creation, payment status tracking, and transaction lookup using FastAPI, SQLAlchemy, and Docker.
- Implemented automated tests and a GitHub Actions CI pipeline to validate code changes, run linting, and build a container image before deployment.
- Added structured application logging and a health check endpoint to improve service reliability, observability, and debugging.
- Documented system architecture, deployment steps, API endpoints, and monitoring strategy for maintainability.
