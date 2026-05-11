# Netflix-Style Cloud Lab

A runnable cloud/SRE portfolio project that demonstrates a small streaming-style backend with:

- FastAPI backend
- PostgreSQL database
- Redis caching
- Docker + Docker Compose
- Static frontend served by Nginx
- Health checks, catalog APIs, watch events, and simple analytics

This is intentionally simple enough to fully understand and explain in interviews, but structured so it can later be extended with Terraform, Kubernetes, CI/CD, monitoring, and AWS deployment.

## Architecture

```text
Browser
  ↓
Frontend container / Nginx
  ↓
FastAPI backend
  ↓              ↓
PostgreSQL      Redis cache
```

## What this project proves

You can explain this as:

> I built a streaming-style backend where the frontend calls a FastAPI service for movie catalog data. The backend stores metadata in PostgreSQL and uses Redis to cache frequently requested catalog queries. The system is containerized with Docker Compose so the frontend, API, database, and cache can run as separate services locally. I also added health checks and basic watch-event analytics to show operational thinking.

## Requirements

- Docker Desktop or Docker Engine
- Git

## Run locally

```bash
git clone <your-repo-url>
cd netflix-cloud-lab
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Seed the database

In a second terminal:

```bash
docker compose exec api python seed.py
```

Then refresh the frontend.

## Main API endpoints

```http
GET /health
GET /movies
GET /movies?genre=Action
GET /movies?search=cloud
GET /movies/{movie_id}
POST /movies
POST /watch-events
GET /analytics/top-movies
```

## Example POST /movies

```bash
curl -X POST http://localhost:8000/movies \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Scaling Season",
    "genre": "Documentary",
    "description": "A documentary about scaling cloud systems under heavy traffic.",
    "release_year": 2026,
    "rating": 8.4,
    "thumbnail_url": "https://picsum.photos/seed/scaling/500/300",
    "video_url": "https://example.com/videos/scaling-season.mp4"
  }'
```

## Example watch event

```bash
curl -X POST http://localhost:8000/watch-events \
  -H "Content-Type: application/json" \
  -d '{
    "movie_id": 1,
    "user_id": "demo-user",
    "seconds_watched": 245
  }'
```

## How caching works

The `/movies` endpoint checks Redis first. If the query result is cached, it returns the cached result and sets:

```http
X-Cache: HIT
```

If Redis does not have the result, the API queries PostgreSQL, stores the result in Redis, and sets:

```http
X-Cache: MISS
```

Test it:

```bash
curl -i http://localhost:8000/movies
curl -i http://localhost:8000/movies
```

The second request should return `X-Cache: HIT`.

## Interview talking points

Use this project to talk about:

- Containerized multi-service architecture
- API/database/cache separation
- Redis caching for lower database load
- Health checks for operational visibility
- Docker Compose for repeatable local environments
- PostgreSQL for persistent relational metadata
- Watch events as a foundation for async analytics later

## Next upgrades

Good next steps:

1. Add GitHub Actions to run tests and build Docker images.
2. Add Prometheus + Grafana for API metrics.
3. Deploy the backend to AWS ECS or Kubernetes/k3s.
4. Add Terraform for AWS VPC, ECS, RDS, ElastiCache, and ALB.
5. Add SQS-style async processing for watch events.

## Troubleshooting

### Port already in use

Change the ports in `docker-compose.yml`, for example:

```yaml
ports:
  - "8001:8000"
```

### Reset database

```bash
docker compose down -v
docker compose up --build
```

Then seed again:

```bash
docker compose exec api python seed.py
```
