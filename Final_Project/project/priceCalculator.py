from datetime import datetime, time

def getUtilizationMultiplier(utilizationPercentage):
    if utilizationPercentage < 10:
        return 0.25
    elif utilizationPercentage < 20:
        return 0.3
    elif utilizationPercentage < 40:
        return 0.5
    elif utilizationPercentage < 60:
        return 0.7
    elif utilizationPercentage < 80:
        return 1.0
    elif utilizationPercentage < 100:
        return 1.35
    else:
        return 2.0

def getHourBasedRate():
    startingTime = datetime.now().time()
    if (startingTime >= time(hour=6, minute=0, second=0)) and (startingTime < time(hour=8, minute=0, second=0)):
        return 5.0
    elif (startingTime >= time(hour=8, minute=0, second=0)) and (startingTime < time(hour=17, minute=0, second=0)):
        return 9.0
    elif (startingTime >= time(hour=17, minute=0, second=0)) or (startingTime < time(hour=6, minute=0, second=0)):
        return 7.0
    
def getDynamicRate(currentOccupancy, maxCapacity):
    utilizationPercentage = currentOccupancy/maxCapacity
    utilizationPriceFactor = getUtilizationMultiplier(utilizationPercentage)
    hourBaseRate = getHourBasedRate()

    dynamicRate = hourBaseRate * utilizationPriceFactor
    return dynamicRate