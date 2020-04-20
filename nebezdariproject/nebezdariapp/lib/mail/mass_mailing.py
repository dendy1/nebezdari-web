from ...models import MailingMember
from django.core.mail import send_mass_mail

def subscribers_mass_mail(message, link=""):
    subcribers_list = []
    subcribers_list_model = MailingMember.objects.all()
    for subscriber in subcribers_list_model:
        subcribers_list.append(str(subscriber.email))
    
    subject = "Рассылка от команды Nebezdari"
    from_email = "noreply@nebezdari.ru"
    mail_message = message + link
    data_tuple = ((subject, mail_message, from_email, subcribers_list),)
    send_mass_mail(data_tuple)
