# AWS Deployment Notes

This service can be deployed as a containerized API on AWS ECS Fargate or Elastic Beanstalk.

## Reference architecture

```text
Internet
   |
Application Load Balancer
   |
ECS Fargate service
   |
Amazon RDS PostgreSQL

Logs and metrics -> Amazon CloudWatch
Container image -> Amazon ECR
```

## Deployment steps

1. Build the Docker image.
2. Push the image to Amazon ECR.
3. Create an RDS PostgreSQL database.
4. Configure the service with `DATABASE_URL`.
5. Deploy the container to ECS Fargate.
6. Configure the load balancer health check path as `/health`.
7. Send container logs to CloudWatch Logs.

## Example production environment

```text
APP_NAME=cloud-parking-payment-microservice
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/parking
LOG_LEVEL=INFO
```

## Monitoring checklist

- API health check success rate.
- HTTP 4xx and 5xx response counts.
- Request latency.
- Container CPU and memory utilization.
- Database connection errors.
- Payment status transition logs.
