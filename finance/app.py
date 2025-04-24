import os
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime,date

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use POSTGRES database
database_url = os.getenv("DATABASE_URL", "sqlite:///finance.db")
db = SQL(database_url)

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    current_price={}
    response={}
    total={}
    query= db.execute("SELECT userid,symbol,name,quantity FROM holdings WHERE userid=:userid ",userid=session["user_id"])
    cashq= db.execute("SELECT cash FROM users WHERE id=:userid",userid=session["user_id"])
    gtotal=cashq[0]["cash"]
    for j in query:
        total[j["symbol"]] = lookup(j["symbol"])["price"] * int(j["quantity"])
        current_price[j["symbol"]]=lookup(j["symbol"])["price"]
        gtotal=gtotal+total[j["symbol"]]

    return render_template("index.html",gtotal=gtotal,query=query,cash=cashq[0]["cash"],total=total,current_price=current_price)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        capital = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Symbol required")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid quantity")

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol")

        total_price = stock["price"] * int(shares)

        if capital[0]["cash"] < total_price:
            return apology("Insufficient funds")

        today = date.today().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")

        trade = db.execute(
            "INSERT INTO transactions (userid, date, time, symbol, name, price, quantity, total, transaction_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            session["user_id"], today, current_time, symbol, stock["name"], stock["price"], int(shares), total_price, "BUY"
        )

        update = db.execute("UPDATE users SET cash = ? WHERE id = ?", capital[0]["cash"] - total_price, session["user_id"])

        check = db.execute("SELECT symbol FROM holdings WHERE symbol = ? AND userid = ?", symbol, session["user_id"])

        if len(check) < 1:
            db.execute(
                "INSERT INTO holdings (userid, symbol, name, quantity) VALUES (?, ?, ?, ?)",
                session["user_id"], symbol, stock["name"], int(shares)
            )
        else:
            quant = db.execute("SELECT quantity FROM holdings WHERE userid = ? AND symbol = ?", session["user_id"], symbol)
            db.execute(
                "UPDATE holdings SET quantity = ? WHERE symbol = ? AND userid = ?",
                int(quant[0]["quantity"]) + int(shares), symbol, session["user_id"]
            )

        flash("Bought!")
        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    query=db.execute("SELECT * FROM transactions WHERE userid=:userid ORDER BY id DESC",userid=session["user_id"])
    return render_template("history.html",query=query)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.pop("user_id", None)


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if not stock:
            flash("Invalid stock symbol. Please try again.", "danger")
            return render_template("quote.html"), 400  # Return error page

        return render_template("quoted.html", message=f"{stock['symbol']} price is ${stock['price']:.2f}")

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username, password, and confirmation are provided
        if not username or not password or not confirmation:
            flash("All fields are required.", "danger")
            return render_template("register.html"), 400  # Return HTTP 400

        # Ensure password matches confirmation
        if password != confirmation:
            flash("Passwords do not match.", "danger")
            return render_template("register.html"), 400  # Return HTTP 400

        # Check if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            flash("Username already taken. Choose another one.", "danger")
            return render_template("register.html"), 400  # Return HTTP 400

        # Insert new user into database
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Redirect to login page after successful registration
        flash("Registered successfully! Please log in.", "success")
        return redirect("/login")

    # Render registration page for GET requests
    return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure valid input
        if not symbol or not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid symbol or share quantity")

        shares = int(shares)

        # Get user's holdings for the selected stock
        user_id = session["user_id"]
        stock = db.execute("SELECT symbol, name, quantity FROM holdings WHERE userid = ? AND symbol = ?", user_id, symbol)

        if not stock or stock[0]["quantity"] < shares:
            return apology("Not enough shares to sell")

        # Fetch stock price
        stock_data = lookup(symbol)
        if not stock_data:
            return apology("Invalid stock symbol")

        sale_price = stock_data["price"]
        total_sale_value = sale_price * shares

        # Insert transaction into `transactions` table (quantity should be negative for sales)
        db.execute(
            "INSERT INTO transactions (userid, symbol, name, quantity, price, total, transaction_type, date, time) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, DATE('now'), TIME('now'))",
            user_id, symbol, stock_data["name"], -shares, sale_price, total_sale_value, "SELL"
        )

        # Update holdings
        new_quantity = stock[0]["quantity"] - shares
        if new_quantity == 0:
            db.execute("DELETE FROM holdings WHERE userid = ? AND symbol = ?", user_id, symbol)
        else:
            db.execute("UPDATE holdings SET quantity = ? WHERE userid = ? AND symbol = ?", new_quantity, user_id, symbol)

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale_value, user_id)

        flash("Sold successfully!", "success")
        return redirect("/")

    holdings = db.execute("SELECT symbol FROM holdings WHERE userid = ?", session["user_id"])
    return render_template("sell.html", holdings=holdings)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    if request.method == "GET":
        return render_template("addcash.html")
    else:
        amount=request.form.get("amount")
        if amount == None:
            return apology("Invalid input")
        else:
            capital= db.execute("SELECT cash FROM users WHERE id=:userid",userid=session["user_id"])
            update= db.execute("UPDATE users SET cash=:cash WHERE id=:userid ", cash=float(capital[0]["cash"])+float(amount),userid=session["user_id"])
            flash('Cash added sucessfully!')
            return redirect("/")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
