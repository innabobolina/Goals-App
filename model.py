"""Models and database functions for Goals app."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User on Goals website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        """Provide helpful representation of user when printed."""

        return f"""\n<User       user_id={self.user_id} 
            username={self.username}
            email={self.email}>"""


class Goal(db.Model):
    """Goal (one user has many goals, each goal belongs to a user)."""

    __tablename__ = "goals"


    goal_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    goal_number = db.Column(db.Integer, nullable=True)
    goal_content = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("goals",
                                              order_by=goal_number))

    def __repr__(self):
        """Provide helpful representation of a goal when printed."""

        return f"""\n<Goal   goal_id={self.goal_id} 
            goal_number={self.goal_number}
            goal_content={self.goal_content}
            user_id={self.user_id}>"""



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///goals'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")