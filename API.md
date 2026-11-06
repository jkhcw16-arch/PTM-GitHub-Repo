# PTM API routes

- `POST /api/v1/states`
- `GET /api/v1/states/{id}?tenantId=...`
- `POST /api/v1/transitions`
- `GET /api/v1/transitions/{id}?tenantId=...`
- `POST /api/v1/transitions:compose`
- `POST /api/v1/deltas:realize`
- `POST /api/v1/realizations:invert`
- `POST /api/v1/validate`

All PostgreSQL values are parameterized. State and transition retrieval requires `tenantId`. Coordinates are canonical decimal strings; duplicates and noncanonical integers are rejected.
