def get_safety_tip(violation):

    tips = {

        "No Helmet":
        "🪖 Always wear ISI-certified helmets to reduce head injury risk.",

        "Triple Riding":
        "🏍️ Triple riding affects vehicle balance and increases accident risk.",

        "Overspeeding":
        "🚗 Follow speed limits to improve reaction time and avoid crashes.",

        "Drunk Driving":
        "🍺 Never drink and drive. Use taxis or designated drivers.",

        "No Seatbelt":
        "🔒 Seatbelts significantly reduce fatal injuries during accidents.",

        "Using Mobile While Driving":
        "📵 Avoid mobile phone usage while driving to prevent distractions."

    }

    return tips.get(
        violation,
        "⚠️ Follow traffic rules and drive safely."
    )