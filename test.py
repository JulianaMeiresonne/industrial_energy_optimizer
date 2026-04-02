import smtplib
from email.message import EmailMessage

sender_email = "bmsi30@yahoo.com"
sender_password = "JUNK_MAIL"

msg = EmailMessage()
msg["Subject"] = "Test SMTP Yahoo"
msg["From"] = sender_email
msg["To"] = sender_email
msg.set_content("Test d'envoi depuis Python")
smpt = smtplib.SMTP_SSL("smtp.mail.yahoo.com", port=465) 

try:
    smpt.login(sender_email, sender_password)
    smpt.send_message(msg)
    smpt.quit()
    smpt.debuglevel(1)


    print("Mail envoyé avec succès")

except Exception as e:
    print()
    print(type(e).__name__, e)