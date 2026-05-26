def tax_calculation_helper():
    return """TAX CALCULATION HELPER — PHASE 345

Mode: read-only tax helper.

Supported examples:
- tax 1000 at 18
- tax inclusive 1180 at 18
- tax exclusive 1000 at 18

Notes:
- This is a calculation helper, not certified tax advice.
- No files are modified.
"""


def calculate_tax(amount_text: str, rate_text: str, inclusive: bool = False):
    try:
        amount = float(amount_text.replace(",", "").strip())
        rate = float(rate_text.replace("%", "").strip())
    except ValueError:
        return "Invalid amount or tax rate."

    if amount < 0 or rate < 0:
        return "Amount and tax rate must be positive."

    if inclusive:
        base = amount / (1 + rate / 100)
        tax = amount - base
        total = amount
    else:
        base = amount
        tax = amount * (rate / 100)
        total = base + tax

    return f"""TAX CALCULATION HELPER — PHASE 345

Mode: read-only calculation.

Amount entered: {amount:,.2f}
Tax rate: {rate:.2f}%

Base amount: {base:,.2f}
Tax amount: {tax:,.2f}
Total amount: {total:,.2f}

Important:
- This is a helper calculation only.
- Confirm official tax rules before filing or invoicing.
"""
