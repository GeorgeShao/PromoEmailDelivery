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

SENDER_EMAIL = ""
SENDER_PASSWORD = ""

colorama.init()

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




# GUI Code
class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('PromoEmailDelivery (PED)')

        self.text = QLabel("Please enter your email username & password.")
        self.emailTextBox = QLineEdit(self)
        self.passwordTextBox = QLineEdit(self)
        self.loginButton = QPushButton("Login")
        self.text.setAlignment(Qt.AlignCenter)

        self.emailTextBox.setText("email@example.com")
        self.passwordTextBox.setText("mypassword123")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.emailTextBox)
        self.layout.addWidget(self.passwordTextBox)
        self.layout.addWidget(self.loginButton)

        self.setLayout(self.layout)

        # Connecting the signal
        self.loginButton.clicked.connect(self.login)

    @Slot()
    def login(self):
        # Get SMTP (Simple Mail Transfer Protocol) server credidentials
        with open("CREDIDENTIALS.json", mode='r', encoding='utf-8') as credidentials_file:
            data = json.load(credidentials_file)
            SENDER_EMAIL = data["SENDER_EMAIL"]
            SENDER_PASSWORD = data["SENDER_PASSWORD"]
            terminal_msg("Obtained credidentials", "success")

        # Login to SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(SENDER_EMAIL, SENDER_PASSWORD)
        terminal_msg("Logged into SMTP server", "success")

        # Get contacts
        contact_emails, contact_first_names, contact_last_names = get_contacts()
        terminal_msg("Received contacts", "success")

        # Read template
        message_template = read_template()
        terminal_msg("Received message template", "success")

        # For each contact, send the custom email
        for contact_email, contact_first_name, contact_last_name in zip(contact_emails, contact_first_names, contact_last_names):
            msg = MIMEMultipart()  # create a message
            message = message_template.substitute(CONTACT_EMAIL=str(contact_email), CONTACT_FIRST_NAME=str(contact_first_name.title()), CONTACT_LAST_NAME=str(contact_last_name.title()))
            msg['From']=SENDER_EMAIL
            msg['To']=contact_email
            msg['Subject']="Just Testing Links..."
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            terminal_msg(f"Msg sent to {contact_last_name}, {contact_first_name}: {contact_email}", "success")
            del msg

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(400, 200)
    widget.show()

    sys.exit(app.exec_())