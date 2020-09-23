import smtplib, ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart


def send_email(address, subject, email_content, pw):
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "gpuscrapingbot@gmail.com"
        password = pw
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = address
        msg.set_content(email_content)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("Successfully sent email to " + address)
    except Exception as e:
        print("email failed see exception below")
        print(str(e))
