import RPi.GPIO as GPIO
import MySQLdb
import datetime

time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_FAN = 22
GPIO_LED = 27
GPIO_WATER = 17

#setup the port as output
GPIO.setup(GPIO_FAN, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)
GPIO.setup(GPIO_WATER, GPIO.OUT)
GPIO.output(GPIO_FAN, GPIO.LOW)
GPIO.output(GPIO_LED, GPIO.LOW)
GPIO.output(GPIO_WATER, GPIO.LOW)

f = open("/home/pi/smartplants/smart-plants/system_log.txt","a")
f.write("%s <<<<<<< RESET DEVICE >>>>>>> \n"% time)
f.close()

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="raspberry",  # your password
                     db="miflora")        # name of the data base
cur = db.cursor()
sql = "UPDATE sensor_data_hour SET light = 0, fan = 0, water = 0"
cur.execute(sql)
db.commit()
db.close()
