def validate_weights(portfolio: dict) -> bool:
    portfolio_objects = portfolio.values()
    weights = [float(p.weight) for p in portfolio_objects]
    total_weight = sum(weights)
    return total_weight == 1
