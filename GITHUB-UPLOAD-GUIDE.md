# GitHub Upload Guide - Pairwise Temporal Memory

This guide uploads the prepared PTM repository bundle to a GitHub repository while preserving the `.github/workflows` directory required for CI.

## 1. Extract the bundle

Extract `PTM-GitHub-Repo.zip`. The directory you upload is the contents of `PTM-GitHub-Repo/`, not the ZIP file itself.

Before publishing, review `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and the repository contents for confidential information, credentials, tokens, private keys, unpublished patent-sensitive material, or third-party restricted content.

## 2. Create the destination repository

Create a new empty repository on GitHub. For the simplest first push, do not initialize the remote with a README, license, or `.gitignore`, because those files already exist or are intentionally controlled by this bundle.

Choose repository visibility deliberately. The PTM bundle carries an all-rights-reserved proprietary notice; repository visibility and licensing are separate decisions.

## 3. Upload with Git

Open a terminal in the extracted `PTM-GitHub-Repo` directory and run:

    git init -b main
    git add .
    git status
    git commit -m "Initial PTM 1.3.0 candidate repository"
    git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
    git push -u origin main

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with the actual GitHub account and repository name.

Before `git commit`, inspect `git status` and verify that the intended files are staged and that no credentials or private material are present.

## 4. Verify the repository structure

After the push, verify that GitHub displays these paths:

    .github/workflows/ptm-ci.yml
    ontology/ptm-1.3.0-additions.ttl
    ontology/ptm-1.3.0-additions.shacl.ttl
    tests/test_ptm_roundtrip.py
    tests/test_ptm_shacl.py
    site/index.html
    site/_headers
    LICENSE
    CONTRIBUTING.md
    SECURITY.md
    README.md
    requirements-test.txt

The `.github/workflows/ptm-ci.yml` file must retain the leading `.github` directory. Do not move the workflow to the repository root.

## 5. Verify GitHub Actions

Open the repository's Actions area and inspect the PTM workflow run triggered by the push. The workflow is configured to parse the Turtle artifacts and run the algebraic and SHACL test suites across its configured Python matrix.

Review each matrix job and confirm that required test steps pass. If a test fails, inspect the corresponding workflow log instead of treating the repository as release-conformant.

## 6. Review uploaded test artifacts

The workflow is configured to upload the two generated test result files as workflow artifacts even when a preceding test step fails, subject to the workflow reaching the upload step.

Expected result files are:

    test_ptm_roundtrip-results.txt
    test_ptm_shacl-results.txt

## 7. Configure repository security

For a public repository, consider enabling GitHub private vulnerability reporting in the repository security settings. `SECURITY.md` provides the PTM reporting and severity policy, but the repository setting controls availability of GitHub's private reporting feature.

## 8. Configure Cloudflare Pages after GitHub is stable

The static site is under:

    site/

The PTM Cloudflare configuration prepared for this repository is:

    Production branch:       main
    Framework preset:        None
    Root directory:          site
    Build command:           exit 0
    Build output directory:  .
    Environment variables:   None

Connect Cloudflare Pages only after the GitHub repository and CI workflow are behaving as expected.

## 9. Recommended acceptance check

Before treating the repository as the PTM candidate source of record, confirm:

- the expected files are present;
- `LICENSE`, `CONTRIBUTING.md`, and `SECURITY.md` display correctly;
- the Actions workflow is recognized;
- all required CI jobs pass;
- the ontology and SHACL artifacts are the intended versions;
- no secrets or confidential material were committed; and
- the Cloudflare site, if connected, is deploying from the intended branch and directory.

## Existing remote repository note

If the destination GitHub repository already contains commits, do not force-push this bundle over existing history. Clone or otherwise synchronize the existing repository first, integrate this bundle deliberately, review the changes, and then commit and push normally.
