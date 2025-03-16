from flask import Flask, render_template, url_for, request, redirect
import pymysql as my
import csv
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
   if request.method== 'POST':
       data = request.form.to_dict()
       write_to_db(data)
       send_mail(data)
       return redirect('/thankyou.html')
   else:
       return "Oops! Somthing Went Wrong"
@app.route("/")
def my_home():
    return render_template('index.html')


def write_to_db(data):
    email = data['email']
    subject = data['subject']
    message = data['message']

    try:
        conn = my.connect(host='localhost',user='root',password='2345',charset='utf8mb4')
        cur = conn.cursor()


        cur.execute('CREATE DATABASE IF NOT EXISTS emails')
        cur.execute('USE emails')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS mail (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(50),
                subject VARCHAR(100),
                message VARCHAR(1000)
            )
        ''')
        cur.execute('INSERT INTO mail (email, subject, message) VALUES (%s, %s, %s)', (email, subject, message))
        conn.commit()

    except my.MySQLError as e:
        print(f"Database error: {e}")
        if cur:
            cur.close()
        if conn:
            conn.close()


def send_mail(data):
    email = data['email']
    subject = data['subject']
    message = data['message']

    mail = EmailMessage()
    mail['from'] = 'Joshua Dayal'
    mail['to'] = email
    mail['subject'] = 'Thank you for responding'
    mail.set_content('''Hellooo there,

Thank you for taking the time to reach out to me. I truly appreciate your message and the effort you've made to connect. 
Please know that I’ve received your email and will get back to you as soon as possible with a response :)

Looking forward to connecting further!

Best regards,  
Joshua Dayal
    ''')
    mailr = EmailMessage()
    mailr['from'] = email
    mailr['to'] = 'joshuadayal72@gmail.com'
    mailr['subject'] = subject+email
    mailr.set_content(message)

    # Use SMTP_SSL for secure connections
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        email_address = 'joshuadayal72@gmail.com'
        email_password = 'ljnd dwkn kvka jkrk'  # Use an app password if needed
        smtp.login(email_address, email_password)
        smtp.send_message(mail)
        smtp.send_message(mailr)

        print("Email sent successfully!")


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)
