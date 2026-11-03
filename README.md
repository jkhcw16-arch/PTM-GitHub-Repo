# Pairwise Temporal Memory (PTM) - 1.3.0 Candidate

Candidate repository bundle for PTM ontology additions, SHACL validation, algebraic round-trip testing, CI, security policy, and the static workflow-marketing site.

## Layout
- `ontology/` - OWL/RDF Turtle additions and SHACL shapes
- `tests/` - Python algebra and SHACL regression tests
- `.github/workflows/ptm-ci.yml` - CI workflow
- `site/` - static Cloudflare Pages site
- `SECURITY.md` - vulnerability reporting and severity policy
- `CONTRIBUTING.md` - contributor policy
- `LICENSE` - proprietary all-rights-reserved notice

## Test commands
From the repository root:

    python -m pip install -r requirements-test.txt
    python tests/test_ptm_roundtrip.py
    python tests/test_ptm_shacl.py

## License
Copyright (c) 2026 Jamie Kinney. All rights reserved. This repository is not distributed under an open-source license. See `LICENSE`.
