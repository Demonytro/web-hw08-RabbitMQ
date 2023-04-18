import pika
from faker import Faker
from mongoengine import *
import pymongo
import json

from datetime import datetime

from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    contacts = Contact.objects()
    i = 0
    for contact in contacts:
        i += 1
        dict_contact = contact.to_mongo().to_dict()
        print(dict_contact)
        print(contact)

        # "_id": {
        #     "$oid": "643ef2c35e76d7fdd1a6bcdf"
        # },

        message = {
            "id": str(dict_contact["_id"]),
            "payload": f"Task #{i}",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)

    connection.close()
    disconnect()


fake = Faker('uk-UA')


def seeds_db(count):
    for _ in range(count):
        Contact(fullname=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()) \
            .save()


if __name__ == '__main__':
    seed_count = input('Заполнить базу данных? (yes)>>> ')
    if seed_count == "yes":
        count_cont = int(input('и количество >>> '))
        seeds_db(count_cont)

    main()
