# Makeathon-2022



## Pysense
The Pysense shield allows you to sense the environment using 5 different sensors:

    Accelerometer (LIS2HH12)
    Light Sensor (LTR329ALS01)
    Pressure Sensor (MPL3115A2)
    Temperature / Humidity Sensor (SI7006A20)


## Pytrack

Pytrack Features

    Super accurate GNSS Glonass GPS
    3 axis 12-bit accelerometer
    USB port with serial access
    LiPo battery charger
    MicroSD card compatibility
    Ultra low power operation (~1uA in deep sleep)

Location Services Supported

    GPS
    GLONASS
    Galileo
    QZSS


## Common errors

- Error cannot connect /dev/ttyACM0
```sudo chmod 777 /dev/ttyACM0 ```

en Debian:
```sudo usermod -a -G dialout $USER ```
en Arch:
```sudo usermod -a -G uucp $USER```

- Pymakr no reconoce placa

```sudo apt install nodejs npm```

Utilizar pymakr version 1.1.18

## Links

- [Boards: More info](https://docs.pycom.io/datasheets/expansionboards/)
