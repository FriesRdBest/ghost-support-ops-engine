# ghost-support-ops-engine

Support operations engineering toolkit and automated diagnostics for Ghost publishers.

This project provides tooling to help Ghost site operators diagnose common issues, validate configuration, and automate routine support tasks. It is intended as a practical engineering aid rather than a polished end-user product.

## Features

- **Diagnostics** — Run automated checks against a Ghost site to surface configuration and content issues.
- **Toolkit utilities** — Helpers for common support and operations tasks.
- **Extensible checks** — Add new diagnostic rules as the platform evolves.

## Local development

### Requirements

- Python 3.10 or later
- `pip`

### Setup

```bash
git clone https://github.com/FriesRdBest/ghost-support-ops-engine.git
cd ghost-support-ops-engine
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Contributing

Contributions and focused feedback are welcome. Keep changes oriented towards reliability, clarity, and practical value for Ghost operators.

## License

Copyright 2026 Robin Sylvester.

Licensed under the [Apache License, Version 2.0](LICENSE).
