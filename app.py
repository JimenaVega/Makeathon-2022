# Decide based on 30-30-30 rule: >30°C <30%Hum >30km/h >30days
def decide_risk(temperature, humidity, air_quality, wind_speed, days_without_rain):
    temp_risk = 1 if temperature > 30 else 0
    hum_risk = 1 if humidity < 30 else 0
    wind_risk = 1 if wind_speed > 30 else 0
    days_risk = 1 if days_without_rain > 30 else 0
    
    risk = temp_risk + hum_risk + wind_risk + days_risk
    
    if(air_quality > 250):
        return 2
    if(risk < 3):
        return 0
    elif(risk >= 3):
        return 1
    
    