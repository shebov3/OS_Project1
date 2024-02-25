import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))

    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == "__main__":
    sender_email = 'shehabtarik425@yahoo.com'
    sender_password = '~~~~~~ PASSWORD ~~~~~~'
    recipient_email = 'shehabtarik425@yahoo.com'

    subject = 'Test Email'
    body = 'This is a test email sent from a Python script.'

    try:
        send_email(sender_email, sender_password, recipient_email, subject, body)
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")