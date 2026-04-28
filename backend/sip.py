def calculate_sip(monthly_amount: float, years: int, annual_return: float = 12.0) -> dict:
    # Step 1 — Validate inputs
    if monthly_amount <= 0 or years <= 0:
        return {
            "final_amount": 0,
            "total_invested": 0,
            "wealth_created": 0,
            "yearly_growth": {"labels": [], "values": []}
        }

    # Step 2 — Set the monthly rate
    monthly_rate = annual_return / 100 / 12

    # Step 3 — Create two empty lists
    labels = []
    values = []

    # Step 4 — Loop from year 1 to years (inclusive)
    for year in range(1, years + 1):
        n = year * 12
        value = monthly_amount * (((1 + monthly_rate) ** n - 1) / monthly_rate) * (1 + monthly_rate)
        value = round(value)
        labels.append(year)
        values.append(value)

    # Step 5 — Calculate final results
    final_amount = values[-1]
    total_invested = round(monthly_amount * 12 * years)
    wealth_created = final_amount - total_invested

    # Step 6 — Return the result dictionary
    return {
        "final_amount": final_amount,
        "total_invested": total_invested,
        "wealth_created": wealth_created,
        "yearly_growth": {
            "labels": labels,
            "values": values
        }
    }


# Step 7 — Test block
if __name__ == "__main__":
    print("--- 12% return ---")
    print(calculate_sip(5000, 5, 12.0))
    print("--- 8% return ---")
    print(calculate_sip(5000, 5, 8.0))
    print("--- 15% return ---")
    print(calculate_sip(5000, 5, 15.0))
