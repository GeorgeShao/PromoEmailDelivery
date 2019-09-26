from string import Template
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

USERNAME = ""
PASSWORD = ""

# Reads contacts from contacts.txt & returns names & emails
def get_contacts():
    names = []
    emails = []
    with open("contacts.txt", mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    return names, emails


# Reads template from message.txt & returns template object
def read_template():
    with open("message.txt", mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# Setup SMTP (Simple Mail Transfer Protocol) server
def setup_server():
    with open("CREDIDENTIALS.json", mode='r', encoding='utf-8') as credidentials_file:
        data = json.load(credidentials_file)
        USERNAME = data["USERNAME"]
        PASSWORD = data["PASSWORD"]
        print(f"USERNAME: {USERNAME}")
        print(f"PASSWORD: {PASSWORD}")

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(USERNAME, PASSWORD)


setup_server()  # setup server
contact_names, contact_emails = get_contacts()  # get contacts
message_template = read_template()  # read template

# For each contact, send the custom email
for contact_name, contact_email in zip(contact_names, contact_emails):
    msg = MIMEMultipart()  # create a message
    message = message_template.substitute(CONTACT_NAME=name.title())
    msg['From']=SENDER_EMAIL
    msg['To']=contact_email
    msg['Subject']="Subject Text Goes Here"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    
    del msg