import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")






@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transkasiyons WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",session["user_id"])

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]


    total_value = cash
    grand_total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock["price"] * stock["total_shares"]
        total_value += stock["value"]
        grand_total += stock["value"]


    return render_template("index.html", stocks = stocks, cash = usd(cash), total_value = usd(total_value), grand_total = grand_total)












@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:

        stock_searched = request.form.get("symbol").upper()
        num_of_stocks = request.form.get("shares")

        if not num_of_stocks and not stock_searched:
            return apology("please enter something😭", 403)


        if lookup(stock_searched) == None:
            return apology("stock not found", 400)

        elif not num_of_stocks:
            return apology("please enter the quantity of stock", 400)

        elif not num_of_stocks.isdigit():
            return apology("please enter a whole number", 400)

        elif int(num_of_stocks) < 0:
            return apology("please enter a positive whole number", 400)

        elif not stock_searched:
            return apology("stock symbol not entered", 403)


        stock_price = lookup(stock_searched)["price"]
        user_cash_from_db = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        user_cash = user_cash_from_db[0]["cash"]
        total_price = int(num_of_stocks) * stock_price
        username_from_db = db.execute("SELECT username FROM users where id = ?", session["user_id"])
        username = username_from_db[0]["username"]

        balance = user_cash - total_price

        if balance < 0:
            return apology("insufficient balance", 402)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance, session["user_id"])

        db.execute("INSERT INTO transkasiyons (user_id, symbol, shares, price) VALUES (?,?,?,?)", session["user_id"], stock_searched, int(num_of_stocks), stock_price)


        flash(f"Bought {num_of_stocks} shares of {stock_searched} costing {usd(total_price)}!")




        return redirect("/")




@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transkasiyons = db.execute("SELECT * FROM transkasiyons WHERE user_id = :user_id ORDER BY timestamp DESC", user_id = session["user_id"])

    return render_template("history.html", transkasiyons = transkasiyons)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)
        else:
            return render_template("quote.html", quote = quote)


















@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()


    if request.method == "GET":
        return render_template("register.html")

    else:

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must type in the confirmation", 400)


        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match with confirmation", 400)

        elif len(db.execute("SELECT * from users WHERE username = ?", request.form.get("username"))) != 0:
            return apology("username is already taken", 400)


        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))[0]["id"]


        return redirect("/")






















@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    stocks = db.execute("SELECT symbol, SUM(shares) AS total_shares FROM transkasiyons WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        if not symbol:
            return apology("Please enter stock", 400)

        elif not shares:
            return apology("Please enter the amount of shares", 400)

        elif not shares.isdigit():
            return apology("The amount of shares must be a whole number", 403)

        elif int(shares) <= 0:
            return apology("The amount of shares cannot be negative or zero", 403)

        else:
            shares = int(shares)

        for stock in stocks:

            if stock["symbol"] == symbol.upper():

                if stock["total_shares"] < shares:

                    return apology("Not enough shares", 400)
                else:

                    quote = lookup(symbol)
                    if quote is None:

                        return apology("Symbol not found", 404)

                    price = quote["price"]
                    total_sale = shares * price

                    db.execute("UPDATE users SET cash = cash + :total_sale WHERE id = :user_id", total_sale  = total_sale, user_id = session["user_id"])

                    db.execute("INSERT INTO transkasiyons (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id = session["user_id"], symbol = symbol, shares = -shares, price = price)



                    flash(f"Sold {shares} share(s) of {symbol} for {usd(total_sale)}!")

                    return redirect("/")


        return apology("Stock not found", 404)


    else:
        return render_template("sell.html", stocks = stocks)
