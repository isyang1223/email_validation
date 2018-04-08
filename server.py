from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'emails_validation')

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/success')
def success():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails = emails)



@app.route('/email', methods = ["POST"])
def create():
    query = "SELECT * FROM emails WHERE email = :email"
    data = {
             'email': request.form['email'],
           }
    email =mysql.query_db(query, data)
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
    else:
        if len(email) > 0:
            flash("Email already exists")
            return redirect("/")

        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!")
            return redirect("/")
        else:
            query = "INSERT INTO emails (email, created_at) VALUES (:email, NOW())"
            data = {
             'email': request.form['email'],
             
           }
            mysql.query_db(query, data)
            return redirect("/success")

@app.route('/email/<email_id>', methods=['POST'])
def delete(email_id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/success')






    
app.run(debug=True)