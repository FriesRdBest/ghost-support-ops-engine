# Contributing to ghost-support-ops-engine

Thank you for your interest in improving the Ghost Support Ops Engine. This repository provides support operations tooling and automated diagnostics for Ghost publishers.

## Before you contribute

- Review the [README](README.md) for the project scope and local setup.
- Search existing issues before opening a new one.
- Keep proposals focused on reliability, clarity, and practical value for Ghost operators.
- Do not include client data, confidential business information, credentials, API keys, or personal information in issues, pull requests, screenshots, or exported files.

## Local setup

```bash
git clone https://github.com/FriesRdBest/ghost-support-ops-engine.git
cd ghost-support-ops-engine
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Contribution guidelines

1. Create a branch from `main`.
2. Make one focused change at a time.
3. Run the app locally and exercise the affected workflow.
4. Check formatting and syntax before opening a pull request:

```bash
python -m py_compile app.py
git diff --check
```

5. In your pull request, explain the problem, the change, validation performed, and any user-facing impact.

## Design principles

- Keep tooling understandable for operators and support engineers.
- Prefer clear diagnostics and actionable output over decorative complexity.
- Preserve responsive behavior across desktop, tablet, and mobile widths.
- Treat exported reports as stakeholder-facing documents.

## Reporting issues

Use the repository issue templates for bugs and feature requests. For security concerns, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
