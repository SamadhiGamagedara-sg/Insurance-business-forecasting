def calculate_warning_status(
    premium_growth,
    policy_growth,
    claims_ratio,
    forecast_deviation
):

    score = 0

    # Premium growth
    if premium_growth < -0.10:
        score += 30
    elif premium_growth < -0.05:
        score += 15

    # Policy growth
    if policy_growth < -0.10:
        score += 25
    elif policy_growth < -0.05:
        score += 12

    # Claims ratio
    if claims_ratio > 0.70:
        score += 25
    elif claims_ratio > 0.65:
        score += 12

    # Forecast deviation
    if forecast_deviation < -0.10:
        score += 20
    elif forecast_deviation < -0.05:
        score += 10

    # Overall status
    if score >= 61:
        status = "WARNING"
    elif score >= 31:
        status = "WATCH"
    else:
        status = "NORMAL"

    return score, status
