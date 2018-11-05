from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""


    portfolio_symbols = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id",id = session["user_id"])


    total_shares_value = 0


    for portfolio_symbol in portfolio_symbols:
        symbol = portfolio_symbol["symbol"]
        shares = portfolio_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_shares_value += total
        db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id = :id and symbol = :symbol", price = usd(stock["price"]), total = usd(total), id = session["user_id"], symbol = symbol)


    user_cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])

    total_worth = total_shares_value + user_cash[0]["cash"]


    latest_portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id = session["user_id"])
    return render_template("index.html", stocks = latest_portfolio, cash = usd(user_cash[0]["cash"]), total = usd(total_worth))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")

    else:

        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")


        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be a positive integer")
        except:
            return apology("Shares must be a positive integer")


        money = db.execute("SELECT cash FROM users WHERE id= :id",id = session["user_id"])

        if not money or float(money[0]["cash"]) < stock["price"] * shares:
            return apology("Not enough money")


        db.execute("INSERT INTO history (id,symbol, shares, price ) VALUES (:id,:symbol, :shares, :price )", symbol = stock["symbol"], shares = shares, price = usd(stock["price"]), id = session["user_id"])


        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id", id = session["user_id"], purchase = stock["price"] * float(shares))


        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol", id = session["user_id"], symbol = stock["symbol"])


        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES (:name, :shares, :price, :total, :symbol, :id)", name = stock["name"], shares = shares, price = usd(stock["price"]),  total = usd(shares * stock["price"]), symbol = stock["symbol"], id = session["user_id"])


        else:
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol", shares = shares_total, id = session["user_id"], symbol = stock["symbol"])


        return redirect(url_for("index"))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM history WHERE id = :id", id = session["user_id"])

    return render_template("history.html", history=history)

@app.route("/funds/add", methods=["GET", "POST"])
@login_required
def add_funds():

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
        except:
            return apology("amount must be a real number")

        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id", user_id=session["user_id"], amount=amount)

        return redirect(url_for("index"))
    else:
        return render_template("add_funds.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Give possibility for user to change her password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password")


        rows = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])


        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password")


        if not request.form.get("new_password"):
            return apology("must provide new password")


        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation")


        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match")


        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :id", id=session["user_id"], hash=hash)


    return render_template("change_password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # forget any user_id
    session.clear()
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        if not request.form.get("username"):

            return apology("must provide username",400)

        elif not request.form.get("password"):

            return apology("must provide password",400)


        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 1 or not generate_password_hash(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password",400)


        session["user_id"] = rows[0]["id"]


        return redirect(url_for("index"))


    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        if not rows:
            return apology("Invalid Symbol")

        return render_template("quoted.html", stock=rows)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("all the feilds are neccessory!",400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("pasword do not match!",400)

        rows = db.execute("SELECT username FROM users")
        for username in rows:
            if username == request.form.get("username"):

                return apology("User already Registered",400)

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = request.form.get("username"),
        hash = generate_password_hash(request.form.get("password")))
        return render_template("login.html")
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
         return render_template("sell.html")

    else:

        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")


        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be a positive integer")
        except:
            return apology("Shares must be a positive integer")


        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol",  id = session["user_id"], symbol = stock["symbol"])


        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("You don't hold enough shares to sell that quantity")


        db.execute("INSERT INTO history (id,symbol, shares, price ) VALUES (:id,:symbol, :shares, :price )", symbol = stock["symbol"], shares = -shares,  price = usd(stock["price"]), id = session["user_id"])

        # update user cash
        db.execute("UPDATE users SET cash = cash + :sale WHERE id = :id", id = session["user_id"],  sale = stock["price"] * float(shares))


        total_shares = user_shares[0]["shares"] - shares


        if total_shares == 0:
            db.execute("DELETE FROM portfolio WHERE id = :id AND symbol = :symbol", id = session["user_id"], symbol = stock["symbol"])


        else:
            db.execute("UPDATE portfolio SET shares = :shares WHERE id = :id AND symbol = :symbol", shares = total_shares, id = session["user_id"], symbol = stock["symbol"])

        # return to index
        return redirect(url_for("index"))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)