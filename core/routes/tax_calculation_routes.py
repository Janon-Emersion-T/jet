import re

from tools.tax_calculation_tools import tax_calculation_helper, calculate_tax


def handle_tax_calculation_routes(user_input: str, text: str, clean_text: str):
    if text in ["tax calculation helper", "tax helper", "345 help", "phase 345 help"]:
        return tax_calculation_helper()

    match = re.match(r"tax\s+([0-9,.]+)\s+at\s+([0-9.]+)", text)
    if match:
        return calculate_tax(match.group(1), match.group(2), inclusive=False)

    match = re.match(r"tax\s+exclusive\s+([0-9,.]+)\s+at\s+([0-9.]+)", text)
    if match:
        return calculate_tax(match.group(1), match.group(2), inclusive=False)

    match = re.match(r"tax\s+inclusive\s+([0-9,.]+)\s+at\s+([0-9.]+)", text)
    if match:
        return calculate_tax(match.group(1), match.group(2), inclusive=True)

    return None
