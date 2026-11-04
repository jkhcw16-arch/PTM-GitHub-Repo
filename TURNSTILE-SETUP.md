# Turnstile setup

1. Create a Cloudflare Turnstile widget for the production hostname.
2. Replace `0x4AAAAAAFyoHcs4Lzw70eyO` in `wrangler.jsonc` and `site/index.html` with the public site key.
3. Store the secret through Wrangler, never in Git:

       npx wrangler secret put TURNSTILE_SECRET_KEY

4. Deploy with `npx wrangler deploy`.
5. Submit one live inquiry and confirm it is stored only after successful Turnstile verification.
