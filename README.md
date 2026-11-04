# PTM GitHub Pages deployment workflow

Copy `.github/workflows/deploy-pages.yml` into the PTM repository.

The workflow publishes only `site/` to GitHub Pages. It intentionally does not publish the repository root, Worker source, D1 configuration, authorization policy, OAuth fixtures, tests, or other project artifacts.

In the repository's GitHub Pages settings, set the publishing source to **GitHub Actions**.

Important: GitHub Pages is the static frontend only. PTM server-side routes such as `/api/contact`, D1 access, Turnstile Siteverify, and future `/api/v1/*` Worker APIs must remain hosted by the server-side backend. If the static Pages frontend calls that backend from another origin, configure the backend URL and cross-origin policy deliberately.
