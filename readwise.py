import csv, random, smtplib
from jinja2 import Template
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Declaring important variables
NO_OF_QUOTES = 2
collection_of_quotes = []
name = "{Your Name}"                              # Change your name
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("GOOGLE_APP_PASSWORD")   # This is the 16 character app password from Google account
receiver_email = os.getenv("RECEIVER_EMAIL")

# Opening the csv file where highlights are stored, and appending all the highlights in the file to a list
with open('highlights.csv', encoding='utf-8') as csvFileObj:
    csvReader = csv.reader(csvFileObj)
    rows = []
    for row in csvReader:
        rows.append(row)

# Appends a certain number of quotes randomly selected from the list of quotes to a list. The quotes are stored as a dictionary containing title, author, and quote
for item in random.sample(rows, NO_OF_QUOTES):
    collection_of_quotes.append({"title": item[1], "author": item[2], "quote": item[4]})

context = {"name": name, "collection": collection_of_quotes, "subject": "Quotes of the day"}

with open("templates\\template.html", 'r') as f:
    template = Template(f.read())

# Generating the HTML file
html_file = template.render(context)

html_message = EmailMessage()
html_message["Subject"] = context['subject']
html_message["From"] = sender_email
html_message["To"] = receiver_email
html_message.add_alternative(html_file, subtype="html")

# Sending the email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, app_password)
    server.send_message(html_message)

exit()
