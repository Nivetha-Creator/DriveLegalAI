def simplify_law(rule):

    return f"""
🚦 Violation: {rule['violation']}

📜 Law Section:
{rule['law']}

💰 Fine Amount:
₹{rule['calculated_fine']}

📝 Simple Explanation:
{rule['description']}

✅ Safety Advice:
Following traffic rules helps prevent accidents, protects road users, and avoids legal penalties.
"""