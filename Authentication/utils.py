from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(body=data['email_body'],subject=data['email_subject'],to=[data['to_email']])

        email.send()