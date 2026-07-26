import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="SENTINEL-X Dashboard", layout="wide")

DATA_PATH = Path("mock_data")

def load_json(filename):
    with open(DATA_PATH / filename) as f:
        return json.load(f)

st.title("🛡️ SENTINEL-X")
st.subheader("Self-Healing Autonomous Cyber Infrastructure")

menu = st.sidebar.radio(
    "Navigation",
    [
        "System Overview",
        "Incident Detection",
        "Decision & Reasoning",
        "Self-Healing Actions",
        "Learning & Governance"
    ]
)

if menu == "System Overview":
    st.markdown("### System Status")
    st.success("System Operating Normally")

    incidents = load_json("analyzed_incidents.json")
    st.metric("Incidents Detected", len(incidents))

elif menu == "Incident Detection":
    st.markdown("### Detected Incidents")
    incidents = load_json("analyzed_incidents.json")
    st.table(incidents)

elif menu == "Decision & Reasoning":
    st.markdown("### AI Decision Explanation")
    decisions = load_json("decisions_enhanced.json")
    for d in decisions:
        st.write(f"**Incident:** {d['incident_id']}")
        st.write(f"**Decision:** {d['decision']}")
        st.write(f"**Confidence:** {d['confidence']}")
        st.info(d["reasoning"])

elif menu == "Self-Healing Actions":
    st.markdown("### Recovery Actions")
    actions = load_json("action_log.json")
    st.table(actions)

elif menu == "Learning & Governance":
    st.markdown("### Learning & Governance")
    st.info("System learns from past incidents and applies autonomy limits.")
