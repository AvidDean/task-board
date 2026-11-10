Phase 5 changes: CORS enabled, configurable frontend API base, backend-only Compose.
Local Docker test: docker build -t local-backend:dev backend && IMAGE_BASE=local IMAGE_TAG=dev docker compose up -d
Check: curl http://localhost/api/health
Stop: IMAGE_BASE=local IMAGE_TAG=dev docker compose down
Note: S3 static website requires a publicly reachable API endpoint; private EC2 is not directly reachable.
