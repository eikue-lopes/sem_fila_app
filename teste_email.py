import smtplib
from email.mime.text import MIMEText
from constants import ADDRESS_DB1 , ADDRESS_DB2 , APP_EMAIL, APP_PASSWORD_EMAIL , SSL_EMAIL_HOST , SSL_EMAIL_HOST_PORT
from random import randrange

def send_email_verification_code(user_email,code):
    try:
        message = MIMEText('<p>Seu código de verificação no App SemFila:</p> <p><b>%s</b></p>'%code,_subtype='html')
        message['subject'] = "Verificação de Email SemFila App"
        message['from'] = APP_EMAIL
        message['to'] = user_email
        server = smtplib.SMTP_SSL(SSL_EMAIL_HOST,SSL_EMAIL_HOST_PORT)
        APP_PASSWORD_EMAIL = input("Email password: ")
        server.login(APP_EMAIL,APP_PASSWORD_EMAIL)
        server.sendmail(APP_EMAIL,user_email,message.as_string())
        server.quit()
        return True
    except:
        return False

code = randrange(100000,1000000)
to = "eikuelopes2014@gmail.com"

print("Enviando código: %d de %s para %s..."%(code,APP_EMAIL,to))

r = send_email_verification_code(to,code)

if r == True:
    print("Sucesso!")
else:
    print("Erro!")