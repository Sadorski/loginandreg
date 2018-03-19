from flask import Flask, redirect, render_template, session, flash, request
from mysqlconnection import MySQLConnector
app = Flask(__name__)
import re, datetime, time, md5
app.secret_key = "penguins"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = MySQLConnector(app, 'logandreg')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def reg():
    print "hello"
    print request.form['action']
    if request.form['action'] == 'register':
        print "hello"
        if len(request.form['first_name']) < 2 or (request.form['first_name'].isalpha()) != True:
            flash("letters only, at least 2 characters and that it was submitted")
            return redirect('/')

        if len(request.form['last_name']) < 2 or (request.form['last_name'].isalpha()) != True:
            flash("Letters only, at least 2 characters and that it was submitted")
            return redirect('/')
       
        if len(request.form['email']) < 1:
            flash("You will need to enter at least one digit for email address")
            return redirect('/')
        elif re.search('[0-9]', request.form['password']) is None:
            flash("your password should include at least one Number")
            return redirect('/')
        elif re.search('[A-Z]', request.form['password']) is None:
            flash("Your password should have one capital letter")
            return redirect('/')
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email address")
            return redirect('/')

        if len(request.form['password']) < 8:
            flash("Your password must be at least 8 characters long")
            return redirect('/')
        elif request.form['password'] != request.form['confirm']:
            flash("Your passwords do not match")
            return redirect('/')

        password = md5.new(request.form['password']).hexdigest()
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(:first, :last, :email, :password, NOW(), NOW())"
        data = {
            "first": request.form['first_name'],
            "last": request.form['last_name'],
            "email": request.form['email'],
            "password": password,
        }
        mysql.query_db(query, data)
        return redirect ('/success')
    elif request.form['action'] == 'login':
        password = md5.new(request.form['password']).hexdigest()
        email = request.form['email']
        query = "SELECT * FROM users where users.email = :email AND users.password = :password"
        data = {
            'email': email,
            'password': password
        }
        user = mysql.query_db(query, data)
        if len(user) > 0:
            return redirect('/success')
        else:
            flash("Your username or password is incorrect")
            return redirect('/')

@app.route('/success')
def success():
    return render_template('success.html')
  
app.run(debug=True)
