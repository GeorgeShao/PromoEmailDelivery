from string import Template
import smtplib
import json

# Reads contacts from contacts.txt & returns names & emails
def get_contacts():
    names = []
    emails = []
    with open("contacts.txt", mode='r', encoding='utf-8') as contacts_file:
        for contact in contacts_file:
            names.append(contact.split()[0])
            emails.append(contact.split()[1])
    return names, emails


# Reads template & returns template object
def read_template():
    with open("message.txt", mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# Setup SMTP (Simple Mail Transfer Protocol) server
def setup_server():
    with open("CREDIDENTIALS.json", mode='r', encoding='utf-8') as credidentials:
        pass

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
