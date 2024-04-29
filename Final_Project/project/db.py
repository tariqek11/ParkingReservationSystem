import psycopg2
from psycopg2 import OperationalError
import os

def create_connection():
    try:
        conn = psycopg2.connect(
            host='smartparkingsystem.postgres.database.azure.com',
            database='postgres',
            user='coe892',
            password='parking=123',
            sslmode='require',  # This is required for Azure
            port='5432'
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

def execute_update_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()  # Commit the transaction
        print("Update successful")
        return cursor.rowcount  # Return the number of rows affected
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return -1  # Return -1 to indicate an error
    
def execute_insert_query(connection, query, data):
    cursor = connection.cursor()  
    try:
        cursor.execute(query, data)  # Execute the query with parameterized data
        connection.commit()  
        return {"success": True, "message": "Record inserted successfully."}
    except Exception as e:  # Catch any exceptions that occur during the query execution
        connection.rollback()  
        print(f"An error occurred: {e}")
        return {"success": False, "message": str(e)}
    finally:
        cursor.close()  

def execute_delete_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()  # Commit the transaction
        print("Deletion successful")
        return cursor.rowcount  # Return the number of rows affected
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        connection.rollback()  # Rollback the transaction on error
        return -1  # Return -1 to indicate an error
    finally:
        cursor.close()