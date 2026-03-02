# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.

    Updated to use the SQLAlchemy ORM by Nick Farnan
"""

import time
import os
from hashlib import md5
from datetime import datetime
from flask import (
    Flask,
    request,
    session,
    url_for,
    redirect,
    render_template,
    abort,
    g,
    flash,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import db, User, Message

# Create the application
app = Flask(__name__)

# Configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = "development key"

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(app.root_path, "minitwit.db")

app.config.from_object(__name__)
app.config.from_envvar("MINITWIT_SETTINGS", silent=True)

db.init_app(app)


@app.cli.command("initdb")
def initdb_command():
    """Creates the database tables."""
    db.create_all()
    print("Initialized the database.")


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = db.session.execute(db.select(User).where(User.username == username)).scalar()
    return rv.user_id if rv else None


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d @ %H:%M")


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return "http://www.gravatar.com/avatar/%s?d=identicon&s=%d" % (
        md5(email.strip().lower().encode("utf-8")).hexdigest(),
        size,
    )


@app.before_request
def before_request():
    g.user = None
    if "user_id" in session:
        g.user = db.session.execute(db.select(User).where(User.user_id == session["user_id"])).scalar()


@app.route("/")
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if not g.user:
        return redirect(url_for("public_timeline"))

    timeline_ids = [g.user.user_id]
    for f in g.user.follows:
        timeline_ids.append(f.user_id)
    messages = (
        Message.query.filter(Message.author_id.in_(timeline_ids))
        .order_by(Message.pub_date.desc())
        .limit(PER_PAGE)
        .all()
    )
    return render_template("timeline.html", messages=messages)


@app.route("/public")
def public_timeline():
    """Displays the latest messages of all users."""
    return render_template(
        "timeline.html",
        messages=Message.query.order_by(Message.pub_date.desc()).limit(PER_PAGE).all(),
    )


@app.route("/<username>")
def user_timeline(username):
    """Display's a users tweets."""
    profile_user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        followed = sum(1 for other in g.user.follows if other.user_id == profile_user.user_id) > 0

    msgs = list(db.session.execute(
        db.select(Message)
            .where(Message.author_id == profile_user.user_id)
            .order_by(Message.pub_date.desc())
            .limit(PER_PAGE)
    ).scalars())
    return render_template(
        "timeline.html", messages=msgs, followed=followed, profile_user=profile_user
    )


@app.route("/<username>/follow")
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)
    followee_id = get_user_id(username)
    if followee_id is None:
        abort(404)

    followee = db.session.execute(db.select(User).where(User.user_id == followee_id)).scalar()
    g.user.follows.append(followee)
    db.session.commit()

    flash("You are now following '%s'" % username)
    return redirect(url_for("user_timeline", username=username))


@app.route("/<username>/unfollow")
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)
    followee_id = get_user_id(username)
    if followee_id is None:
        abort(404)

    followee = db.session.execute(db.select(User).where(User.user_id == followee_id)).scalar()
    g.user.follows.remove(followee)
    db.session.commit()

    flash("You are no longer following '%s'" % username)
    return redirect(url_for("user_timeline", username=username))


@app.route("/add_message", methods=["POST"])
def add_message():
    """Registers a new message for the user."""
    if "user_id" not in session:
        abort(401)
    if request.form["text"]:
        db.session.add(
            Message(session["user_id"], request.form["text"], int(time.time()))
        )
        db.session.commit()

        flash("Your message was recorded")
    return redirect(url_for("timeline"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for("timeline"))
    error = None
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.username == request.form["username"])).scalar()
        # Why not check both individually?
        if user is None or not check_password_hash(user.pw_hash, request.form["password"]):
            error = "Invalid username/password combination"
        else:
            flash("You were logged in")
            session["user_id"] = user.user_id
            return redirect(url_for("timeline"))
    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for("timeline"))
    error = None
    if request.method == "POST":
        if not request.form["username"]:
            error = "You have to enter a username"
        elif not request.form["email"] or "@" not in request.form["email"]:
            error = "You have to enter a valid email address"
        elif not request.form["password"]:
            error = "You have to enter a password"
        elif request.form["password"] != request.form["password2"]:
            error = "The two passwords do not match"
        elif get_user_id(request.form["username"]) is not None:
            error = "The username is already taken"
        else:
            db.session.add(
                User(
                    request.form["username"],
                    request.form["email"],
                    generate_password_hash(request.form["password"]),
                )
            )
            db.session.commit()
            flash("You were successfully registered and can login now")
            return redirect(url_for("login"))
    return render_template("register.html", error=error)


@app.route("/logout")
def logout():
    """Logs the user out."""
    flash("You were logged out")
    session.pop("user_id", None)
    return redirect(url_for("public_timeline"))


# Add some filters to jinja
app.jinja_env.filters["datetimeformat"] = format_datetime
app.jinja_env.filters["gravatar"] = gravatar_url
