from datetime import datetime, timedelta
import requests
import random
import db
import pytz

db_conn = db.create_connection()
BASE_URL = "http://127.0.0.1:8001"


def selectSpot():
    print()
    #query database to get the first free available spot
    available_spots = get_available_parking_spots()
    if available_spots:
    # Randomly choose one of the available spots
        chosen_spot = random.choice(available_spots)
        print(f"Chosen parking spot ID: {chosen_spot[0]}")
        return chosen_spot
    else:
        print("No available parking spots found.")
        return None

 
    
def makeReservation(license_plate, duration, price ):
    print()
    #query database to insert into reservation table
    available_spot = selectSpot()
    if available_spot is None:
        print("No parking spot available.")
        return
    

    space_id = available_spot[0]

    current_time = datetime.now()
    eastern = pytz.timezone('America/New_York')
    current_time_edt = eastern.localize(current_time)
    end_time = current_time_edt + timedelta(hours=int(duration))
 

    params = {
        "license_plate": license_plate,
        "id": space_id,
        "start_time": current_time.isoformat(),
        "end_time": end_time.isoformat(),
        "price": price
    }
    
    response = requests.get(f"{BASE_URL}/createreservation", params=params)
    #call function to update parking_lot table
    updateParkingLot(available_spot)


def updateParkingLot(parking_spot):
    space_id = parking_spot[0]
    update_query = f"UPDATE parking_lot SET availability = FALSE WHERE space_id = {space_id}"
    db.execute_update_query(connection=db_conn, query=update_query)


def sendConfirmationEmail(email): #this is out of scope, so we're only printing out a statement
    print("Email sent to " + email)



def get_available_parking_spots():
     response = requests.get(f"{BASE_URL}/availability")
     return handle_response(response)


def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}