# Pairwise Temporal Memory on Cloudflare

One repository deploys both the public site and PTM Worker API.

## Architecture

```text
Cloudflare Worker
├── Workers Assets -> site/
├── /health/live
├── /health/ready -> Hyperdrive -> PostgreSQL
└── /api/v1/status
```

## Required setup

1. Provision a PostgreSQL database and apply `db/schema.sql`.
2. Create a Cloudflare Hyperdrive configuration for that database.
3. Replace `REPLACE_WITH_HYPERDRIVE_ID` in `wrangler.jsonc`.
4. In GitHub Actions secrets, add `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`.
5. Ensure the Cloudflare Worker name is `ptm-runtime`, or change both the dashboard project name and `wrangler.jsonc` to the same value.
6. Push to `main`.

The static site lives under `site/`. API and health routes execute the Worker first. Credentials are never committed.
