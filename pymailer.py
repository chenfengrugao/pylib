
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formataddr, formatdate
from email import encoders
import os

class pymailer(object):
    
    def __init__(self, config: dict):
        self.Host = config['host']
        self.Port = config['port']
        self.Email = config['email']
        self.Password = config['password']
        self.From = config['from']
        self.using_ssl = config['using_ssl']
        self.To = []
        self.Cc = []
        self.Bcc = []
        self.attach_list = []

    def add_to(self, to: list):
        self.To = to
        
    def add_cc(self, cc: list):
        self.Cc = cc

    def add_bcc(self, bcc: list):
        self.Bcc = bcc

    def add_attach(self, f):
        self.attach_list.append(f)

    def send_mail(self, subject, content):
        # Create message container - the correct MIME type is multipart/alternative.
        if len(self.attach_list) > 0:
            msg = MIMEMultipart('mixed') # with attachment
        else:
            msg = MIMEMultipart('alternative') # text/html
        # msg = MIMEMultipart('related') # embeded image
        msg["Accept-Language"] = "zh-CN"
        msg["Accept-Charset"] = "ISO-8859-1,utf-8"
        msg['From'] = formataddr([self.From, self.Email])
        msg['To'] = ','.join(self.To)
        recipient = self.To
        msg['Subject'] = subject
        
        if len(self.Cc) > 0:
            msg['Cc'] = ','.join(self.Cc)
            recipient += self.Cc
            
        if len(self.Bcc) > 0:
            msg['Bcc'] = ','.join(self.Bcc)
            recipient += self.Bcc

        # msg format should be 'plain' or 'html'
        body = MIMEText(content, 'html', 'utf-8')
        msg.attach(body)

        # add attachment if exists
        for p in self.attach_list:
            part = MIMEBase('application', "octet-stream")
            with open(p, 'rb') as f:
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="{}"'.format(os.path.basename(p)))
                msg.attach(part)
        
        try:
            if self.using_ssl:
                smtp = smtplib.SMTP_SSL(self.Host, self.Port, timeout=30)
            else:
                smtp = smtplib.SMTP(self.Host, self.Port, timeout=30)
            smtp.set_debuglevel(1)
            smtp.login(self.Email, self.Password)
            smtp.sendmail(self.Email, recipient, msg.as_string())
            smtp.quit()
            print("email sent successfully")
        except Exception as e:
            print("email sent failed with error: {}".format(e))

if __name__ == '__main__':
    mailer = pymailer({'host': 'smtpcom.263xmail.com', #smtp server host
                       'port': '465', #smtp server port, 465 is for ssl, and 25 is for nossl
                       'email': 'feng.chen@newvisionu.com', #email account
                       'password': '******', #email password
                       'from': 'Chenfeng', # your name
                       'using_ssl': True}) #whether to use ssl
    
    mailer.add_to(['cf <chenfeng@exasic.com>'])
    #mailer.add_bcc(['exasic <chenfeng@exasic.com>'])
    
    mailer.add_attach('xxx.pdf')
    mailer.add_attach('xxx.ppt')
    
    mailer.send_mail('python smtp example',
                     '<p>Hi, </p><p>&nbsp;&nbsp;See the attachment.</p><p>Thanks.</p>')

    
