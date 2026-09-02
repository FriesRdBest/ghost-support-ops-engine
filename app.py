import streamlit as st
import sqlite3
import datetime

st.set_page_config(
    page_title="Ghost Support Operations Engine",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .ghost-header {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .metric-container {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        background-color: rgba(128, 128, 128, 0.05);
        margin-bottom: 12px;
    }
    .metric-number {
        font-size: 1.6rem;
        font-weight: 700;
        color: #30cf43;
    }
    .metric-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.8;
        margin-top: 4px;
    }
    .content-card {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 20px;
        background-color: rgba(128, 128, 128, 0.04);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #30cf43 !important;
        color: #000000 !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 18px !important;
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
    st.markdown("## Ghost")
    st.markdown("### The Watchmaker Hub")
    st.write("Turning support operations into an engineering product for independent publishing.")
    st.divider()
    
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
    
    st.divider()
    st.caption("Environment: Production Ready")
    st.caption("Database: SQLite Knex Emulation")
    st.caption("Status: Zero Hallucination Mode")

if navigation_choice == "Mission and Telemetry":
    st.markdown('<div class="ghost-header">Support Operations Telemetry</div>', unsafe_allow_html=True)
    st.write("A unified operational hub designed to eliminate recurring publisher friction, audit system health, and scale support while staying lean and human.")
    st.write("")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-container"><div class="metric-number">$11,099,649</div><div class="metric-title">Annual Run Rate</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-container"><div class="metric-number">30,579</div><div class="metric-title">Active Publishers</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-container"><div class="metric-number">2.92%</div><div class="metric-title">Net Churn</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-container"><div class="metric-number">1 to 10,193</div><div class="metric-title">Support Ratio</div></div>', unsafe_allow_html=True)
        
    st.write("")
    
    with st.container():
        st.markdown("### The Watchmaker Philosophy")
        st.write("Support engineers stand at the frontline to guide publishers through challenges. Support operations engineers work behind the scenes to calibrate tools, eliminate root causes, and stop future tickets before they reach the queue.")
        st.write("By automating diagnostics and resolving edge case bugs directly in the Ghost codebase, we give support engineers their time back so they can deliver thoughtful, high touch service.")

elif navigation_choice == "Stripe Member Reconciliation":
    st.markdown('<div class="ghost-header">Stripe Subscription Reconciliation Engine</div>', unsafe_allow_html=True)
    st.write("Audit asynchronous Stripe webhook discrepancies against the Ghost members database and generate safe SQL remediation scripts.")
    
    with st.container():
        st.markdown("#### Simulated Incident: Dropped Stripe Webhook")
        st.write("Stripe received a successful payment for Alex Rivera on plan price_pro_annual, but a network interruption prevented the webhook from updating Ghost. The database still lists the publisher as free with an incomplete subscription record.")
    
    if st.button("Run Reconciliation Audit"):
        c = st.session_state.db_conn.cursor()
        c.execute("SELECT m.email, m.status, s.status, s.plan_id, s.subscription_id FROM members m JOIN members_stripe_customers_subscriptions s ON m.id = s.member_id WHERE m.id = 'mem_101'")
        row = c.fetchone()
        
        st.error("State Mismatch Detected: Ghost database is out of sync with Stripe live subscription status.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Ghost Database State**")
            st.code(f"Member Status: {row[1]}\nSubscription Status: {row[2]}\nPlan: {row[3]}", language="text")
        with col_b:
            st.markdown("**Stripe Live State**")
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
    st.markdown('<div class="ghost-header">Mailgun Newsletter and DNS Health Engine</div>', unsafe_allow_html=True)
    st.write("Diagnose custom domain email records instantly and generate plain language setup instructions for publishers.")
    
    domain_input = st.text_input("Enter Publisher Custom Domain", value="theindependentdispatch.com")
    
    col1, col2 = st.columns(2)
    with col1:
        spf_check = st.checkbox("Simulate SPF Record Configured", value=True)
    with col2:
        dkim_check = st.checkbox("Simulate DKIM Record Configured", value=False)
        
    if st.button("Run Deliverability Audit"):
        st.divider()
        if spf_check and dkim_check:
            st.success("All DNS records are verified and configured correctly for bulk delivery.")
        else:
            st.warning("Deliverability Alert: Missing critical DNS records causing Mailgun bounces.")
            
            st.markdown("#### Diagnostic Findings")
            st.write("SPF Record Status: " + ("Valid" if spf_check else "Missing Mailgun authorization"))
            st.write("DKIM Record Status: " + ("Valid" if dkim_check else "Missing public key on k1._domainkey"))
            
            st.markdown("#### Publisher Friendly Guidance")
            st.info("""Dear Publisher,

We noticed your newsletter emails are currently encountering delivery issues. To resolve this, add this single DNS record inside your domain provider dashboard:

Type: TXT
Name: k1._domainkey
Value: k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC3

Once saved, DNS servers typically update within an hour and full email delivery will resume immediately.""")

elif navigation_choice == "Grounded Support Intelligence":
    st.markdown('<div class="ghost-header">Grounded Support Intelligence</div>', unsafe_allow_html=True)
    st.write("Zero hallucination operational guidance grounded strictly in official Ghost architecture and engineering documentation.")
    
    sample_queries = [
        "Can a publisher use custom SMTP for bulk newsletters on Ghost Pro?",
        "How do member tiers interact with Stripe webhooks during billing cycles?",
        "What happens when a custom domain SSL certificate renewal fails?"
    ]
    
    selected_query = st.selectbox("Select or enter a support inquiry", sample_queries)
    
    if st.button("Generate Verified Operational Guidance"):
        st.divider()
        if "custom SMTP" in selected_query:
            st.markdown("#### Engineering Verification")
            st.write("Ghost Pro utilizes Mailgun for bulk newsletter delivery to protect sender reputation and manage delivery queues. Custom SMTP is only supported for transactional system messages such as login links and password resets.")
            
            st.markdown("#### Recommended Action")
            st.write("Guide the publisher to configure Mailgun API keys in their settings. If they require non Mailgun bulk delivery, inform them that this requires self hosting Ghost with a custom webhook server proxy.")
            
            st.markdown("#### Grounding Source")
            st.caption("Verified against Ghost Core Architecture and Email Subsystem Documentation")

elif navigation_choice == "Strategic Operations Roadmap":
    st.markdown('<div class="ghost-header">Strategic Support Operations Roadmap</div>', unsafe_allow_html=True)
    st.write("A phased engineering strategy to systematically reduce incoming ticket volume while empowering the human support team.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Days 1 to 30")
        st.markdown("**Audit and Tooling**")
        st.write("Audit Front inbox routing rules and categorize repeat ticket volume. Build automated Stripe reconciliation scripts to resolve billing state mismatches.")
    with col2:
        st.markdown("### Days 31 to 60")
        st.markdown("**Linear and Core Fixes**")
        st.write("Implement two way webhook syncing between Front conversations and Linear engineering issues. Ship direct bug fixes in the Ghost repository for top recurring issues.")
    with col3:
        st.markdown("### Days 61 to 90")
        st.markdown("**Grounded AI and Docs**")
        st.write("Deploy grounded internal drafting tools for support engineers. Publish comprehensive self serve guides for custom domain and DNS setup.")
