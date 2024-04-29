import eel
import pika
import math

#Assumes that this data is already given and saved by the app, creating user accounts is out of scope
email = "fake@email.com"
license_plate = "ASRM959"

#RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelReq = connection.channel()
channelReq.queue_declare(queue='requests')

def handleResponse(ch, method, properties, body):
    global response
    response = float(body.decode())
    print(response)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    ch.close()


def waitForResponse():
    channelRes = connection.channel()
    channelRes.queue_declare(queue='response')
    channelRes.basic_qos(prefetch_count=1)
    channelRes.basic_consume(queue='response', on_message_callback=handleResponse)
    channelRes.start_consuming()


@eel.expose
def getRate():
    message = "1"
    channelReq.basic_publish(exchange='', routing_key='requests', body=message)

    waitForResponse()
    rate = response
    return rate

@eel.expose()
def getTicketPrice(hours):
    message = license_plate + " " + hours
    channelReq.basic_publish(exchange='', routing_key='requests', body=message)

    waitForResponse()
    rate = response
    return rate

@eel.expose
def confirmReservation(duration, price):
    message = "2" + " " + license_plate + " " + str(duration) + " " + str(price) + " " + email
    channelReq.basic_publish(exchange='', routing_key='requests', body=message)