# Indoor Air Pollution Monitoring System (Mobile)

A mobile indoor air quality monitoring system for measuring humidity, volatile organic compounds, particulate matter and detecting concentration of various gases.

## Features

1. Live Dashboard - Real time graphs and AQI alerts 

    - For email alerts, edit `file.py` (in the `Live_Dashboard` folder) with your details
2. Website - View old graphs based on locations in the IIIT-H campus
3. Arduino folder contains the `.ino` scripts to dump onto the nodes - connects to OneM2M and Thingspeak and gets sensor readings
4. Graphs Scripts - generates different graphs based on location and time