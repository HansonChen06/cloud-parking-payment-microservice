# Test Plan

## Acceptance criteria

- A customer can create a parking session with a valid license plate, parking zone, duration, and payment amount.
- A customer or support agent can retrieve a parking session by ID.
- A support workflow can filter sessions by license plate or zone.
- A payment processor workflow can update the payment status.
- Invalid inputs return clear validation errors.
- Missing sessions return `404 Not Found`.
- The service exposes a health check for deployment monitoring.

## Automated coverage

- `GET /health` returns service status.
- `POST /sessions` creates an active session with pending payment.
- `GET /sessions/{session_id}` retrieves an existing session.
- `GET /sessions?license_plate=...` filters transaction lookup results.
- `PATCH /sessions/{session_id}/payment` updates payment status.
- Missing sessions return `404`.
- Invalid duration returns `422`.

## Manual smoke test

```bash
uvicorn app.main:app --reload
curl http://localhost:8000/health
```
