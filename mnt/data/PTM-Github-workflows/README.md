# PTM GitHub workflows

Copy the `.github/workflows/` directory into the repository root.

- `validate-site.yml`: prevents `site/index.html` from being committed/deployed as flattened plain text and checks the PTM contact-form contract.
- `deploy-pages.yml`: validates and publishes only `./site` to GitHub Pages.
- `ptm-ci.yml`: checks required Worker/deployment files, JavaScript syntax, key bindings/routes, and frontend markup.

The workflows intentionally do not contain Cloudflare credentials or Turnstile secrets.
