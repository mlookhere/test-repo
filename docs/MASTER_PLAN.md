# Master plan — Small Test Website

Repository: `mlookhere/test-repo`  
Integration: `dev` · Production: `main`  
Stack: static HTML5, CSS3, modern vanilla JavaScript (Node.js 22 for JS checks), Python 3.12 for the vendored CI infrastructure and Python `unittest` website checks. No runtime framework, backend, database, secrets, or deployment services.

## Execution contract

One Issue per numbered slice; development branches `work/<issue-number>-<slug>` from `dev`; PRs target `dev`; release is `dev` into `main`. Do not merge without successful completed GitHub Actions checks. Every PR includes `Refs #<issue>` and the required Result, Implementation, Verification, Risk, and Remaining work sections.

### CI configuration

`.claude-workflow.json` uses `github.expected_owner=mlookhere`, `github.expected_repository=test-repo`, `branches.integration=dev`, `branches.production=main`, and `quality.source_extensions=[.py,.js,.ts,.html,.css]`. `risk:dependencies` adds `package.json` and `package-lock.json`; the project does not need a Node dependency manifest.

Planned command groups (ensure every invoked group executes a real command in item 1):
- `bootstrap_local`: `"$CI_PYTHON" -m pytest --version`; `"$CI_PYTHON" -m mypy --version`; `"$CI_PYTHON" -m ruff --version`; `"$CI_PYTHON" -m pip_audit --version`.
- `bootstrap_ci`: same four commands.
- `workflow_self_test`: `"$CI_PYTHON" workflow/self_test.py --ci`.
- `format_check`: `ruff format --check .`.
- `lint`: `ruff check .`; `node --check assets/app.js`.
- `typecheck`: `mypy` (configure concrete mypy targets in item 1).
- `unit`: `python3 -m unittest discover -s tests -v`.
- `coverage`: `python3 -m unittest discover -s tests -v` (must assert a nonzero executed-test count; not a substitute for coverage measurement if a coverage threshold is adopted).
- `security`: `pip-audit -r ci/requirements-ci.txt --strict`.

Stages: `fast=[workflow_self_test,quality,format_check,lint,typecheck]`; `pr=[unit,coverage]`; `release=[security,unit,coverage]`; `nightly=[security,unit,coverage]`; `audit=[security]`; `bootstrap-local=[bootstrap_local]`; `bootstrap-ci=[bootstrap_ci]`. The vendored `./scripts/bootstrap --ci` and `./ci/run <stage>` remain the sole workflow entry points and all original GitHub Actions job names remain unchanged.

## 1. Scaffold the project and make hello-world pass fast and PR CI
**Acceptance:** `index.html`, `assets/styles.css`, and `assets/app.js` render a valid hello-world page; reproducible Python unittest suite has at least one real assertion; Node syntax check runs; Python CI tool configuration is installed; both `./ci/run fast` and `./ci/run pr` actually execute and pass on GitHub Actions. Fix any vendoring compatibility defects without removing checks or reducing thresholds.  
**Areas:** root HTML; `assets/`; `tests/`; `pyproject.toml`; `.claude-workflow.json`; CI setup only as needed.  
**Gates:** PR metadata; Fast deterministic gates; PR test/build gates; Dependency audit; Workflow policy.  
**Risk:** `risk:ci`, `risk:dependencies`.

## 2. Build a responsive, accessible landing page
**Acceptance:** A compact header, clear main message, explanatory section, and footer render correctly on narrow and wide screens; semantic headings, keyboard-visible focus, adequate contrast, and responsive layout are verified by tests. No runtime dependencies.  
**Areas:** `index.html`, `assets/styles.css`, `tests/`.  
**Gates:** fast, pr; all PR Actions checks.  
**Risk:** none.

## 3. Add one lightweight interactive feature and polish
**Acceptance:** A user-operable theme toggle persists only a theme preference, honors initial system preference, updates `aria-pressed`, works with keyboard, and degrades gracefully without JavaScript; tests cover markup and JS syntax. The site has no console errors or broken local references.  
**Areas:** `index.html`, `assets/styles.css`, `assets/app.js`, `tests/`.  
**Gates:** fast, pr; all PR Actions checks.  
**Risk:** none.

## 4. Release — merge dev into main with green release checks
**Acceptance:** All preceding item PRs are merged into `dev`; create a release PR with source `dev`, target `main`, linked to this release Issue; the `release` stage and every GitHub Actions check complete successfully; merge only after green checks, verify `main` matches the approved release.  
**Areas:** release PR, documentation and control Issue; no unrelated source changes.  
**Gates:** Release metadata; Full regression and production build; Workflow policy; every other check GitHub schedules on the release PR.  
**Risk:** `risk:deployment`.

No check is considered green when missing, pending, or failed.
