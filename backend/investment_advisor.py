def get_investment_advice(amount: float, language: str = "english") -> dict:

    # Step 1 — Validation
    if amount < 500:
        return {"error": "Minimum ₹500 required"}
    if amount > 10000000:
        return {"error": "Amount too large, consult expert"}

    # Step 2 — Risk profile
    if amount < 5000:
        risk = "conservative"
    elif amount < 50000:
        risk = "moderate"
    else:
        risk = "growth"

    # Step 3 — Allocation
    if risk == "conservative":
        allocation = [
            {"category": "Savings Account", "percentage": 60},
            {"category": "Fixed Deposit", "percentage": 40}
        ]
    elif risk == "moderate":
        allocation = [
            {"category": "Fixed Deposit", "percentage": 40},
            {"category": "Mutual Fund SIP", "percentage": 40},
            {"category": "Digital Gold", "percentage": 20}
        ]
    else:
        allocation = [
            {"category": "Mutual Fund SIP", "percentage": 50},
            {"category": "Fixed Deposit", "percentage": 20},
            {"category": "PPF Account", "percentage": 20},
            {"category": "Digital Gold", "percentage": 10}
        ]

    # Step 4 — Calculate amounts (single source of truth)
    remaining = amount
    for i, item in enumerate(allocation):
        if i == len(allocation) - 1:
            item["amount"] = round(remaining)
        else:
            value = round(amount * item["percentage"] / 100)
            item["amount"] = value
            remaining -= value

    # Step 5 — Add reasons + actions (NO recalculation)
    info = {
        "Savings Account": {
            "reason": "Emergency use ke liye",
            "action": "SBI ya HDFC savings account use karo"
        },
        "Fixed Deposit": {
            "reason": "Safe returns",
            "action": "Bank mein FD kholo"
        },
        "Mutual Fund SIP": {
            "reason": "Long term growth",
            "action": "Groww pe SIP start karo"
        },
        "Digital Gold": {
            "reason": "Inflation protection",
            "action": "Paytm ya GPay se gold lo"
        },
        "PPF Account": {
            "reason": "Tax saving + safe",
            "action": "PPF account open karo"
        }
    }

    for item in allocation:
        item["reason"] = info[item["category"]]["reason"]
        item["action"] = info[item["category"]]["action"]

    # Step 6 — Action steps
    if language == "hinglish":
        if risk == "conservative":
            action_steps = [
                "SBI ya HDFC mein savings account kholo",
                f"Rs {round(amount * 0.6)} emergency fund rakho — kabhi bhi nikal sako",
                f"Rs {round(amount * 0.4)} ki 1 saal ki FD kholo bank mein"
            ]
            summary = "Pehle safe raho — baad mein invest karo."
        elif risk == "moderate":
            action_steps = [
                "Aaj Groww app download karo — free hai",
                f"Rs {round(amount * 0.4)} ki SIP start karo Nifty 50 Index Fund mein",
                f"Rs {round(amount * 0.4)} ki FD kholo SBI ya HDFC mein",
                f"Rs {round(amount * 0.2)} ka digital gold lo Paytm se"
            ]
            summary = "Safe bhi hai aur grow bhi karega — balanced plan hai."
        else:
            action_steps = [
                "Groww ya Zerodha pe account kholo",
                f"Rs {round(amount * 0.5)} Nifty 50 Index Fund mein lagao",
                f"Rs {round(amount * 0.2)} ki FD kholo",
                f"Rs {round(amount * 0.2)} PPF mein daalo — tax bhi bachega",
                f"Rs {round(amount * 0.1)} digital gold mein"
            ]
            summary = "Tumhara amount grow karne ke liye ready hai."
    else:
        if risk == "conservative":
            action_steps = [
                "Open a savings account in SBI or HDFC",
                f"Keep Rs {round(amount * 0.6)} as emergency fund",
                f"Open a 1-year FD for Rs {round(amount * 0.4)}"
            ]
            summary = "Stay safe first — invest more as your savings grow."
        elif risk == "moderate":
            action_steps = [
                "Download Groww app — it is free",
                f"Start SIP of Rs {round(amount * 0.4)} in Nifty 50 Index Fund",
                f"Open FD for Rs {round(amount * 0.4)} in SBI or HDFC",
                f"Buy Rs {round(amount * 0.2)} digital gold via Paytm"
            ]
            summary = "This plan gives you safety and growth together."
        else:
            action_steps = [
                "Open account on Groww or Zerodha",
                f"Invest Rs {round(amount * 0.5)} in Nifty 50 Index Fund",
                f"Open FD for Rs {round(amount * 0.2)} in SBI",
                f"Put Rs {round(amount * 0.2)} in PPF — saves tax too",
                f"Buy Rs {round(amount * 0.1)} digital gold via Paytm"
            ]
            summary = "Your money is ready to grow — follow these steps."

    # Step 7 — Return
    return {
        "amount": round(amount),
        "risk_level": risk,
        "allocation": allocation,
        "action_steps": action_steps,
        "summary": summary
    }


if __name__ == "__main__":
    print("--- Conservative (₹2000) ---")
    print(get_investment_advice(2000))
    print()
    print("--- Moderate (₹20000) ---")
    print(get_investment_advice(20000))
    print()
    print("--- Growth (₹100000) ---")
    print(get_investment_advice(100000))
    print()
    print("--- Hinglish (₹20000) ---")
    print(get_investment_advice(20000, "hinglish"))
