import bcrypt 
from app import db, login_manager
from flask_login import UserMixin
from flask import flash, redirect, session, url_for

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Add the 'rank' attribute with a default value of 3 (customer)
    rank = db.Column(db.Integer, default=3)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_admin(self):
        # Check if the current user is authenticated and has admin rank (rank = 1)
        return self.is_authenticated and self.rank == 1
    
    def __repr__(self):
        return f"{self.username}, {self.email}, {self.password}, {self.id}"

####################################################################################################
# Create the default admin user (you can modify this data as needed)
def create_default_admin():
    username = 'admin'
    # You can use the bcrypt library to hash the password here if desired
    password = 'admin'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    rank = 1  # Admin rank is 1
    # Check if the admin user already exists in the database
    admin_user = User.query.filter_by(username=username).first()
    if admin_user is None:
        # If the admin user doesn't exist, create it
        admin_user = User(username=username,
                          password_hash=hashed_password, rank=rank)
        db.session.add(admin_user)
        db.session.commit()
