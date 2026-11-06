# Cloudflare CI gates

Local preflight:

```bash
npm ci
npm run ci:validate
```

`ci:validate` performs the non-secret predeployment gates: unresolved-placeholder scan, Wrangler binding type generation, TypeScript checking, a Wrangler dry-run bundle, and a scan of that bundle for obvious placeholder/credential strings.

Production deployment is manual through the deployment workflow and reruns `ci:validate` before deployment.

Real OIDC token issuance, Hyperdrive connectivity, PostgreSQL integration, and deployed HTTP smoke tests require environment-specific endpoints/credentials and should be gated separately after those production values are configured.
