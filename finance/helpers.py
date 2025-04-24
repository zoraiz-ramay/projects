import os
import requests
import urllib.parse
from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """Escape special characters for memegen."""
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """Ensure user is logged in before accessing certain routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(symbol):
    """Look up quote for symbol using Alpha Vantage"""

    api_key = os.getenv("API_KEY", "R5P7RAQ7VNM7YFBY")  # Use environment variable or fallback key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={urllib.parse.quote_plus(symbol)}&apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure API call is successful
        data = response.json()

        # Check if the response contains valid data
        if "Time Series (Daily)" not in data:
            return None

        # Get the most recent available date
        latest_date = sorted(data["Time Series (Daily)"].keys())[-1]

        # Extract the latest closing price
        closing_price = float(data["Time Series (Daily)"][latest_date]["4. close"])

        return {
            "symbol": symbol.upper(),
            "price": closing_price
        }
    except (requests.RequestException, KeyError, TypeError, ValueError):
        return None  # Return None if API call fails

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

