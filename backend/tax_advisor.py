def calculate_old_regime_tax(income: float) -> int:
    if income <= 250000:
        tax = 0
    elif income <= 500000:
        tax = (income - 250000) * 0.05
    elif income <= 1000000:
        tax = 12500 + (income - 500000) * 0.20
    else:
        tax = 112500 + (income - 1000000) * 0.30
    tax = tax * 1.04
    return round(tax)


def calculate_tax_savings(annual_salary: float) -> dict:
    standard_deduction = 50000
    income_after_standard = annual_salary - standard_deduction
    tax_without_saving = calculate_old_regime_tax(income_after_standard)

    section_80c = 150000
    income_after_80c = income_after_standard - section_80c
    tax_with_saving = calculate_old_regime_tax(max(0, income_after_80c))

    tax_saved = tax_without_saving - tax_with_saving

    options = [
        {"name": "PPF - Public Provident Fund", "recommended": True},
        {"name": "ELSS Mutual Fund", "recommended": True},
        {"name": "NSC - National Savings Certificate", "recommended": False},
        {"name": "EPF - Employee Provident Fund", "recommended": False},
        {"name": "Life Insurance Premium", "recommended": False}
    ]

    return {
        "annual_salary": round(annual_salary),
        "standard_deduction": standard_deduction,
        "section_80c_limit": 150000,
        "tax_without_saving": tax_without_saving,
        "tax_with_saving": tax_with_saving,
        "tax_saved": tax_saved,
        "options": options
    }


if __name__ == "__main__":
    result = calculate_tax_savings(800000)
    print(result)
