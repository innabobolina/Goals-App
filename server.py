"""Main server file for the Goals web app"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Goal

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


#########################
# http://0.0.0.0:5000/
#########################
@app.route('/', methods=['GET'])
def index():
    """Homepage showing a log in form."""

    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get login form variables:
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user, please register")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    # flash("Logged in")
    # print("logged in", email)
    return redirect("/goals")
    # return redirect(f"/users/{user.user_id}")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


###############################
# http://0.0.0.0:5000/register
###############################
@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get registration form variables
    email    = request.form["email"]
    password = request.form["password"]
    username = request.form["username"]
    
    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        flash(f"""User {email} already exists. 
            Please log in, you don't need to register! :)""")
        return redirect("/")

    new_user = User(email=email, password=password, username=username)

    # for act_name, act_unit in Activity.DEFAULT_ACTIVITIES:
    #     activity = Activity(act_name=act_name, act_unit=act_unit)
    #     new_user.activities.append(activity)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added. Now please log in.")
    return redirect("/")


###############################
# http://0.0.0.0:5000/goals
###############################
@app.route('/goals', methods=['GET'])
def goal():
    """Page displaying a list of goals."""

    if "user_id" in session:
        user = User.query.get(session["user_id"])

        return render_template("goals.html", user=user)

    return redirect('/')


@app.route('/goals', methods=['POST'])
def get_goal():
    """Add a new goal from the form to the database."""

    user = User.query.get(session["user_id"])

    # Get form variables:
    goal = request.form["goal"]
    number = request.form["number"]

    # Add the new goal to the database:
    new_goal = Goal(goal_content=goal, goal_number=number)
    user.goals.append(new_goal)

    db.session.add(new_goal)
    db.session.commit()

    flash(f"Goal { goal } added.")

    return redirect("/goals")



###########################################
# http://0.0.0.0:5000/delete/<goal_id>
# http://0.0.0.0:5000/delete/1
###########################################
@app.route('/delete/<int:goal_id>', methods=['GET'])
def delete_goal(goal_id):
    """Delete a goal from the database."""    

    del_goal = Goal.query.get(goal_id)
    db.session.delete(del_goal)
    db.session.commit()

    return redirect("/goals")





if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
