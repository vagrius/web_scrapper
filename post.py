import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate

from auth import TOKEN


def auto_mailing():
    msg = MIMEMultipart()
    msg['Subject'] = 'Automail'
    msg['From'] = 'sender@gmail.com'
    msg['To'] = 'receiver@gmail.com'
    msg['Message-Id'] = make_msgid()
    msg['Date'] = formatdate(localtime=True)

    msg.attach(MIMEText(f'This letter means that Vadim completed the task :)', 'plain' if format == 'txt' else 'html'))
    part = MIMEApplication(open('output.csv').read())
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename('output.csv'))
    msg.attach(part)

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('sender@gmail.com', TOKEN)
    smtpObj.sendmail('sender@gmail.com', 'receiver@gmail.com', msg.as_string())
    smtpObj.quit()
