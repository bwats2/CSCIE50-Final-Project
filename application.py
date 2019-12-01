import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Importing date/time modules
from datetime import datetime
import time

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use my SQLite database
db = SQL("sqlite:///app.db")


@app.route("/")
@login_required
def index():
    return redirect("/write")


@app.route("/updatepassword", methods=["GET", "POST"])
@login_required
def updatepassword():
    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)
        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation must match", 400)
        # ***HASH PASSWORD***
        hash = generate_password_hash(request.form.get("password"))
        # Store new password via update
        db.execute("UPDATE users SET hash=:hash WHERE id=:id", hash=hash, id=session["user_id"])

        # Flash message to user
        flash("You have updated your password!")

        # Redirect user back to about page
        return redirect("/about")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("updatepassword.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Get username
    username = request.args.get("username")

    # Check for username
    if not len(username) or db.execute("SELECT 1 FROM users WHERE username = :username", username=username.lower()):
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/help", methods=["GET", "POST"])
def help():
    # If user isn't logged in
    if session.get("user_id") is None:
        return render_template("help.html")
    # If user logged in, get Support Contact information ready for display
    else:
        sc = db.execute("SELECT scname,scemail FROM supportcontact WHERE userid = :id", id=session["user_id"])
        return render_template("help.html", sc=sc)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    # If "POST"
    if request.method == "POST":
        # If user hasn't supplied information for updating Support Contact
        if not (request.form.get("scname") or request.form.get("scemail")):
            return apology("it doesn't seem like you wish to update your Support Contact information?")
        # Update Support Contact information
        else:
            # https://www.tutorialspoint.com/sqlite/sqlite_update_query.htm
            db.execute("UPDATE supportcontact SET scname=:scname, scemail=:scemail WHERE userid = :id",
                       scname=request.form.get("scname"), scemail=request.form.get("scemail"), id=session["user_id"])
            flash("Support Contact info has been updated!")
            return redirect("/help")
    # If "GET"
    else:
        # Need them to include the update info.
        return render_template("/update.html")


@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        # In case they are REALLY not doing well, if the lowest value is selected, it seamlessly redirects them to the help page
        if request.form.get("score") is '1':
            return render_template("help.html")
        # To make sure that the user writes something in their entry
        if not (request.form.get("content1") or request.form.get("content2") or request.form.get("content3") or request.form.get("content4") or request.form.get("content5")):
            return apology("please write something first!")
        # Trying to fix the time issue with SQL store/retrieve which is UTC, Tom said to try Python
        # https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python
        # https://stackoverflow.com/questions/4530069/python-how-to-get-a-value-of-datetime-today-that-is-timezone-aware
        # time2 is storing localtime, time3 is storing epoch time (this is a standard), time1 was sql utc auto timestamp
        else:
            db.execute("INSERT INTO journal (userid,score,content1,content2,content3,content4,content5,time2,time3) VALUES(:userid, :score, :content1, :content2, :content3, :content4, :content5, :time2, :time3)",
                       userid=session["user_id"], score=request.form.get("score"), content1=request.form.get("content1"), content2=request.form.get("content2"), content3=request.form.get("content3"), content4=request.form.get("content4"), content5=request.form.get("content5"), time2=datetime.now().strftime("%Y-%m-%d %I:%M %p"), time3=time.time())
            flash("Journal entry saved!")
            return redirect("/read")
    # If "GET"
    else:
        # Need them write a post! So we reload page.
        return render_template("/index.html")


@app.route("/selectread", methods=["GET", "POST"])
@login_required
def selectread():
    return redirect("/read")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        choice = request.form.get("delete")
        # If user has selected yes to deletion
        if choice == 'yes':
            # Delete Support Contact
            db.execute("DELETE FROM supportcontact WHERE userid = :id", id=session["user_id"])
            # Delete Journal Entries
            db.execute("DELETE FROM journal WHERE userid = :id", id=session["user_id"])
            # LASTLY, delete User Account
            db.execute("DELETE FROM users WHERE id = :id", id=session["user_id"])
            # Forget user_id
            session.clear()
            # Flash message of successful deletion, and redirect to registration page
            flash("Your account and all your data has been deleted.")
            return redirect("/register")
        # If user has selected no
        else:
            return redirect("/about")
    # If "GET"
    else:
        # Need them to make a selection! So we reload page.
        return render_template("/delete.html")


@app.route("/read", methods=["GET", "POST"])
@login_required
def read():
    # If "POST"
    if request.method == "POST":
        # Pulls all information from journal database, passed to template for display
        contentselected = db.execute("SELECT score,time2,content1,content2,content3,content4,content5 FROM journal WHERE (userid = :id AND time2 = :time2)",
                                     id=session["user_id"], time2=request.form.get("time"))
        return render_template("/selectread.html", contentselected=contentselected)
    # If "GET"
    else:
        # Queue up the datetimes from user posts, so they can select a post to display
        dateoptions = db.execute("SELECT time2 FROM journal WHERE userid = :id ORDER BY time3 DESC", id=session["user_id"])
        # If user hasn't written anything yet, no need to redirect to selection since nothing to select
        if not dateoptions:
            # If user hasn't written anything yet, flash message and stay on write page (which is homepage)
            flash("You haven't written anything yet!")
            return redirect("/")
        else:
            return render_template("/read.html", dateoptions=dateoptions)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Let user know they've logged in
        flash("You have logged in!")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    # Copied/adapted from Login, per spec sheet
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Ensure password and confirmation match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password and confirmation must match", 400)

        # ***HASH PASSWORD***
        hash = generate_password_hash(request.form.get("password"))

        # ***CHECK USERNAME DOES NOT EXISTS while ALSO Storing USER!***
        # Query database for username
        # From Ballatore Section Video
        # https://stackoverflow.com/questions/4205181/insert-into-a-mysql-table-or-update-if-exists
        # Does not overwrite, therefore we can use it to check if username exists!
        result = db.execute("INSERT INTO users (username,hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("username already taken", 400)

        # Remember which user has logged in
        # Or equals result? Since if doesn't exist will be stored in result
        session["user_id"] = result

        db.execute("INSERT INTO supportcontact (userid,scname,scemail) VALUES (:userid, :scname, :scemail)",
                   userid=session["user_id"], scname=request.form.get("scname"), scemail=request.form.get("scemail"))

        # Let user know they're registered (Staff Solution to Pset8)
        flash("You have registered your account!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)