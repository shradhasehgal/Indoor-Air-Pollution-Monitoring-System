from flask import Flask, jsonify, json
from flask import render_template
from flask import request
import requests
import thingspeak
import time
import sys
import datetime
import aqi
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from file import *

app = Flask(__name__)

@app.route("/")
def main(count=8000):
	channels = [873271,873288]
	fields = [["field1","field2"],["field2","field3"]]
	avg = [[0,0],[0,0]]
	for i in range(len(channels)):
		ch = thingspeak.Channel(channels[i])
		r=ch.get({'results': count})
		e=eval(r)
		f=e['feeds']
		x1=[eval(t[fields[i][0]]) for t in f]
		x2=[eval(t[fields[i][1]]) for t in f]
		tx=[time.strptime(t['created_at'],"%Y-%m-%dT%H:%M:%SZ") for t in f]

		currentDT = datetime.datetime.now()
		day = int(currentDT.strftime("%j"))
		hour = int(currentDT.strftime("%H"))
		minute = int(currentDT.strftime("%M"))

		flag = 0

		#day = 299
		#minute = 1
		#hour = 21

		if minute <= 29:
			hour -= 1
		minute = (minute + 60 -30) % 60
		
		if hour <= 4:
			day -= 1
		hour = (hour + 24 - 5) % 24

		if hour == 0:
			hour = 23
			day = day-1
			flag = 1
		else:
			hour = hour-1

		index = []
		print(minute," ",hour," ",day)
		for x in range(len(tx)):
			if minute == 0:
				if int(tx[x].tm_yday) == day  and int(tx[x].tm_hour) == hour:
					index.append(x)				
			else:
				if flag == 1:
					if(int(tx[x].tm_yday) == day and int(tx[x].tm_hour) == 23 and int(tx[x].tm_min) >= minute) or (int(tx[x].tm_yday) == day+1 and int(tx[x].tm_hour) == 0 and tx[x].tm_min <= minute):
						index.append(x); 
				else:
					if(tx[x].tm_yday == day and tx[x].tm_hour == hour and tx[x].tm_min >= minute) or (tx[x].tm_yday == day and tx[x].tm_hour == hour+1 and tx[x].tm_min <= minute):
						index.append(x);
						print("minute ", minute, " ", tx[x].tm_min)
						print("hour ", hour, " ", tx[x].tm_hour)
						print("day ", day, " ", tx[x].tm_yday)
		
		avg[i][0] = 0
		avg[i][1] = 0

		for x in index:
			print("x1 ",x1[x]," x2 ",x2[x])
			avg[i][0] += x1[x]
			avg[i][1] += x2[x]
		
		avg[i][0] = avg[i][0]/len(index)
		avg[i][1] = avg[i][1]/len(index) 

		
		print(len(index))
		
	for i in range(2):
		print(avg[i][0])
		print(avg[i][1])

	myaqi = aqi.to_aqi([
		(aqi.POLLUTANT_PM25, avg[0][0]),
		(aqi.POLLUTANT_PM10, avg[0][1]),
		(aqi.POLLUTANT_NO2_1H, avg[1][1])
	], algo=aqi.ALGO_EPA)

	print("AQI: ", myaqi)

	mycc = aqi.to_cc(aqi.POLLUTANT_PM25, avg[0][0])
	print("pm25: " ,mycc)

	mycc = aqi.to_cc(aqi.POLLUTANT_PM10, avg[0][1])
	print("pm10: " ,mycc)

	mycc = aqi.to_cc(aqi.POLLUTANT_CO_8H, avg[1][0])
	print("CO: " ,mycc)

	mycc = aqi.to_cc(aqi.POLLUTANT_NO2_1H, avg[1][1])
	print("NO2: " ,mycc)


if __name__ == "__main__":
	app.run(debug = True)