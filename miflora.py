#!/usr/bin/python
#Read data from Xiaomi flower monitor, tested on firmware version 2.6.6

import sys
from gattlib import GATTRequester, GATTResponse
from struct import *
import MySQLdb
import datetime
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_FAN = 22
GPIO_LED = 27
GPIO_WATER = 17

#setup the port as output
GPIO.setup(GPIO_FAN, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_WATER, GPIO.OUT)

now = datetime.datetime.now()
time =now.strftime("%Y-%m-%d %H:%M:%S")
hour = int(now.strftime("%H"))
minutes = int(now.strftime("%M"))
date = now.date()

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="raspberry",  # your password
                     db="miflora")        # name of the data base
cur = db.cursor()
sql = "select * from plants_info where id = 1"
cur.execute(sql)
for row in cur.fetchall():
	address = str(row[0])
	sun_b = row[2]
        sun_t = row[3]
        moi_b = row[4]
        moi_t = row[5]
        tem_b = row[6]
        tem_t = row[7]
        fer_b = row[8]
        fer_t = row[9]

sun_b = int(sun_b*10.76/(24*0.71))
sun_t = int(sun_t*10.76/(2*0.71))        

sql = "SELECT sunlight,moisture,temperature,fertility,hour(time),date(time),number,light,water,fan,time from sensor_data_hour where id = 1"
cur.execute(sql)
for row in cur.fetchall():
        sum_sunlight = row[0]
	sum_moisture = row[1]
	sum_temperature = row[2]
	sum_fertility = row[3]
	last_hour = row[4]
	last_date = row[5]
	number = row[6]
	last_light = row[7]
	last_water = row[8]
	last_fan =row[9]
	last_time = row[10]
db.close()

#address = "C4:7C:8D:60:93:25"
requester = GATTRequester(address)
#Read battery and firmware version attribute
data=requester.read_by_handle(0x0038)[0]
battery, version = unpack('<B6s',data)
#print "Battery level:",battery,"%"
#print "Firmware version:",version
#Enable real-time data reading
requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))
#Read plant data
data=requester.read_by_handle(0x0035)[0]
temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
temperature = float(temperature/10)
#print "Light intensity:",sunlight,"lux"
#print "Temperature:",temperature/10.,"C"
#print "Soil moisture:",moisture,"%"
#print "Soil fertility:",fertility,"uS/cm"
f = open("/home/pi/smartplants/smart-plants/system_log.txt","a")
if hour > 17 or hour < 6:
	if last_light == 1:
		GPIO.output(GPIO_LED, GPIO.LOW)
		last_light = 0
		#f = open("system_log.txt","a")
		f.write("%s [LIGHTING] is [OFF] \n"% time)
		#f.close()
else:
	if last_light == 0:
		GPIO.output(GPIO_LED, GPIO.HIGH)
		last_light = 1
		#f = open("system_log.txt","a")
                f.write("%s [LIGHTING] is [ON] \n"% time)
                #f.close()

if last_water == 0:
	if moisture < moi_b:
		GPIO.output(GPIO_WATER, GPIO.HIGH)
		last_water = 1
		#f = open("system_log.txt","a")
                f.write("%s [WATERING] is [ON] \n"% time)
                #f.close()
else:
	if moisture > moi_t:
		GPIO.output(GPIO_WATER, GPIO.LOW)
		last_water = 0
		#f = open("system_log.txt","a")
                f.write("%s [WATERING] is [OFF] \n"% time)
                #f.close()

if last_fan == 1:
	if moisture < moi_t and temperature < tem_t:
		last_fan = 0
		GPIO.output(GPIO_FAN, GPIO.LOW)
		#f = open("system_log.txt","a")
                f.write("%s [FAN] is [OFF] \n"% time)
                #f.close()
else:
	if moisture > moi_t or temperature > tem_t:
		GPIO.output(GPIO_FAN, GPIO.HIGH)
		last_fan = 1
		#f = open("system_log.txt","a")
                f.write("%s [FAN] is [ON] \n"% time)
                #f.close()

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="raspberry",  # your password
                     db="miflora")        # name of the data base
cur = db.cursor()

sql = "UPDATE sensor_data_hour SET sunlight = %d, moisture = %d, temperature = %0.1f, fertility = %d, time = '%s', light = %d, water = %d, fan = %d WHERE id = 2 " % (sunlight, moisture, temperature, fertility, time, last_light, last_water, last_fan)
cur.execute(sql)
db.commit()

if hour != int(last_hour) or last_date < date :
	compare_time = str(last_date) + " " + str(last_hour) + '%'
	#print compare_time
	sql = "SELECT * FROM sensor_data where time LIKE '%s'" % compare_time
	cur.execute(sql)
	if cur.rowcount == 0:
		#f = open("system_log.txt","a")
		f.write("%s ======= STORE SENSOR DATA ======= \n"% time)
		#f.close()
		sum_sunlight = int(round(float(sum_sunlight)/number))
		sum_moisture = int(round(float(sum_moisture)/number))
		sum_temperature = float(sum_temperature/number)
		sum_fertility = int(round(float(sum_fertility)/number))
		sql = "INSERT INTO sensor_data(sunlight,moisture,temperature,fertility,time) VALUES ('%d','%d','%0.1f','%d','%s')" % (sum_sunlight,sum_moisture,sum_temperature,sum_fertility,last_time)
		cur.execute(sql)
		db.commit()
	number = 1
	sql = "UPDATE sensor_data_hour SET  sunlight = %d, moisture = %d, temperature = %0.1f, fertility = %d, time = '%s', number = %d, light = %d, water = %d, fan = %d WHERE id = 1" % (sunlight,moisture,temperature,fertility,time,number,last_light,last_water,last_fan)
else:
	sql = "UPDATE sensor_data_hour SET  sunlight = %d, moisture = %d, temperature = %0.1f, fertility = %d, time = '%s', number = %d, light = %d, water = %d, fan = %d WHERE id = 1" % (sum_sunlight+sunlight, sum_moisture+moisture, sum_temperature + temperature, sum_fertility + fertility, time, number + 1, last_light, last_water, last_fan )

#f = open("system_log.txt","a")
f.write("%s ....... READ SENSOR DATA ....... \n"% time)
f.close()

# Use all the SQL you like
cur.execute(sql)

db.commit()

db.close()

#limit the log file to 500 lines
f = open("/home/pi/smartplants/smart-plants/system_log.txt","r")
lines = f.readlines()
f.close()

number_line = len(lines)
if number_line > 500:
        f = open("/home/pi/smartplants/smart-plants/system_log.txt","w")
        number_line = number_line - 500
        for line in lines:
                if number_line == 0:
                        f.write(line)
                else:
                        number_line = number_line-1
        f.close()
