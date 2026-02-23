🔗 Live App: https://taylorheyward-invisible-cost-calculator-app-aomdjd.streamlit.app/ 
The Invisible Cost Calculator is a visual tool that reveals the hidden social, environmental, and human costs behind everyday “cheap” decisions, making tradeoffs visible rather than invisible.

This project helps analysts, product teams, and policy makers explore how decisions that look financially cheap today can impose larger, often unseen costs over time. It combines scenario modelling, score-based allocation, and fast Monte Carlo sampling to quantify a simple, interpretable "hidden cost" metric and show its distribution across plausible futures.

Key features

- Interactive scenario comparison: define two scenarios and compare their implied hidden costs side-by-side.
- Live scoring weights: tune how much different signals (cap rate, occupancy, discount, risk, liquidity) matter and see allocations update immediately.
- Per-type and per-asset overrides: override multipliers for asset classes or individual assets to model targeted interventions or tail risks.
- Fast, vectorized Monte Carlo engine: run thousands of simulations quickly to get distributions, ECDFs, and probabilities (e.g., P(A < B)).
- Visual outputs & exports: Plotly-based histograms, ECDFs, allocation tables, and downloadable HTML reports with embedded charts.

How it works (brief)

1. Assets are scored using normalized signals (cap rate, occupancy, discount, risk, liquidity) and a set of user-controlled weights.
2. Scores are converted to allocation weights via a softmax-like transformation.
3. A per-asset "hidden cost" proxy is computed as nominal_value × allocation_weight × adjusted_discount; scenario multipliers and uncertainty (the "certainty dial") change adjusted discounts.
4. The Monte Carlo engine samples scenario and asset-level perturbations, producing a distribution of hidden-cost totals that the UI visualizes and summarizes.

Quick start

Requirements

- Python 3.10+
- Streamlit, pandas, numpy, plotly

Install (in a virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Usage tips

- Use the Certainty dial to model more or less volatile futures (lower certainty = wider tails).
- Tweak Score Weights to capture your intuition about what matters most for allocation decisions.
- Use per-asset overrides to model specific risks (e.g., known legal issues, ESG flags, or concentration effects).
- Run the Monte Carlo and download the HTML report to share findings with stakeholders.

Design goals

- Make hidden tradeoffs visible and actionable.
- Keep the models transparent and auditable (no black-box ML models required).
- Be fast enough for interactive exploration while flexible enough for deeper analysis.

Contributing

Contributions, feature requests, and bug reports are welcome. Please open an issue or a pull request. If you add new data transformations or external data sources, include tests and update the README example dataset.

License

See the LICENSE file in the repository (MIT by default unless otherwise specified).

