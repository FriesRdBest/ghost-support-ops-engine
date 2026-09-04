**Ghost Support Operations Engine**
A dedicated support operations engineering toolkit designed to eliminate recurring publisher friction, automate complex diagnostics, and scale support for Ghost Pro.
Built around the philosophy of The Watchmaker & The Lighthouse: treating frontline support as our primary product and equipping engineers with precision tooling.

**Live Links & Resources**
Live Interactive Diagnostics Hub: ghost-support-ops-engine.streamlit.app
Strategic Operations Blueprint: Integrated in app and delivered via executive PDF
Target Architecture: Ghost Core (Node.js/Knex), Stripe API, Mailgun DNS, Front, Linear

**Architecture Overview**
                      ┌──────────────────────────────────────────────┐
                      │        GHOST SUPPORT OPERATIONS HUB          │
                      └──────────────────────┬───────────────────────┘
                                             │
         ┌────────────────────────┬──────────┴───────────┬─────────────────────────┐
         ▼                        ▼                      ▼                         ▼
┌──────────────────┐    ┌──────────────────┐   ┌──────────────────┐      ┌──────────────────┐
│ Stripe Member    │    │ Mailgun & DNS    │   │ Grounded Support │      │ Front <-> Linear │
│ Reconciliation   │    │ Health Engine    │   │ Intelligence     │      │ Webhook Router   │
├──────────────────┤    ├──────────────────┤   ├──────────────────┤      ├──────────────────┤
│• Webhook Audit   │    │• SPF / DKIM Auth │   │• Zero-Slop RAG   │      │• Two-way sync    │
│• Safe SQL Engine │    │• Mailgun Triage  │   │• Grounded Docs   │      │• Bug Escalation  │
│• State Healing   │    │• Publisher Guide │   │• Human Review    │      │• Reproduction    │
└──────────────────┘    └──────────────────┘   └──────────────────┘      └──────────────────┘

**Core Engineering Modules**
1. Stripe Subscription State Reconciler (diagnostic_core.py)
Addresses one of the most frequent technical edge cases in creator billing: asynchronous webhook drops (customer.subscription.updated) that leave paid members flagged with free status in Ghost's members database table.
Reconciliation Logic: Ingests live Stripe subscription objects, queries members and members_stripe_customers_subscriptions, identifies discrepancies, and outputs atomic Knex/SQL remediation transactions.
Safety: Every generated remediation runs in an isolated transaction block (BEGIN TRANSACTION ... COMMIT) to prevent partial database writes.

2. Mailgun Newsletter & Custom Domain DNS Diagnostic Engine
Analyzes custom domain DNS records (SPF, DKIM on selector k1._domainkey, and DMARC) to identify newsletter deliverability drops.
Generates clear, non-technical instructions for publishers to paste directly into Cloudflare, Namecheap, or GoDaddy.
Automates Front conversation tagging (#deliverability-dkim) and severity escalation.

3. Grounded Support Intelligence Assistant
An internal engineering copilot built strictly with zero-hallucination guardrails. Grounded directly in official Ghost Core architectural specifications:
Custom bulk SMTP boundary verification
Stripe subscription lifecycle and invoice retry dynamics
Edge proxy SSL certificate provisioning and CAA record diagnostics

**Upstream Core Fix Simulation (Sample PR)**
This repository includes an upstream bug fix simulation targeting Ghost core (TryGhost/Ghost):
Issue: Asynchronous Subscription Reconnection on Interrupted Webhooks
File: ghost/core/core/server/services/members/service.js
Fix Description: Implements an idempotent fallback query during member tier validation that verifies live Stripe status when a local membership record displays incomplete past the grace window.
Impact: Prevents publishers from having paying subscribers erroneously locked out of premium content following temporary network timeouts.

**Running Locally**
**Prerequisites**
Python 3.10+
Git

**Installation**
# Clone the repository
git clone https://github.com/FriesRdBest/ghost-support-ops-engine.git
cd ghost-support-ops-engine
# Install dependencies
pip install -r requirements.txt
# Run the Streamlit hub
streamlit run app.py

**License**
This project is open-source under the MIT License.
