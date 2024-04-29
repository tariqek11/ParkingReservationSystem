from fastapi import FastAPI, HTTPException
import psycopg2
import db

app = FastAPI()
db_conn = db.create_connection()

@app.get("/parking_spots")
async def get_parking_lots():
    query = "SELECT * FROM parking_lot"
    result = db.execute_read_query(connection=db_conn, query=query)

    return result

@app.get("/availability")
async def get_available_parking_spots():
    update_query = f"SELECT space_id FROM parking_lot WHERE availability = True"
    result = db.execute_read_query(db_conn, update_query)
    print(f"Parking Availability entry: {result}")
    return result

@app.get("/availability/{id}")
async def get_availability(id: int):
    update_query = f"SELECT availability FROM parking_lot WHERE space_id = {id}"
    result = db.execute_read_query(db_conn, update_query)
    print(f"Parking Availability entry: {result}")
    if result and len(result) > 0:
        # Extract the first column of the first row in the result
        availability = result[0][0]
        print(f"Parking Availability for space_id {id}: {availability}")
        return availability
    else:
        print(f"No parking space found with space_id {id}")
        return {"error": "Parking space not found"}
    
@app.get("/reservations")
async def get_reservations():
    update_query = f"SELECT reservation_id, end_time FROM reservation"
    result = db.execute_read_query(db_conn, update_query)
    print(f"Parking Reservations: {result}")
    return result

@app.get("/createreservation")
async def create_reservation(license_plate: str, id: int, start_time: str, end_time: str, price: float):
    update_query = f"""
    INSERT INTO reservation (license_plate, space_id, start_time, end_time, price)
    VALUES (%s, %s, %s, %s, %s)
    """
    query_params = (license_plate, id, start_time, end_time, price)
    
    result = db.execute_insert_query(db_conn, update_query, query_params)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": "Reservation created successfully", "id": id}