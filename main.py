from invisible_cost import CostItem, Scenario, Calculator, ReportFormatter


def build_scenarios():
    fast_fashion = Scenario(
        name="Fast Fashion T Shirt",
        visible_price=8.99,
        description="A low price tee bought impulsively, replaced often."
    )
    fast_fashion.add_item(CostItem("labor", "workers", 5, 0.8, "Low wages and unsafe conditions are more likely in cost-cutting supply chains."))
    fast_fashion.add_item(CostItem("environment", "public", 4, 0.7, "Dyeing and finishing can pollute waterways when standards are weak or unenforced."))
    fast_fashion.add_item(CostItem("waste", "future generations", 4, 0.6, "Short lifespans increase landfill burden and long-term cleanup costs."))
    fast_fashion.add_item(CostItem("health", "workers", 3, 0.6, "Chemical exposure risks rise with poor protective equipment and oversight."))
    fast_fashion.add_item(CostItem("community", "public", 2, 0.5, "Local manufacturing ecosystems lose resilience when production offshores to the cheapest option."))

    cheap_fast_food = Scenario(
        name="Cheap Fast Food Meal",
        visible_price=6.49,
        description="A quick meal optimized for price and convenience."
    )
    cheap_fast_food.add_item(CostItem("health", "consumer", 4, 0.7, "High sodium and ultra-processed ingredients can increase long-term health risk."))
    cheap_fast_food.add_item(CostItem("labor", "workers", 3, 0.7, "Low-margin operations can pressure wages, scheduling stability, and working conditions."))
    cheap_fast_food.add_item(CostItem("environment", "public", 3, 0.6, "Packaging and supply chains increase emissions and waste."))
    cheap_fast_food.add_item(CostItem("time", "consumer", 2, 0.6, "Convenience can become a habit that displaces cooking skills and planning."))
    cheap_fast_food.add_item(CostItem("public_budget", "public", 3, 0.5, "Long-run health impacts can shift costs into shared systems."))

    free_social = Scenario(
        name="Free Social Media App",
        visible_price=0.00,
        description="A free platform paid for by attention, data, and incentives."
    )
    free_social.add_item(CostItem("privacy", "consumer", 5, 0.8, "Personal data can be collected and used for targeting, profiling, and inference."))
    free_social.add_item(CostItem("time", "consumer", 4, 0.8, "Engagement optimization can pull time away from goals and relationships."))
    free_social.add_item(CostItem("mental_health", "consumer", 4, 0.6, "Comparison loops and outrage cycles can increase stress and anxiety for some users."))
    free_social.add_item(CostItem("democracy", "public", 3, 0.5, "Incentives can reward misinformation and polarization in certain environments."))
    free_social.add_item(CostItem("labor", "workers", 3, 0.5, "Content moderation and creator labor can be undercompensated relative to value created."))

    return [fast_fashion, cheap_fast_food, free_social]


def main():
    scenarios = build_scenarios()
    calc = Calculator(max_items_for_scaling=10)

    for s in scenarios:
        report = calc.evaluate(s)
        print(ReportFormatter.to_terminal(report))

    # Optional compare demo
    print("\n\nCOMPARE DEMO")
    a, b = scenarios[0], scenarios[2]
    comp = calc.compare(a, b)
    print(f"Lower hidden cost (0–100): {comp['lower_hidden_cost']}")


if __name__ == "__main__":
    main()