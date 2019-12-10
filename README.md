# Indoor Air Pollution Monitoring System (Mobile)

A mobile indoor air quality monitoring system for measuring humidity, volatile organic compounds, particulate matter and detecting concentration of various gases.

## Features

### Live Dashboard 
- Real time graphs and AQI alerts 
- For email alerts, edit `file.py` (in the `Live_Dashboard` folder) with your details

### Website 
- View old graphs based on locations in the IIIT-H campus

### Arduino 
- Arduino folder contains the `.ino` scripts to dump onto the nodes 
- Scripts connect to OneM2M and Thingspeak and gets sensor readings

### Graphs Scripts 
- Python script to generate different graphs based on location and time