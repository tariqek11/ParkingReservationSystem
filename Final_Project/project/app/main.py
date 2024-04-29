import eel

eel.init('web')
from frontend import getRate, getTicketPrice, confirmReservation
eel.start("index.html")