import streamlit as st
import json
import pandas as pd
import plotly.express as px

from modules.safety_tips import get_safety_tip
from modules.challan_calculator import calculate_challan
from modules.chatbot import ask_ai
from modules.rule_lookup import get_rules_by_state
from modules.legal_simplifier import simplify_law

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="DriveLegal AI",
    page_icon="🚦",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main App */

.stApp {
    background-color: #0f172a;
    color: #ffffff !important;
}

/* Headings */

h1, h2, h3 {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

/* All text */

p, span, div, label, li {
    color: #f8fafc !important;
}

/* Buttons */

.stButton > button {
    background-color: #38bdf8;
    color: black !important;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #0ea5e9;
    color: white !important;
}

/* Success Box */

.stSuccess {
    background-color: #14532d !important;
    color: white !important;
    border-radius: 10px;
}

.stSuccess * {
    color: white !important;
}

/* Info Box */

.stInfo {
    background-color: #0c4a6e !important;
    color: white !important;
    border-radius: 10px;
}

.stInfo * {
    color: white !important;
}

/* Warning Box */

.stWarning {
    background-color: #78350f !important;
    color: white !important;
    border-radius: 10px;
}

.stWarning * {
    color: white !important;
}

/* Error Box */

.stError {
    background-color: #7f1d1d !important;
    color: white !important;
}

.stError * {
    color: white !important;
}

/* Chat */

.stChatMessage {
    background-color: #1e293b;
    border-radius: 12px;
}

.stChatMessage * {
    color: white !important;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Selectbox labels */

.stSelectbox label {
    color: white !important;
    font-weight: bold;
}

/* Chat input */

.stChatInputContainer textarea {
    color: white !important;
}

/* Metric Values */

[data-testid="stMetricValue"] {
    color: #38bdf8 !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
# ---------------- SIDEBAR ----------------

st.sidebar.title("🚘 DriveLegal AI")

st.sidebar.info("""
DriveLegal AI helps citizens:

✅ Check traffic fines
✅ Calculate challans
✅ Understand road laws
✅ Improve road safety awareness
✅ Access location-based regulations
✅ Supports offline rule lookup
""")

# ---------------- TITLE ----------------

st.markdown("""
# 🚦 DriveLegal AI

### AI-Powered Traffic Law, Challan & Road Safety Assistant
""")

st.info(
    "🌐 Offline Mode Supported: Rule Lookup and Challan Calculator work without internet."
)

# ---------------- LOAD DATA ----------------

with open("data/traffic_rules.json", "r") as file:
    rules = json.load(file)

df = pd.DataFrame(rules)

# ---------------- COUNTRY SELECTOR ----------------

countries = sorted(df["country"].unique())

country = st.selectbox(
    "🌍 Select Country",
    countries
)

# ---------------- STATE SELECTOR ----------------

states = sorted(
    df[df["country"] == country]["state"].unique()
)

state = st.selectbox(
    "📍 Select State / Region",
    states
)

# ---------------- VEHICLE SELECTOR ----------------

vehicles = sorted(
    df["vehicle"].unique()
)

vehicle = st.selectbox(
    "🚗 Select Vehicle Type",
    vehicles
)

# ---------------- VIOLATION SELECTOR ----------------

violations = sorted(
    df[
        (df["country"] == country)
        & (df["state"] == state)
    ]["violation"].unique()
)

violation = st.selectbox(
    "🚨 Select Violation",
    violations
)

# ---------------- OFFENSE COUNT ----------------

offense_count = st.selectbox(
    "🔁 Previous Offenses",
    [0, 1, 2, 3]
)

# ---------------- CHALLAN CALCULATOR ----------------

st.header("💰 Automated Challan Calculator")

if st.button("Calculate Challan"):

    result = calculate_challan(
        country,
        state,
        vehicle,
        violation,
        offense_count
    )

    if result:

        st.success(
            f"💰 Fine Amount: ₹{result['calculated_fine']}"
        )

        st.info(
            f"📜 Law Section: {result['law']}"
        )

        st.write("### 🚨 Violation Description")
        st.write(result["description"])

        st.warning(
            get_safety_tip(violation)
        )

        st.write("### 📖 Easy Legal Explanation")

        st.success(
            simplify_law(result)
        )

    else:

        st.error(
            "No matching traffic rule found."
        )

# ---------------- AI ASSISTANT ----------------

st.header("🤖 DriveLegal AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask any traffic law question..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    response = ask_ai(prompt)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response)

# ---------------- RULE LOOKUP ----------------

st.header("📚 Geo-Fenced Traffic Rule Lookup")

lookup_country = st.selectbox(
    "Country",
    countries,
    key="country_lookup"
)

lookup_states = sorted(
    df[df["country"] == lookup_country]["state"].unique()
)

lookup_state = st.selectbox(
    "State",
    lookup_states,
    key="state_lookup"
)

if st.button("Show Applicable Rules"):

    state_rules = get_rules_by_state(
        lookup_country,
        lookup_state
    )

    for rule in state_rules:

        st.write(f"## 🚦 {rule['violation']}")

        st.write(
            f"💰 Fine: ₹{rule['fine']}"
        )

        st.write(
            f"📜 Law Section: {rule['law']}"
        )

        st.write(
            f"⚠️ Description: {rule['description']}"
        )

        st.divider()

# ---------------- DASHBOARD ----------------

st.header("📊 Traffic Analytics Dashboard")

# Violations

violation_count = (
    df["violation"]
    .value_counts()
    .reset_index()
)

violation_count.columns = [
    "Violation",
    "Count"
]

fig1 = px.bar(
    violation_count,
    x="Violation",
    y="Count",
    title="Most Common Traffic Violations"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Vehicles

vehicle_count = (
    df["vehicle"]
    .value_counts()
    .reset_index()
)

vehicle_count.columns = [
    "Vehicle",
    "Count"
]

fig2 = px.pie(
    vehicle_count,
    names="Vehicle",
    values="Count",
    title="Vehicle Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Countries

country_count = (
    df["country"]
    .value_counts()
    .reset_index()
)

country_count.columns = [
    "Country",
    "Count"
]

fig3 = px.bar(
    country_count,
    x="Country",
    y="Count",
    title="Traffic Rule Coverage Across Countries"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------- FOOTER ----------------

st.markdown("---")

st.markdown("""
### 🚀 Road Safety Hackathon 2026

DriveLegal AI combines:

- Geo-Fenced Rule Lookup
- Automated Challan Calculator
- AI Legal Assistant
- Legal Simplifier
- Offline Rule Access
- Multi-Country Traffic Law Framework

Built for safer roads and informed citizens.
""")