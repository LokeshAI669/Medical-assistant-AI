def analyze_symptoms(message: str):
    message = message.lower()

    if "chest pain" in message:
        return {
            "risk": "HIGH",
            "advice": "⚠️ Possible heart issue. Seek immediate medical help."
        }

    elif "fever" in message:
        return {
            "risk": "MEDIUM",
            "advice": "You may have an infection. Monitor temperature and rest."
        }

    elif "headache" in message:
        return {
            "risk": "LOW",
            "advice": "Could be stress or dehydration. Drink water and rest."
        }

    else:
        return {
            "risk": "UNKNOWN",
            "advice": "Please provide more details."
        }