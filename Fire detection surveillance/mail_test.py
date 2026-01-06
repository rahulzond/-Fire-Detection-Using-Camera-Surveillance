import smtplib
from email.mime.text import MIMEText

EMAIL = "kambleajinkya490@gmail.com"
PASSWORD = "mzyq azrl vtaa yzxs"
TO = "rahulzond2004@gmail.com"

msg = MIMEText("Test email from Python")
msg['Subject'] = "Test"
msg['From'] = EMAIL
msg['To'] = TO

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)

print("Sent!")
