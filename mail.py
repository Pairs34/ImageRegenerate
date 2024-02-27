import smtplib
import traceback
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    def send_mail(self, receiver_email, spoofed_email, spoofed_name, message, subject, attachments: MIMEImage):
        try:
            smtp_config = {
                'host': "smtp-relay.brevo.com",
                'port': 587,
                'username': "botsepeti@gmail.com",
                'password': "ETkmBnzMFgdy6ZpX"
            }

            if smtp_config:
                msg = MIMEMultipart()
                msg['From'] = f"{spoofed_name} <{spoofed_email}>"
                msg['To'] = receiver_email
                msg['Subject'] = subject
                # body = message
                msg.attach(attachments)

                with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
                    server.starttls()
                    server.login(smtp_config['username'], smtp_config['password'])
                    server.sendmail(spoofed_email, receiver_email, msg.as_string())
                print('Spoofed Email sent successfully to', receiver_email, 'from', spoofed_name)
        except Exception as e:
            print("Error sending email:", e)
            traceback.print_exc()