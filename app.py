import streamlit as st

from invisible_cost import Calculator
from main import build_scenarios  # re-use curated scenarios


st.set_page_config(page_title="Invisible Cost Calculator", layout="centered")

st.title("The Invisible Cost Calculator")
st.write("A tool for seeing the hidden bill behind cheap choices.")

scenarios = build_scenarios()
scenario_map = {s.name: s for s in scenarios}
choice = st.selectbox("Choose a scenario", list(scenario_map.keys()))

calc = Calculator(max_items_for_scaling=10)
report = calc.evaluate(scenario_map[choice])

col1, col2 = st.columns(2)
with col1:
    st.metric("Visible price", f"${report['visible_price']:.2f}")
with col2:
    st.metric("Hidden cost score", f"{report['hidden_score']:.1f} / 100")

st.subheader("Who pays most")
for bearer, val in report["top_bearers"]:
    st.write(f"- {bearer} (impact: {val:.2f})")

st.subheader("Category breakdown")
cats = report["breakdown_by_category"]
if cats:
    st.bar_chart(cats)

st.subheader("What is going on here")
st.write(report["explanation"])

with st.expander("See the underlying assumptions"):
    st.write("Each hidden cost item has a severity (1–5) and a certainty (0–1).")
    st.write("Impact is severity × certainty. Scores are scaled to 0–100 for interpretability.")
    st.write("This is not a moral verdict. It is a structured estimate to make tradeoffs visible.")

with st.expander("See the cost items"):
    for item in report["items"]:
        st.write(
            f"• {item.category} | bearer: {item.bearer} | "
            f"severity: {item.severity} | certainty: {item.certainty:.2f} | {item.note}"
        )