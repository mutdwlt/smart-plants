#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, flash, session, render_template, json, request
from flask.ext.mysql import MySQL
from gattlib import GATTRequester, GATTResponse
import datetime
from struct import *
import schedule
import time
from threading import Thread

app = Flask(__name__)
app.secret_key = "super secret key"
app.debug = True
mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'raspberry'
app.config['MYSQL_DATABASE_DB'] = 'miflora'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

g_sun = [-1] * 6
g_tem = [-1.0] * 6
g_moi = [-1] * 6
g_fer = [-1] * 6

with app.app_context():
	conn = mysql.connect()
	cursor = conn.cursor()
	sql = "SELECT * FROM plants_info WHERE id = 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
 		mac_address_sleep = row[0]
	cursor.close()
	conn.close()

mac_address = str(mac_address_sleep)

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)
    
def read_data_job():
	address = mac_address
	global g_sun
	global g_moi
	global g_tem
	global g_fer
	now = datetime.datetime.now()
        test_min = int(now.strftime("%M"))
        time = now.strftime("%Y-%m-%d %H:%M:%S")
	try:
		requester = GATTRequester(address)
                #Read battery and firmware version attribute
                data=requester.read_by_handle(0x0038)[0]
                battery, version = unpack('<B6s',data)
                #Enable real-time data reading
                requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))
                #Read plant data
                data=requester.read_by_handle(0x0035)[0]
                temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
                temperature=float(temperature/10)
		min = int(test_min/10)
		#g_sun[min] = sunlight
		#g_moi[min] = moisture
		#g_fer[min] = fertility
		#g_tem[min] = temperature
		#conn = mysql.connect()
               	#cursor = conn.cursor()
               	#sql = "INSERT INTO sensor_data_test (sunlight,moisture,temperature,fertility,time) VALUES ('%d','%d','%f','%d','%s')" % (sunlight,moisture,temperature,fertility,time)
             	#cursor.execute(sql)
              	#conn.commit()
               	#cursor.close()
                #conn.close()
		print "get data at %s" % time
	except:
		print "can not get data at %s" % time
	finally:
                if int(test_min/10) == 5:
                        sum_sun = 0
                        sum_tem = 0
                        sum_fer = 0
                        sum_moi = 0
                        check_sun = 0
                        check_tem = 0
                        check_fer = 0
                        check_moi = 0
                        for i in range(0,6):
                                if g_sun[i] != -1:
                                        sum_sun += g_sun[i]
                                        check_sun += 1
                                if g_moi[i] != -1:
                                        sum_moi += g_moi[i]
                                        check_moi += 1
                                if g_tem[i] != -1.0:
                                        sum_tem += g_tem[i]
                                        check_tem += 1
                                if g_fer[i] != -1:
                                        sum_fer += g_fer[i]
                                        check_fer += 1
			if check_sun != 0:
                        	sum_sun = int(sum_sun/check_sun)
			if check_moi != 0:
                       	 	sum_moi = int(sum_moi/check_moi)
                        if check_tem != 0:
				sum_tem = float(sum_tem/check_tem)
                        if check_fer != 0:
				sum_fer = int(sum_fer/check_fer)
			conn = mysql.connect()
                	cursor = conn.cursor()
			print "STORE DATA AFTER 1 HOUR at %s" % time
                	sql = "INSERT INTO sensor_data (sunlight,moisture,temperature,fertility,time) VALUES ('%d','%d','%f','%d','%s')" % (sum_sun,sum_moi,sum_tem,sum_fer,time)
                	cursor.execute(sql)
                	conn.commit()
                	cursor.close()
                	conn.close()
			for i in range(0,6):
				g_sun[i] = -1
				g_moi[i] = -1
				g_tem[i] = -1.0
				g_fer[i] = -1	


@app.route('/',methods=['GET', 'POST'])
def main():
	conn = mysql.connect()
      	cursor = conn.cursor()
     	sql = "SELECT * FROM plants_info WHERE id = 1"
     	cursor.execute(sql)
     	results = cursor.fetchall()
     	for row in results:
		plants_name = row[1]
             	sun_b = row[2]
		sun_t = row[3]
		moi_b = row[4]
		moi_t = row[5]
		tem_b = row[6]
		tem_t = row[7]
		fer_b = row[8]
		fer_t = row[9]
	sql = "SELECT * FROM sensor_data_hour WHERE id = 2"
	cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
		status_led = row[7]
		status_water = row[8]
		status_fan = row[9]
	cursor.close()
        conn.close()
	sun_b = int(sun_b*10.76/(0.71*24))
	sun_t = int(sun_t*10.76/(0.71*2))
	status_sun = 1
	status_moi = 1
	status_tem = 1
	status_fer = 1
	if request.method == 'POST':
		if not session.get('mac'):
			conn = mysql.connect()
                	cursor = conn.cursor()
                	sql = "SELECT * FROM plants_info WHERE id = 1"
                	cursor.execute(sql)
                	results = cursor.fetchall()
                	for row in results:
                        	address_x = row[0]
                	cursor.close()
                	conn.close()
			address = str(address_x)
			session['mac'] = address_x
		else:
			address = str(session['mac'])
		try:
			requester = GATTRequester(address)
			#Read battery and firmware version attribute
			data=requester.read_by_handle(0x0038)[0]
			battery, version = unpack('<B6s',data)
			#Enable real-time data reading
			requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))
			#Read plant data
			data=requester.read_by_handle(0x0035)[0]
			temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
			temperature=float(temperature/10)
			data_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			conn = mysql.connect()
                	cursor = conn.cursor()
                	sql = "UPDATE plants_info SET baterry = %d, firmware = '%s' WHERE id = 1" % (battery,version)
                	cursor.execute(sql)
			conn.commit()
			sql = "UPDATE sensor_data_hour SET sunlight = %d, moisture = %d,temperature=%0.1f,fertility=%d,time='%s' WHERE id = 2" % (sunlight,moisture,temperature,fertility,data_time)
                        cursor.execute(sql)
                        conn.commit()
			cursor.close()
			conn.close()
			flash('Data updated successfully','success')
		except:
			flash('Could not update sensor value, please try again','danger')
			conn = mysql.connect()
	                cursor = conn.cursor()
        	        sql = "SELECT * FROM sensor_data_hour WHERE id = 2"
                	cursor.execute(sql)
                	results = cursor.fetchall()
                	for row in results:
                        	sunlight = row[1]
                        	moisture = row[2]
                        	fertility = row[4]
                        	temperature = row[3]
                        	data_time = row[5]
                	cursor.close()
                	conn.close()
		if sunlight < sun_b:
			status_sun = 0
		elif sunlight > sun_t:
			status_sun = 2
                if moisture < moi_b:
                        status_moi = 0
                elif moisture > moi_t:
                        status_moi = 2
                if temperature < tem_b:
                        status_tem = 0
                elif temperature > tem_t:
                        status_tem = 2
                if fertility < fer_b:
                        status_fer = 0
                elif fertility > fer_t:
                        status_fer = 2
		string_time = str(data_time)
		string_time = string_time[11:-6]
		check_hour = int(string_time)
		if check_hour >= 18 or check_hour <=5:
			status_sun = 3
		return render_template('index.html',status_fan=status_fan,status_led=status_led,status_water=status_water,status_sun=status_sun,status_moi=status_moi,status_tem=status_tem,status_fer=status_fer,sun=sunlight,moi=moisture,tem=temperature,fer=fertility,time=data_time,plants_name=plants_name,sun_b=sun_b,sun_t=sun_t,moi_b=moi_b,moi_t=moi_t,tem_b=tem_b,tem_t=tem_t,fer_b=fer_b,fer_t=fer_t)
	else:
		conn = mysql.connect()
               	cursor = conn.cursor()
                sql = "SELECT * FROM sensor_data_hour WHERE id = 2"
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    	data_sun = row[1]
                       	data_moi = row[2]
                      	data_fer = row[4]
                     	data_tem = row[3]
                      	data_time = row[5]
		cursor.close()
		conn.close()
		if data_sun < sun_b:
                        status_sun = 0
                elif data_sun > sun_t:
                        status_sun = 2
                if data_moi < moi_b:
                        status_moi = 0
                elif data_moi > moi_t:
                        status_moi = 2
                if data_tem < tem_b:
                        status_tem = 0
                elif data_tem > tem_t:
                        status_tem = 2
                if data_fer < fer_b:
                        status_fer = 0
                elif data_fer > fer_t:
                        status_fer = 2
                string_time = str(data_time)
                string_time = string_time[11:-6]
                check_hour = int(string_time)
                if check_hour >= 18 or check_hour <=5:
                        status_sun = 3
		return render_template('index.html',status_fan=status_fan,status_led=status_led,status_water=status_water,status_sun=status_sun,status_moi=status_moi,status_tem=status_tem,status_fer=status_fer,plants_name=plants_name,sun=data_sun,moi=data_moi,tem=data_tem,fer=data_fer,time=data_time,sun_b=sun_b,sun_t=sun_t,moi_b=moi_b,moi_t=moi_t,tem_b=tem_b,tem_t=tem_t,fer_b=fer_b,fer_t=fer_t)

@app.route('/showSignUp')
def showSignUp():
	if not session.get('logged_in'):
		return render_template('signup.html')
	else:
                return redirect(url_for('main'))

@app.route('/plants')
def plants():
        if not session.get('logged_in'):
                return redirect(url_for('main'))
	conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM plants_info WHERE id = 1"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
                mac_address = row[0]
		plants_name = row[1]
		sun_bottom = row[2]
		sun_top	= row[3]
		moi_bottom = row[4]
		moi_top = row[5]
		tem_bottom = row[6]
		tem_top = row[7]
		fer_bottom = row[8]
		fer_top = row[9]
		battery = row[10]
		firmware = row[11]
        cursor.close()
        conn.close()	
	return render_template('plants.html',mac_address=mac_address,plants_name=plants_name,sun_b=sun_bottom,sun_t=sun_top,moi_b=moi_bottom,moi_t=moi_top,tem_b=tem_bottom,tem_t=tem_top,fer_b=fer_bottom,fer_t=fer_top,battery=battery,firmware = firmware)

@app.route('/editSensor',methods=['GET', 'POST'])
def editSensor():
	global mac_address
	if not session.get('logged_in') or session['user_role'] ==0:
                return redirect(url_for('main'))
	if request.method == 'POST':
		new_mac_address = request.form['mac_address']
		conn = mysql.connect()
                cursor = conn.cursor()
                sql = "UPDATE plants_info SET mac_address = '%s' WHERE id = 1" % new_mac_address
                cursor.execute(sql)
		conn.commit()
                cursor.close()
                conn.close()
		flash('Your sensor has been updated successfully','success')
		session['mac'] = new_mac_address
		mac_address = new_mac_address
		return redirect(url_for('plants'))
	else:
		conn = mysql.connect()
        	cursor = conn.cursor()
        	sql = "SELECT * FROM plants_info WHERE id = 1"
        	cursor.execute(sql)
        	results = cursor.fetchall()
        	for row in results:
                	mac_add = row[0]
        	cursor.close()
        	conn.close()
		return render_template('edit-sensor.html',mac_add=mac_add)

@app.route('/editPlants',methods=['GET', 'POST'])
def editPlants():
        if not session.get('logged_in') or session['user_role'] == 0:
                return redirect(url_for('main'))
        if request.method == 'POST':
		n_plants_name = request.form['plants_name']
                n_sun_b = request.form['sun_b']
		n_sun_t = request.form['sun_t']
		n_moi_b = request.form['moi_b']
		n_moi_t = request.form['moi_t']
		n_tem_b = request.form['tem_b']
		n_tem_t = request.form['tem_t']
		n_fer_b = request.form['fer_b']
		n_fer_t = request.form['fer_t']
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "UPDATE plants_info SET plants_name = '%s',sun_top = '%s',sun_bottom = '%s', moi_top = '%s', moi_bottom = '%s', tem_top = '%s', tem_bottom = '%s', fer_top = '%s', fer_bottom = '%s' WHERE id = 1" % (n_plants_name,n_sun_t,n_sun_b,n_moi_t,n_moi_b,n_tem_t,n_tem_b,n_fer_t,n_fer_b)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
                flash('Your plants has been updated successfully','success')
                return redirect(url_for('plants'))
        else:
                conn = mysql.connect()
                cursor = conn.cursor()
                sql = "SELECT * FROM plants_info WHERE id = 1"
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                        plants_name = row[1]
			sun_b = row[2]
			sun_t = row[3]
			moi_b = row[4]
			moi_t = row[5]
			tem_b = row[6]
			tem_t = row[7]
			fer_b = row[8]
			fer_t = row[9]
                cursor.close()
                conn.close()
                return render_template('edit-plants.html',plants_name=plants_name,sun_t=sun_t,sun_b=sun_b,tem_t=tem_t,tem_b=tem_b,moi_t=moi_t,moi_b=moi_b,fer_t=fer_t,fer_b=fer_b)

@app.route('/user')
def user():
    	if not session.get('logged_in'):
		return redirect(url_for('main'))
    	conn = mysql.connect()
      	cursor = conn.cursor()
        sql = "SELECT * FROM user \
                WHERE user_id = '%s'" % session['user_id']
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
                u_username = row[2]
	cursor.close()
	conn.close()
    	return render_template('user.html',username=u_username)

@app.route('/editUser')
def editUser():
	if not session.get('logged_in'):
                return redirect(url_for('main'))
    	return render_template('edit-user.html')

@app.route('/updateUser', methods=['POST'])
def updateUser():
	new_name = request.form['name']
	new_password = request.form['password']
	if new_name and new_password:
		conn = mysql.connect()
            	cursor = conn.cursor()
            	sql = "UPDATE user SET user_name = '%s', user_password = '%s'\
                	WHERE user_id = '%s'" % (new_name, new_password, session['user_id'])
            	cursor.execute(sql)
		conn.commit()
		cursor.close()
		conn.close()
		session['name']= new_name
		flash('Your information has been updated successfully','success')
		return redirect(url_for('user'))
	else:
		flash('Please check your input','danger')
		return redirect(url_for('editUser'))

@app.route('/showSignIn')
def showSignIn():
	if not session.get('logged_in'):
                return render_template('signin.html')
	else:
		return redirect(url_for('main'))

@app.route('/log')
def log():
	if not session.get('logged_in') or session['user_role'] == 0:
                return redirect(url_for('main'))
        else:
		f =open("device_log.txt","r")
		lines = f.readlines()
		f.close()
                return render_template('log.html',lines = lines)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
	if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
		cursor.close()
		conn.close()
                flash('User created successfully !','success')
		return redirect(url_for('showSignIn'))
            else:
		cursor.close()
		conn.close()
                flash(str(data[0]),'danger')
		return redirect(url_for('showSignUp'))	
	else:
            flash('Enter the required fields','danger')
	    return redirect(url_for('showSignUp'))

    except Exception as e:
        flash(str(e),'danger')
	return redirect(url_for('showSignUp'))

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
	    sql = "SELECT * FROM user \
       		WHERE user_username = '%s'" % _email
	    cursor.execute(sql)
	    results = cursor.fetchall()
	    for row in results:
		u_id = row[0]
		u_name = row[1]
		u_username = row[2]
		u_password = row[3]
		u_role = row[4]
	    cursor.close()
            conn.close()
	    if _password == u_password:
		session['logged_in'] = True
		session['name'] = u_name
		session['user_id'] = u_id
		session['user_role'] = u_role	
            	flash('You were logged in','success')
              	return redirect(url_for('main'))
	    else:
		flash('There was error, please try again','danger')
		return redirect(url_for('showSignIn'))
	else:
	    flash('Enter all required field','danger')
	    return redirect(url_for('showSignIn'))
    except Exception as e:
	flash(str(e),'danger')
	return redirect(url_for('showSignIn'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['user_role'] = 0
    flash('You were logged out','success')
    return redirect(url_for('main'))

@app.route("/add-data")
def add_data():
	conn = mysql.connect()
        cursor = conn.cursor()
	for i in range(0,11):
		time = "2017-05-17 %02d:00:00" % i
		if i%2 == 1:
			tem = 31.3
			moi = 18
		else:
			tem = 32.9
			moi = 17
		if i >5 and i<=13:
			sun = 410-(13-i)*35
		elif i>13 and i <19:
			sun = 150+(19-i)*31
		else:
			sun = 0
		fer = 11
        	sql = "INSERT INTO sensor_data (sunlight,moisture,temperature,fertility,time) VALUE ('%d','%d','%f','%d','%s')" % (sun,moi,tem,fer,time)
        	#cursor.execute(sql)
	#conn.commit()
	cursor.close()
	conn.close()
	return 'ok'

@app.route("/history",methods=['POST','GET'])
def history():
	if not session.get('logged_in'):
		flash('You need to sign in first','info')
		return redirect(url_for('showSignIn'))
	today = datetime.datetime.now().strftime("%Y-%m-%d")
        input_date = today
	conn = mysql.connect()
        cursor = conn.cursor()
        sql = 'SELECT * FROM plants_info WHERE id = 1'
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
                sun_b = row[2]
                sun_t = row[3]
                moi_b = row[4]
                moi_t = row[5]
                tem_b = row[6]
                tem_t = row[7]
                fer_b = row[8]
                fer_t = row[9]
        cursor.close()
        conn.close()
	if request.method == 'POST':
		report_type = request.form['select1']
		if report_type == '2':
			x=1
		elif report_type == '3':
			x=1
		elif report_type == '1':
			input_date = request.form['date1']
	tem = [0] * 24
	sun = [0] * 24
	moi = [0] * 24
	fer = [0] * 24
	conn = mysql.connect()
       	cursor = conn.cursor()
	sql = 'SELECT DATE(time) FROM sensor_data ORDER BY id LIMIT 1'
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		min_date = row[0]
     	sql = 'SELECT HOUR(time) AS hour,sunlight,moisture,temperature,fertility FROM sensor_data WHERE time LIKE \"' + input_date + '%\"' 
      	cursor.execute(sql)
      	results = cursor.fetchall()
     	for row in results:
		tem[row[0]] = row[3]
		sun[row[0]] = row[1]
		moi[row[0]] = row[2]
		fer[row[0]] = row[4]
	cursor.close()
	conn.close()
	sum_sun = 0
	min_moi = 0
	max_moi = 0
	min_tem = 0
	max_tem = 0
	min_fer = 0
	max_fer = 0
	for i in range(0,24):
		sun[i] = int(sun[i]*0.71/10.76)
		sum_sun += sun[i] 
		if moi[i] > max_moi:
			max_moi=moi[i]
		if moi[i] < min_moi:
                        min_moi=moi[i]
		if tem[i] > max_tem:
                        max_tem=tem[i]
		if tem[i] < min_tem:
                        min_tem=tem[i]
		if fer[i] > max_fer:
                        max_fer=fer[i]
		if fer[i] > min_fer:
                        min_fer=fer[i]
	return render_template('history.html',tem=tem,moi=moi,sun=sun,fer=fer,date=input_date,min_date=min_date,today=today,sun_b=sun_b,sun_t=sun_t,moi_b=moi_b,moi_t=moi_t,tem_b=tem_b,tem_t=tem_t,fer_b=fer_b,fer_t=fer_t,sum_sun=sum_sun,max_moi=max_moi,min_moi=min_moi,max_tem=max_tem,min_tem=min_tem,max_fer=max_fer,min_fer=min_fer)

if __name__ == "__main__":
#	schedule.every(60).seconds.do(read_data_job)
#   	t = Thread(target=run_schedule)
#    	t.start()
        app.run(host='0.0.0.0',use_reloader=False)
