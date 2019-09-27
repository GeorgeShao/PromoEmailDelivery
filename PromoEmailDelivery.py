import csv
from string import Template
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = ""
SENDER_PASSWORD = ""

# Reads contacts from contacts.txt & returns names & emails
def get_contacts():
    emails = []
    first_names = []
    last_names = []
    with open("test_data.csv", mode='r', encoding='utf-8') as csv_file:
        print("Listing contact emails...")
        csv_file_content = csv.reader(csv_file, delimiter=',')
        first_line = True
        for contact in csv_file_content:
            if not first_line:
                if contact[0]:
                    emails.append(contact[0])
                    first_names.append(contact[1])
                    last_names.append(contact[2])
                    print(f"- {contact[0]}: {contact[1]} {contact[2]}")
            else:
                first_line = False
    return emails, first_names, last_names


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
    print("Obtained credidentials")

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(SENDER_EMAIL, SENDER_PASSWORD)
print("Logged into SMTP server")


contact_emails, contact_first_names, contact_last_names = get_contacts()  # get contacts
print("Received contacts")
message_template = read_template()  # read template
print("Received message template")


# For each contact, send the custom email
for contact_email, contact_first_name, contact_last_name in zip(contact_emails, contact_first_names, contact_last_names):
    msg = MIMEMultipart()  # create a message
    message = message_template.substitute(CONTACT_EMAIL=str(contact_email), CONTACT_FIRST_NAME=str(contact_first_name.title()), CONTACT_LAST_NAME=str(contact_last_name.title()))
    msg['From']=SENDER_EMAIL
    msg['To']=contact_email
    msg['Subject']="Subject Text Goes Here"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    print(f"Msg sent to {contact_last_name}, {contact_first_name}: {contact_email}")
    
    del msg