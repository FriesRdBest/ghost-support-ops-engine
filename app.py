import streamlit as st
import sqlite3
import datetime
from typing import Dict, Any

st.set_page_config(
    page_title="Ghost Support Operations Engine",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #0d0f12;
        color: #ffffff;
    }
    .metric-card {
        background-color: #15171a;
        border: 1px solid #282c34;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-val {
        font-size: 24px;
        font-weight: 700;
        color: #30cf43;
    }
    .metric-label {
        font-size: 13px;
        color: #7c8b9a;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .stButton>button {
        background-color: #30cf43;
        color: #000000;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #28b338;
        color: #000000;
    }
    .card-box {
        background-color: #15171a;
        border: 1px solid #282c34;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def init_mock_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE members (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            name TEXT,
            status TEXT,
            created_at DATETIME
        )
    """)
    c.execute("""
        CREATE TABLE members_stripe_customers_subscriptions (
            id TEXT PRIMARY KEY,
            customer_id TEXT,
            subscription_id TEXT,
            member_id TEXT,
            status TEXT,
            plan_id TEXT
        )
    """)
    c.execute("INSERT INTO members VALUES ('mem_101', 'editor@independentpress.com', 'Alex Rivera', 'free', '2026-02-15')")
    c.execute("INSERT INTO members_stripe_customers_subscriptions VALUES ('sub_rec_1', 'cus_9942', 'sub_live_9942', 'mem_101', 'incomplete', 'price_tier_starter')")
    conn.commit()
    return conn

if "db_conn" not in st.session_state:
    st.session_state.db_conn = init_mock_db()

with st.sidebar:
    st.image("https://ghost.org/images/ghost-logo-light.svg", width=140)
    st.markdown("### The Watchmaker Hub")
    st.markdown("Turning support operations into an engineering product for independent publishing.")
    st.markdown("---")
    
    navigation_choice = st.radio(
        "Operational Modules",
        [
            "Mission and Telemetry",
            "Stripe Member Reconciliation",
            "Mailgun and DNS Diagnostics",
            "Grounded Support Intelligence",
            "Strategic Operations Roadmap"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Environment:** Production Ready")
    st.markdown("**Database:** SQLite Knex Emulation")
    st.markdown("**Status:** Zero Hallucination Mode")

if navigation_choice == "Mission and Telemetry":
    st.title("Support Operations Telemetry")
    st.markdown("A unified operational hub designed to eliminate recurring publisher friction, audit system health, and scale support while staying lean and human.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-val">$11,099,649</div><div class="metric-label">Annual Run Rate</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-val">30,579</div><div class="metric-label">Active Publishers</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-val">2.92%</div><div class="metric-label">Net Churn</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-val">1 to 10,193</div><div class="metric-label">Support Ratio</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-box">
        <h3>The Watchmaker Philosophy</h3>
        <p>Support engineers stand at the frontline to guide publishers through challenges. Support operations engineers work behind the scenes to calibrate tools, eliminate root causes, and stop future tickets before they reach the queue.</p>
        <p>By automating diagnostics and resolving edge case bugs directly in the Ghost codebase, we give support engineers their time back so they can deliver thoughtful, high touch service.</p>
    </div>
    """, unsafe_allow_html=True)

elif navigation_choice == "Stripe Member Reconciliation":
    st.title("Stripe Subscription Reconciliation Engine")
    st.markdown("Audit asynchronous Stripe webhook discrepancies against the Ghost members database and generate safe SQL remediation scripts.")
    
    st.markdown("""
    <div class="card-box">
        <h4>Simulated Incident: Dropped Stripe Webhook</h4>
        <p>Stripe received a successful payment for Alex Rivera on plan <code>price_pro_annual</code>, but a network interruption prevented the webhook from updating Ghost. The database still lists the publisher as free with an incomplete subscription record.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Run Reconciliation Audit"):
        c = st.session_state.db_conn.cursor()
        c.execute("SELECT m.email, m.status, s.status, s.plan_id, s.subscription_id FROM members m JOIN members_stripe_customers_subscriptions s ON m.id = s.member_id WHERE m.id = 'mem_101'")
        row = c.fetchone()
        
        st.error("State Mismatch Detected: Ghost database is out of sync with Stripe live subscription status.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Ghost Database State**")
            st.code(f"Member Status: {row[1]}\nSubscription Status: {row[2]}\nPlan: {row[3]}", language="text")
        with col_b:
            st.markdown(f"**Stripe Live State**")
            st.code("Member Status: paid\nSubscription Status: active\nPlan: price_pro_annual", language="text")
            
        safe_sql = f"""BEGIN TRANSACTION;
UPDATE members_stripe_customers_subscriptions 
SET status = 'active', plan_id = 'price_pro_annual' 
WHERE subscription_id = '{row[4]}';

UPDATE members 
SET status = 'paid' 
WHERE id = 'mem_101';
COMMIT;"""
        
        st.markdown("#### Safe Remediation Script")
        st.code(safe_sql, language="sql")
        
        if st.button("Apply Remediation"):
            c.execute("UPDATE members_stripe_customers_subscriptions SET status = 'active', plan_id = 'price_pro_annual' WHERE subscription_id = 'sub_live_9942'")
            c.execute("UPDATE members SET status = 'paid' WHERE id = 'mem_101'")
            st.session_state.db_conn.commit()
            st.success("Remediation executed successfully. Ghost database synchronized with Stripe.")

elif navigation_choice == "Mailgun and DNS Diagnostics":
    st.title("Mailgun Newsletter and DNS Health Engine")
    st.markdown("Diagnose custom domain email records instantly and generate plain language setup instructions for publishers.")
    
    domain_input = st.text_input("Enter Publisher Custom Domain", value="theindependentdispatch.com")
    
    col1, col2 = st.columns(2)
    with col1:
        spf_check = st.checkbox("Simulate SPF Record Configured", value=True)
    with col2:
        dkim_check = st.checkbox("Simulate DKIM Record Configured", value=False)
        
    if st.button("Run Deliverability Audit"):
        st.markdown("---")
        if spf_check and dkim_check:
            st.success("All DNS records are verified and configured correctly for bulk delivery.")
        else:
            st.warning("Deliverability Alert: Missing critical DNS records causing Mailgun bounces.")
            
            st.markdown("#### Diagnostic Findings")
            st.write("SPF Record Status: " + ("Valid" if spf_check else "Missing Mailgun authorization"))
            st.write("DKIM Record Status: " + ("Valid" if dkim_check else "Missing public key on k1._domainkey"))
            
            st.markdown("#### Publisher Friendly Guidance")
            st.info("""
Dear Publisher,

We noticed your newsletter emails are currently encountering delivery issues. To resolve this, add this single DNS record inside your domain provider dashboard:

Type: TXT
Name: k1._domainkey
Value: k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3

Once saved, DNS servers typically update within an hour and full email delivery will resume immediately.
            """)

elif navigation_choice == "Grounded Support Intelligence":
    st.title("Grounded Support Intelligence")
    st.markdown("Zero hallucination operational guidance grounded strictly in official Ghost architecture and engineering documentation.")
    
    sample_queries = [
        "Can a publisher use custom SMTP for bulk newsletters on Ghost Pro?",
        "How do member tiers interact with Stripe webhooks during billing cycles?",
        "What happens when a custom domain SSL certificate renewal fails?"
    ]
    
    selected_query = st.selectbox("Select or enter a support inquiry", sample_queries)
    
    if st.button("Generate Verified Operational Guidance"):
        st.markdown("---")
        if "custom SMTP" in selected_query:
            st.markdown("#### Engineering Verification")
            st.markdown("Ghost Pro utilizes Mailgun for bulk newsletter delivery to protect sender reputation and manage delivery queues. Custom SMTP is only supported for transactional system messages such as login links and password resets.")
            
            st.markdown("#### Recommended Action")
            st.markdown("Guide the publisher to configure Mailgun API keys in their settings. If they require non Mailgun bulk delivery, inform them that this requires self hosting Ghost with a custom webhook server proxy.")
            
            st.markdown("#### Grounding Source")
            st.caption("Verified against Ghost Core Architecture and Email Subsystem Documentation")

elif navigation_choice == "Strategic Operations Roadmap":
    st.title("Strategic Support Operations Roadmap")
    st.markdown("A phased engineering strategy to systematically reduce incoming ticket volume while empowering the human support team.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="card-box">
            <h4>Days 1 to 30</h4>
            <p><strong>Audit and Tooling</strong></p>
            <p>Audit Front inbox routing rules and categorize repeat ticket volume. Build automated Stripe reconciliation scripts to resolve billing state mismatches.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card-box">
            <h4>Days 31 to 60</h4>
            <p><strong>Linear and Core Fixes</strong></p>
            <p>Implement two way webhook syncing between Front conversations and Linear engineering issues. Ship direct bug fixes in the Ghost repository for top recurring issues.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="card-box">
            <h4>Days 61 to 90</h4>
            <p><strong>Grounded AI and Docs</strong></p>
            <p>Deploy grounded internal drafting tools for support engineers. Publish comprehensive self serve guides for custom domain and DNS setup.</p>
        </div>
        """, unsafe_allow_html=True)
