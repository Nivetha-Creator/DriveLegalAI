import json


def ask_ai(user_question):

    user_question = user_question.lower()

    with open("data/traffic_rules.json", "r") as file:
        rules = json.load(file)

    # Search for matching violations
    for rule in rules:

        violation = rule["violation"].lower()

        if (
            violation in user_question
            or any(
                word in user_question
                for word in violation.split()
            )
        ):

            response = f"""
# 🚦 Traffic Law Information

### 📌 Violation
{rule['violation']}

### 🌍 Country
{rule['country']}

### 📍 State / Region
{rule['state']}

### 🚗 Vehicle Type
{rule['vehicle']}

### 💰 Fine Amount
₹{rule['fine']}

### 📜 Law Section
{rule['law']}

### ⚠️ Why This Rule Exists
{rule['description']}

### ✅ Safety Recommendation
Follow traffic regulations to protect yourself and other road users.
"""

            return response

    # General question handling
    if "helmet" in user_question:
        return """
🪖 Helmet use is mandatory for two-wheeler riders in most regions.

Benefits:
- Reduces head injury risk
- Improves rider safety
- Avoids penalties
"""

    elif "seatbelt" in user_question:
        return """
🔒 Seatbelts are mandatory for drivers and passengers.

Benefits:
- Reduces fatal injuries
- Improves crash survival rates
- Prevents penalties
"""

    elif "drunk" in user_question or "alcohol" in user_question:
        return """
🍺 Drunk driving is a serious traffic offense.

Consequences:
- Heavy fines
- License suspension
- Increased accident risk
"""

    elif "mobile" in user_question:
        return """
📵 Using a mobile phone while driving can distract the driver and increase accident risk.

Use hands-free systems only where permitted by law.
"""

    return """
❌ Sorry, I could not find a matching traffic rule.

Try asking questions like:

• What is the fine for No Helmet?
• Explain Overspeeding rules
• Penalty for Triple Riding
• Fine for Drunk Driving
• Using Mobile While Driving
• Seatbelt violation fine
"""