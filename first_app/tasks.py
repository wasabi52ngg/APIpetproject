from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Reservation
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_reservation_notification(self, reservation_id, action):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        customer = reservation.customer
        if not customer.email:
            logger.warning(f"Клиент {customer} не имеет email для бронирования {reservation_id}")
            return f"No email for customer {customer.id}"

        subject = f"Статус бронирования #{reservation_id}"
        if action == 'confirmed':
            message = (
                f"Уважаемый {customer.first_name} {customer.last_name},\n\n"
                f"Ваше бронирование стола #{reservation.table.table_number} в ресторане "
                f"{reservation.table.restaurant.name} на {reservation.reservation_date} в "
                f"{reservation.time} подтверждено.\n\n"
                f"Количество гостей: {reservation.number_of_guests}\n"
                f"Спасибо за выбор нашего ресторана!"
            )
        elif action == 'cancelled':
            message = (
                f"Уважаемый {customer.first_name} {customer.last_name},\n\n"
                f"Ваше бронирование стола #{reservation.table.table_number} в ресторане "
                f"{reservation.table.restaurant.name} на {reservation.reservation_date} в "
                f"{reservation.time} было отменено.\n\n"
                f"Если у вас есть вопросы, свяжитесь с нами."
            )
        else:
            raise ValueError(f"Недопустимое действие: {action}")

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email],
            fail_silently=False,
        )
        logger.info(f"Уведомление о бронировании {reservation_id} ({action}) отправлено на {customer.email}")
        return f"Notification sent for reservation {reservation_id}"
    except Reservation.DoesNotExist:
        logger.error(f"Бронирование {reservation_id} не найдено")
        return f"Reservation {reservation_id} not found"
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления для бронирования {reservation_id}: {str(e)}")
        self.retry(countdown=60, exc=e)
