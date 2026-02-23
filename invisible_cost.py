from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
from collections import defaultdict


@dataclass(frozen=True)
class CostItem:
    """A single hidden cost component for a scenario."""
    category: str           # e.g., "labor", "environment", "health", "privacy"
    bearer: str             # e.g., "workers", "consumer", "public", "future generations"
    severity: int           # 1–5 (how bad)
    certainty: float        # 0–1 (how confident)
    note: str               # 1–2 sentences explaining the mechanism

    def weighted_impact(self) -> float:
        """Return severity weighted by certainty."""
        return float(self.severity) * float(self.certainty)


class Scenario:
    """A 'cheap choice' with a visible price and a set of hidden cost items."""

    def __init__(self, name: str, visible_price: float, description: str = "") -> None:
        self.name = name
        self.visible_price = float(visible_price)
        self.description = description
        self.items: List[CostItem] = []

    def add_item(self, item: CostItem) -> None:
        """Add a hidden cost item."""
        if not (1 <= item.severity <= 5):
            raise ValueError("severity must be between 1 and 5")
        if not (0.0 <= item.certainty <= 1.0):
            raise ValueError("certainty must be between 0 and 1")
        self.items.append(item)

    def raw_hidden_score(self) -> float:
        """Sum of weighted impacts."""
        return sum(i.weighted_impact() for i in self.items)

    def hidden_score_0_to_100(self, max_items: int = 10) -> float:
        """Scale raw score to a 0–100 score using a cap for interpretability."""
        max_raw = max_items * 5.0 * 1.0
        raw = self.raw_hidden_score()
        scaled = (raw / max_raw) * 100.0
        if scaled < 0:
            return 0.0
        if scaled > 100:
            return 100.0
        return scaled

    def breakdown_by_category(self) -> Dict[str, float]:
        """Return weighted impact summed by category."""
        out: Dict[str, float] = defaultdict(float)
        for item in self.items:
            out[item.category] += item.weighted_impact()
        return dict(out)

    def breakdown_by_bearer(self) -> Dict[str, float]:
        """Return weighted impact summed by who bears the cost."""
        out: Dict[str, float] = defaultdict(float)
        for item in self.items:
            out[item.bearer] += item.weighted_impact()
        return dict(out)

    def top_bearers(self, n: int = 3) -> List[Tuple[str, float]]:
        """Return top n bearers by weighted impact."""
        b = self.breakdown_by_bearer()
        return sorted(b.items(), key=lambda x: x[1], reverse=True)[:n]

    def top_categories(self, n: int = 3) -> List[Tuple[str, float]]:
        """Return top n categories by weighted impact."""
        c = self.breakdown_by_category()
        return sorted(c.items(), key=lambda x: x[1], reverse=True)[:n]


class Calculator:
    """Evaluates scenarios and generates human-readable conclusions."""

    def __init__(self, max_items_for_scaling: int = 10) -> None:
        self.max_items_for_scaling = max_items_for_scaling

    def evaluate(self, scenario: Scenario) -> Dict:
        """Return a report dictionary for a scenario."""
        score = scenario.hidden_score_0_to_100(max_items=self.max_items_for_scaling)
        top_bearers = scenario.top_bearers(3)
        top_categories = scenario.top_categories(3)

        explanation = self._explain(scenario, score, top_bearers, top_categories)

        return {
            "name": scenario.name,
            "visible_price": scenario.visible_price,
            "description": scenario.description,
            "hidden_score": score,
            "raw_hidden_score": scenario.raw_hidden_score(),
            "breakdown_by_category": scenario.breakdown_by_category(),
            "breakdown_by_bearer": scenario.breakdown_by_bearer(),
            "top_bearers": top_bearers,
            "top_categories": top_categories,
            "items": scenario.items,
            "explanation": explanation,
        }

    def compare(self, a: Scenario, b: Scenario) -> Dict:
        """Compare two scenarios and return a combined report."""
        ra = self.evaluate(a)
        rb = self.evaluate(b)
        winner = a.name if ra["hidden_score"] < rb["hidden_score"] else b.name
        return {"a": ra, "b": rb, "lower_hidden_cost": winner}

    def _explain(
        self,
        scenario: Scenario,
        score: float,
        top_bearers: List[Tuple[str, float]],
        top_categories: List[Tuple[str, float]],
    ) -> str:
        """Generate a short explanation from the report components."""
        if not scenario.items:
            return "No hidden costs have been defined yet."

        bearers_text = ", ".join([b[0] for b in top_bearers if b[0]]) or "unknown groups"
        cats_text = ", ".join([c[0] for c in top_categories if c[0]]) or "unknown categories"

        if score >= 70:
            tone = "This looks cheap up front, but the hidden bill is heavy."
        elif score >= 40:
            tone = "The sticker price is not the full story."
        else:
            tone = "Relative to other choices, the hidden bill is lighter."

        return (
            f"{tone} The biggest costs tend to land on {bearers_text}. "
            f"The main pressure points are {cats_text}. "
            f"This score is a structured estimate, not a perfect measurement."
        )


class ReportFormatter:
    """Formats reports for terminal or markdown output."""

    @staticmethod
    def to_terminal(report: Dict) -> str:
        """Return a readable terminal string."""
        lines: List[str] = []
        lines.append(f"\n{report['name']}")
        if report.get("description"):
            lines.append(f"{report['description']}")
        lines.append(f"Visible price: ${report['visible_price']:.2f}")
        lines.append(f"Hidden cost score: {report['hidden_score']:.1f} / 100")

        lines.append("\nWho pays most:")
        for bearer, val in report["top_bearers"]:
            lines.append(f"  - {bearer}: {val:.2f}")

        lines.append("\nCategory breakdown:")
        cat = report["breakdown_by_category"]
        for k, v in sorted(cat.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  - {k}: {v:.2f}")

        lines.append("\nWhy:")
        lines.append(f"  {report['explanation']}")

        return "\n".join(lines)