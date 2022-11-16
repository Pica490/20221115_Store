from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from backend.models import ConfirmEmailToken, User

new_user_registered = Signal(
    providing_args=['user_id'],
)

new_order = Signal(
    providing_args=['user_id'],
)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):

    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {token.user.email}",
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email]
    )
    msg.send()

def message(user_id, id,data):

    user = User.objects.get(id=user_id)

    body = f'Номер вашего заказа: {id}\n' \
           f'Наш оператор свяжется с вами в ближайшее время для уточнения делатей заказа.\n' \
           f'Статуcы заказов вы можете посмотреть в разделе "Заказы".\n'

    for item in data[0]['ordered_items']:
        body += f'\nНаименование товара: {item["product_info"]["product"]["name"]}\n' \
                 f'Магазин: {item["product_info"]["shop"]}\n' \
                 f'Цена: {item["product_info"]["price"]} р.\n' \
                 f'Количество: {item["product_info"]["quantity"]} \n'

    body += f'\nСумма: {data[0]["total_sum"]} р.\n'
    body += f'\nФамилия Имя: {user.first_name} {user.last_name}\n' \
            f'Email: {user.email}\n' \
            f'\nАдрес доставки: \n г.{data[0]["contact"]["city"]}, ул.{data[0]["contact"]["street"]}, ' \
            f'д.{data[0]["contact"]["house"]}, к.{data[0]["contact"]["structure"]}, стр.{data[0]["contact"]["building"]},' \
            f' кв.{data[0]["contact"]["apartment"]}\n' \
            f'тел. {data[0]["contact"]["phone"]}'
    return body

@receiver(new_order)
def new_order_signal(user_id, id, data, **kwargs):

    user = User.objects.get(id=user_id)

    body = message(user_id, id, data)

    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f"Спасибо за заказ!",
        # message:
        f'{body}',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
