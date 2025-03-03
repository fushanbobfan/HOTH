import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
import random as random 
from lunardate import LunarDate
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from datetime import datetime
import pytz

df = pd.read_csv("quotes.csv")
quotes = df["quote"].dropna().tolist()
app = Flask(__name__)
CORS(app) 

@app.route('/random_quote', methods=['GET'])
def get_random_quote():
    quote = random.choice(quotes)
    return jsonify({"quote": quote})

def generate_tung_shing(lunar_month, lunar_day):
    """Dynamically generate Tung Shing data"""
    auspicious_activities = ["Worship", "Business Opening", "Marriage", "Travel", "Signing Contracts"]
    inauspicious_activities = ["Funeral", "Lawsuit", "Construction", "Investment"]

    return {
        "good_to_do": [auspicious_activities[(lunar_month + lunar_day) % len(auspicious_activities)]],
        "bad_to_do": [inauspicious_activities[(lunar_month * lunar_day) % len(inauspicious_activities)]]
    }

@app.route('/tungshing/<date>', methods=['GET'])
def get_tungshing(date):
    """Fetches Tung Shing data for a given date."""
    try:
        year, month, day = map(int, date.split("-"))
        lunar_date = LunarDate.fromSolarDate(year, month, day)
        daily_data = generate_tung_shing(lunar_date.month, lunar_date.day)

        return jsonify({
            "date": date,
            "lunar_date": f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}",
            "auspicious": daily_data.get("good_to_do"),
            "inauspicious": daily_data.get("bad_to_do")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Astrology Functions
def get_monthly_influence(month):
    monthly_influences = {
        1: "Focus on new beginnings and setting goals",
        2: "Nurture relationships and practice self-love",
        3: "Embrace change and new opportunities",
        4: "Work on stability and grounding yourself",
        5: "Express yourself creatively and communicate openly",
        6: "Focus on home and family matters",
        7: "Pursue personal passions and enjoy leisure activities",
        8: "Transform and let go of what no longer serves you",
        9: "Expand your knowledge and explore new horizons",
        10: "Work on achieving balance in all areas of life",
        11: "Connect with others and contribute to your community",
        12: "Reflect on the past year and prepare for the new one"
    }
    return monthly_influences.get(month, "Embrace the energy of the current month")


@app.route('/api/monthly_influence', methods=['POST'])
def get_monthly_influence_method(month):
    monthly_influences = {
        1: "Focus on new beginnings and setting goals",
        2: "Nurture relationships and practice self-love",
        3: "Embrace change and new opportunities",
        4: "Work on stability and grounding yourself",
        5: "Express yourself creatively and communicate openly",
        6: "Focus on home and family matters",
        7: "Pursue personal passions and enjoy leisure activities",
        8: "Transform and let go of what no longer serves you",
        9: "Expand your knowledge and explore new horizons",
        10: "Work on achieving balance in all areas of life",
        11: "Connect with others and contribute to your community",
        12: "Reflect on the past year and prepare for the new one"
    }
    return monthly_influences.get(month, "Embrace the energy of the current month")

def get_current_fortune(name="Eileen", selected_datetime=None, city="California", country="US"):
    """
    Generate astrological influences based on a given date & time.
    If no time is provided, it defaults to the current time.
    """
    try:
        # Use selected time or default to current UTC time
        if selected_datetime is None:
            selected_datetime = datetime.now(pytz.utc)
        else:
            selected_datetime = selected_datetime.astimezone(pytz.utc)  # Ensure it's in UTC
            selected_datetime = selected_datetime.replace(hour=12, minute=0)

        day_of_week = selected_datetime.weekday()  # Monday = 0, Sunday = 6
        month = selected_datetime.month

        #  astrological subject
        subject = AstrologicalSubject(
            name, 
            selected_datetime.year, 
            selected_datetime.month, 
            selected_datetime.day, 
            selected_datetime.hour,
            selected_datetime.minute,
            city=city,
            country=country
        )

        # ✅ Generate Birth Chart SVG
        birth_chart_svg = KerykeionChartSVG(subject)
        svg_path = f"/Users/eileen/{name.replace(' ', '_')}_chart.svg"
        birth_chart_svg.makeSVG(svg_path)

        # ✅ Extract Astrological Details
        sun_info = subject.sun
        moon_info = subject.moon
        sun_house = sun_info.house
        moon_house = moon_info.house
        sun_sign = sun_info.sign
        moon_element = moon_info.element

        # ✅ Generate SUGGESTIONS
        suggestions = []

        # 🌞 Sun Sign Influence
        if sun_sign in ['Ari', 'Leo', 'Sgr']:
            suggestions.append("Today is a great day for physical activity and leadership.")
        elif sun_sign in ['Tau', 'Vir', 'Cap']:
            suggestions.append("Focus on stability, financial planning, or self-care today.")
        elif sun_sign in ['Gem', 'Lib', 'Aqr']:
            suggestions.append("Engage in social activities, networking, or brainstorming ideas.")
        else:
            suggestions.append("A perfect day to reflect, meditate, and focus on emotions.")

        # 🌙 Moon Phase Influence
        if moon_element == "Water":
            suggestions.append("Pay attention to your emotions, today is a time for deep reflection.")
        elif moon_element == "Fire":
            suggestions.append("Take action, trust your instincts, and express yourself boldly.")
        elif moon_element == "Earth":
            suggestions.append("Stay grounded, focus on practical matters, and find stability.")
        elif moon_element == "Air":
            suggestions.append("Communicate your thoughts, socialize, and be intellectually curious.")
        """
        # ⏳ Hourly Influence
        if 5 <= hour < 12:
            suggestions.append("Focus on important tasks requiring concentration.")
        elif 12 <= hour < 17:
            suggestions.append("Collaborate with others or attend meetings.")
        elif 17 <= hour < 22:
            suggestions.append("Engage in leisure activities or personal hobbies.")
        else:
            suggestions.append("Prioritize rest and relaxation.")
        """
        # 📅 Weekly Influence
        if day_of_week == 0:  # Monday
            suggestions.append("Set goals for the week.")
        elif day_of_week == 2:  # Wednesday
            suggestions.append("Network or communicate important ideas.")
        elif day_of_week == 4:  # Friday
            suggestions.append("Socialize or plan weekend activities.")

        # 📆 Monthly Influence
        suggestions.append(get_monthly_influence(month))

        # 🏠 House Placements
        if sun_house == "10th House":
            suggestions.append("Focus on career advancement.")
        if moon_house == "4th House":
            suggestions.append("Spend time at home or with family.")

        return {
            "selected_time": selected_datetime.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "suggestions": suggestions,
            "chart_svg": svg_path
        }
    except Exception as e:
        return {"error": str(e)}
# Test the function
if __name__ == "__main__":
    app.run(debug=True)




