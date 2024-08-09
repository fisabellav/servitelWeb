# utils.py

from mailersend import emails
from django.conf import settings


def get_template(status):
    if status == 'CF':
        return "7dnvo4d092xg5r86"
    elif status == 'CN':
        return "yzkq340xnx34d796"
    elif status == 'EP':
        return "7dnvo4d092xg5r86"

def get_subject(status):
    if status == 'CF':
        return "Confirmación de Pedido"
    elif status == 'CN':
        return "Pedido Cancelado"
    elif status == 'EP':
        return "Pedido en Proceso"
    else:
        return "Actualización de Pedido"

def send_order_status_email(user_email, user_name, order, new_status):
    products = []
    template = get_template(new_status)
    subject = get_subject(new_status)

    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
    mail_body = {
        "products": products,
        "order_number": order.id
    }

    mail_from = {
        "name": "Servitel",
        "email": settings.DEFAULT_FROM_EMAIL,
    }

    recipients = [
        {
            "name": user_name,
            "email": user_email,
        }
    ]

    products = [
        {
            "url": detail.product.image.url if detail.product.image else "",
            "image": detail.product.image.url if detail.product.image else "",
            "price": detail.product.price,
            "title":  detail.product.product,
            "description":  detail.product.description
        }
        for detail in order.orderdetail_set.all()
    ]

    personalization = [
        {
            "email": user_email,
            "data": {
                "products": products,
                "order_number": order.id
            }
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_template(template, mail_body)  # Reemplaza TEMPLATE_ID con el ID de tu plantilla
    mailer.set_advanced_personalization(personalization, mail_body)

    
    response = mailer.send(mail_body)

def send_verification_email(user_email, verification_url):
    
    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
    mail_body = {}

    mail_from = {
        "name": "Servitel",
        "email": settings.DEFAULT_FROM_EMAIL,
    }

    recipients = [
        {
            "email": user_email,
        }
    ]

    subject = 'Completa tu registro en nuestro sitio'
    html_content = f"""
    <p>Para completar tu registro, haz clic en el siguiente enlace:</p>
    <p><a href="{verification_url}">Completar registro</a></p>
    """

    # Configurar el correo
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_html_content(html_content, mail_body)

    # using print() will also return status code and data
    response = mailer.send(mail_body)
    print(response)

    return response
