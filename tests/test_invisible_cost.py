from invisible_cost import CostItem, Scenario, Calculator


def test_costitem_weighted_impact():
    item = CostItem("labor", "workers", 4, 0.5, "test")
    assert item.weighted_impact() == 2.0


def test_scenario_add_item_increases_count():
    s = Scenario("Test", 1.0)
    assert len(s.items) == 0
    s.add_item(CostItem("privacy", "consumer", 3, 0.7, "test"))
    assert len(s.items) == 1


def test_hidden_score_increases_with_higher_impact():
    s = Scenario("Test", 1.0)
    calc = Calculator(max_items_for_scaling=10)

    s.add_item(CostItem("labor", "workers", 1, 0.1, "low"))
    low = calc.evaluate(s)["hidden_score"]

    s.add_item(CostItem("labor", "workers", 5, 1.0, "high"))
    high = calc.evaluate(s)["hidden_score"]

    assert high > low