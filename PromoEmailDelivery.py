from string import Template
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = ""
SENDER_PASSWORD = ""

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
with open("CREDIDENTIALS.json", mode='r', encoding='utf-8') as credidentials_file:
    data = json.load(credidentials_file)
    SENDER_EMAIL = data["SENDER_EMAIL"]
    SENDER_PASSWORD = data["SENDER_PASSWORD"]
    print(f"SENDER_EMAIL: {SENDER_PASSWORD}")
    print(f"SENDER_PASSWORD: {SENDER_PASSWORD}")

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(SENDER_EMAIL, SENDER_PASSWORD)


contact_names, contact_emails = get_contacts()  # get contacts
message_template = read_template()  # read template


# For each contact, send the custom email
for contact_name, contact_email in zip(contact_names, contact_emails):
    msg = MIMEMultipart()  # create a message
    message = message_template.substitute(CONTACT_NAME=contact_name.title())
    msg['From']=SENDER_EMAIL
    msg['To']=contact_email
    msg['Subject']="Subject Text Goes Here"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    print(f"Msg sent to {contact_name}: {contact_email}")
    
    del msg