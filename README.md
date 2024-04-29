Needed Python libraries to be installed:
- FastAPI: pip install fastapi
- Requests: pip install requests
- Psycopg2: pip install psycopg2
- Pika: pip install pika
- Eel: pip install eel
- Paho MQTT Client: pip install paho-mqtt
- Pytz: pip install pytz
- Docker desktop: docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:3.13-management

Steps:

Run IoT Simulation
1) Make sure MQTT server is running at https://coe892.cloud.shiftr.io/
2) Go to https://wokwi.com/projects/394156695210647553 and run ESP32 device
simulation by clicking the green play circle button
3) Run python updateParking.py in a terminal to listen to IoT device and actively update
database
*Should actively see ESP32 and updateParking.py connect to the server and see messages
exchanged in both terminals by toggling (clicking) switches on the breadboard for the ESP32
device

Run Program (requires 4 terminals)
1) On terminal 1 run docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672
rabbitmq:3.13-management
2) On terminal 2 run uvicorn server:app --port 8001 so FastAPI server is running on
http://127.0.0.1:8001
3) On terminal 3 run python requestHandler.py
4) On terminal 4 cd into the app folder then run python main.py to start the program

Resolving an Eel Error
Traceback (most recent call last):
File "c:\Users\tariq\Downloads\app\app\main.py", line 1, in <module>
import eel
File "C:\Python312\Lib\site-packages\eel_init_.py", line 16, in <module>
import bottle.ext.websocket as wbs
ModuleNotFoundError: No module named 'bottle.ext.websocket'
Open the C:\Python312\Lib\site-packages\eel_init_.py file and go to line 16.
Replace <import bottle.ext.websocket as wbs> with <import bottle_websocket as wbs>
