# Authenticated API access

Public routes:

- `GET /health/live`
- `GET /health/ready`
- `GET /api/v1/status`

Every other `/api/v1/*` route requires an RS256 Bearer JWT. Validation checks signature, `exp`, optional `nbf`, issuer, audience, subject context, tenant claim, and scopes.

Required configuration variables:

- `OIDC_ISSUER`
- `OIDC_AUDIENCE`
- `OIDC_JWKS_URL`

Accepted tenant claims: `tenant_id` or `tid`. The requested tenant must equal the authenticated tenant.

Scopes:

- `ptm:states:read`, `ptm:states:write`
- `ptm:transitions:read`, `ptm:transitions:write`, `ptm:transitions:compose`
- `ptm:realize`, `ptm:invert`, `ptm:validate`
- `ptm:*` grants all PTM scopes

Example header:

```text
Authorization: Bearer <OIDC access token>
```
