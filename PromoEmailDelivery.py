import sys
import csv
from string import Template
import smtplib
import json
import colorama
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from PySide2.QtWidgets import *
from PySide2.QtCore import *


colorama.init()

SENDER_EMAIL = ""
SENDER_PASSWORD = ""


# Prints custom coloured terminal msgs for logging, success msgs, errors msgs
def terminal_msg(msg, msg_type):
    if msg_type == "log":
        print(colorama.Fore.WHITE + msg)
    elif msg_type == "success":
        print(colorama.Fore.GREEN + msg)
    elif msg_type == "error":
        print(colorama.Fore.RED + msg)
    

# Reads contacts from contacts.txt & returns names & emails
def get_contacts():
    emails = []
    first_names = []
    last_names = []
    with open("test_data.csv", mode='r', encoding='utf-8') as csv_file:
        terminal_msg("Listing contact emails...", "log")
        csv_file_content = csv.reader(csv_file, delimiter=',')
        first_line = True
        for contact in csv_file_content:
            if not first_line:
                if contact[0]:
                    emails.append(contact[0])
                    first_names.append(contact[1])
                    last_names.append(contact[2])
                    terminal_msg(f"- {contact[0]}: {contact[1]} {contact[2]}", "log")
            else:
                first_line = False
    return emails, first_names, last_names


# Reads template from message.txt & returns template object
def read_template():
    with open("message.txt", mode='r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


# Main code
class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    @Slot()
    def login(self):
        # Get SMTP (Simple Mail Transfer Protocol) server credidentials
        try:
            SENDER_EMAIL = self.emailTextBox.text()
            SENDER_PASSWORD = self.passwordTextBox.text()
            terminal_msg("Obtained credidentials", "success")
        except Exception as e:
            terminal_msg("Error obtaining credidentials", "error")

        # Login to SMTP server
        try:
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login(SENDER_EMAIL, SENDER_PASSWORD)
            terminal_msg("Logged into SMTP server", "success")
        except Exception as e:
            terminal_msg("Error logging into SMTP server", "error")

        # Get contacts
        try:
            contact_emails, contact_first_names, contact_last_names = get_contacts()
            terminal_msg("Obtained contacts", "success")
        except Exception as e:
            terminal_msg("Error obtaining contacts", "error")

        # Read template
        try:
            message_template = read_template()
            terminal_msg("Obtained message template", "success")
        except Exception as e:
            terminal_msg("Error obtaining message template", "error")

        # For each contact, send the custom email
        for contact_email, contact_first_name, contact_last_name in zip(contact_emails, contact_first_names, contact_last_names):
            try:
                msg = MIMEMultipart()  # create a message
                message = message_template.substitute(CONTACT_EMAIL=str(contact_email), CONTACT_FIRST_NAME=str(contact_first_name.title()), CONTACT_LAST_NAME=str(contact_last_name.title()))
                msg['From']=SENDER_EMAIL
                msg['To']=contact_email
                msg['Subject']="Just Testing Links..."
                msg.attach(MIMEText(message, 'plain'))
                s.send_message(msg)
                terminal_msg(f"Msg sent to {contact_last_name}, {contact_first_name}: {contact_email}", "success")
                del msg
            except Exception as e:
                terminal_msg(f"Error sending msg to {contact_last_name}, {contact_first_name}: {contact_email}", "error")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # loginWindow setup code
    loginWindow = MyWidget()
    loginWindow.resize(400, 200)
    loginWindow.setWindowTitle('PromoEmailDelivery (PED)')

    loginWindow.text = QLabel("Please enter your email username & password.")
    loginWindow.emailTextBox = QLineEdit(loginWindow)
    loginWindow.passwordTextBox = QLineEdit(loginWindow)
    loginWindow.loginButton = QPushButton("Login")
    loginWindow.text.setAlignment(Qt.AlignCenter)

    loginWindow.emailTextBox.setText("email@example.com")
    loginWindow.passwordTextBox.setText("mypassword123")

    loginWindow.layout = QVBoxLayout()
    loginWindow.layout.addWidget(loginWindow.text)
    loginWindow.layout.addWidget(loginWindow.emailTextBox)
    loginWindow.layout.addWidget(loginWindow.passwordTextBox)
    loginWindow.layout.addWidget(loginWindow.loginButton)

    loginWindow.setLayout(loginWindow.layout)

    loginWindow.loginButton.clicked.connect(loginWindow.login)
    loginWindow.show()

    sys.exit(app.exec_())