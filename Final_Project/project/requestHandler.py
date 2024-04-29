import pika
from datetime import datetime, timedelta, timezone
from priceCalculator import getDynamicRate
from reservation import selectSpot, makeReservation, sendConfirmationEmail
import requests
import db
import pytz

db_conn = db.create_connection()
BASE_URL = "http://127.0.0.1:8001"
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channelReq = connection.channel()
channelRes = connection.channel()
channelReq.queue_declare(queue='requests')
channelRes.queue_declare(queue='response')

def checkReservations():
    response = requests.get(f"{BASE_URL}/reservations")
    if response.status_code == 200:
        reservations = response.json()
        current_time = datetime.now(pytz.utc)
        eastern = pytz.timezone('America/New_York')
        current_time_edt = current_time.astimezone(eastern)
        for reservation in reservations:
            reservation_id = reservation[0]
            end_time_str = reservation[1]

            # Assuming end_time is in ISO format, parse it
            end_time = datetime.fromisoformat(end_time_str.rstrip('Z')).replace(tzinfo=timezone.utc)
            end_time_edt = end_time.astimezone(eastern)
            print (end_time_edt)
            print(current_time_edt)
            print( end_time_edt < current_time_edt)
            if end_time_edt < current_time_edt:
                # Delete past reservations
                delete_query = f"DELETE FROM reservation WHERE reservation_id = {reservation_id}"
                db.execute_delete_query(connection=db_conn, query=delete_query)





    
def handleParkingRequest(ch, method, properties, body):
    checkReservations()
    message = body.decode().split()
    print(f"Received message: {message}")
    #get values from database
    result = requests.get("http://127.0.0.1:8001/parking_spots").json()
    print(result)
    maxCapacity = len(result)
    currentOccupancy = 0
    for parking_spot in result:
        if(not parking_spot[2]): #availability column = false
            currentOccupancy += 1
    
    
    rate = getDynamicRate(currentOccupancy, maxCapacity)
    if(message[0] == "1"):
        res = rate
    elif(message[0] == "2"):
        print(f"Received message: {message[0]}")
        license = message[1]
        duration = message[2]
        price = message[3]
        email = message[4]
        #result = requests.get() #INSERT API TO POST A RESERVATION TO DATABASE
        makeReservation(license, int(duration), float(price))
        sendConfirmationEmail(email)
        ch.basic_ack(delivery_tag = method.delivery_tag)
        return
    else:
        license = message[0]
        duration = float(message[1])
        print(license)
        print(duration)
        res = duration * getDynamicRate(currentOccupancy, maxCapacity)

    res = round(res, 2)
    print(res)
    channelRes.basic_publish(exchange='', routing_key='response', body=str(res))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channelReq.basic_qos(prefetch_count=1)
channelReq.basic_consume(queue='requests', on_message_callback=handleParkingRequest)
channelReq.start_consuming()