import json
import os
from django.core.mail import send_mail
from kafka import KafkaConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification.settings')

def send_email(email,status):
    send_mail(
        'Payment Confirmation',
        f'Your order status: {status}.',
        'from@largescale.com',
        [email],
        fail_silently=False,
    )

def email_consumer():
    consumer = KafkaConsumer(
        'payment_result',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='pay-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        email = message.value['email_data']['email']
        status = message.value['email_data']['status']
        send_email(email, status)


if __name__ == '__main__':
    email_consumer()
