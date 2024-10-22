"""app.py: render and route to webpages"""

from flask import flash, request, render_template, redirect, session, url_for
from sqlalchemy import Engine, insert, text, select

from db.server import app
from db.server import db

from db.schema.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        #raw sql query
        #query = f"""INSERT INTO "Users" ("FirstName", "LastName", "Email", "PhoneNumber", "Password")
        #            VALUES ('{request.form["FirstName"]}',
        #                    '{request.form["LastName"]}',
        #                    '{request.form["Email"]}',
        #                    '{request.form["PhoneNumber"]}',
        #                    '{request.form["Password"]}'
        #                    );"""
        
        query = insert(User).values(request.form)
        
        #application context -temporary environment that holds our application level data
        with app.app_context():
            # execute raw query
            db.session.execute(query)
            # commit changes to the db
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form["Email"]
        password = request.form["Password"]
        if not User.query.filter_by(Email=email).first():
            return render_template('login.html', error="Invalid Email. Try again!")
        else:
            user = User.query.filter_by(Email=email).first()
            if user.Password == password:
                return render_template('index.html')
            else:
                return render_template('login.html', error="Invalid Password. Try again!")
    return render_template('login.html')

@app.route('/users')
def users():
    with app.app_context():
        # select users where the first name is Calista
        # stmt = select(User).where(User.FirstName == "Calista")

        # select all users
        stmt = select(User)
        all_users = db.session.execute(stmt)

        return render_template('users.html', users=all_users)
    
    return render_template('users.html')

if __name__ == "__main__":
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)

