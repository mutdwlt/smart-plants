# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, flash, session, render_template, json, request
from flask.ext.mysql import MySQL
from gattlib import GATTRequester, GATTResponse
import RPi.GPIO as GPIO
import datetime
from struct import *
import schedule,time

mysql = MySQL()
app = Flask(__name__)
app.secret_key = "super secret key"
app.debug = True

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'raspberry'
app.config['MYSQL_DATABASE_DB'] = 'miflora'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#setup schedule task
def read_data_job():
	if not session.get('mac'):
		conn = mysql.connect()
                cursor = conn.cursor()
                sql = "SELECT * FROM plants_info WHERE id = 1"
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                   	session['mac'] = row[0]
               	cursor.close()
              	conn.close()
	address=session['mac']
	try:
		requester = GATTRequester(address)
		data=requester.read_by_handle(0x0035)[0]
        	temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
        	temperature=float(temperature/10);
		conn = mysql.connect()
                cursor = conn.cursor()
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql = "INSERT INTO sensor_data (sunlight,moisture,temperature,fertility,time) VALUES ('%d','%d','%f','%d','%s')" % (sunlight,moisture,temperature,fertility,now)
                cursor.execute(sql)
		conn.commit()
                cursor.close()
                conn.close()
	except:
		conn = mysql.connect()
                cursor = conn.cursor()
		sql = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1"
		cursor.execute(sql)
		results = cursor.fetchall()
              	for row in results:
			sunlight = row[1]
			moisture = row[2]
			temperature = row[3]
			fertility = row[4]
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql = "INSERT INTO sensor_data (sunlight,moisture,temperature,fertility,time) VALUES ('%d','%d','%f','%d','%s')" % (sunlight,moisture,temperature,fertility,now)
                cursor.execute(sql)
                conn.commit()
                cursor.close()
                conn.close()
			
#schedule.every(2).minutes.do(read_data_job)
#while True:
#	schedule.run_pending()
#    	time.sleep(1)


@app.route('/',methods=['GET', 'POST'])
def main():
	if request.method == 'POST':
		if not session.get('mac'):
                	conn = mysql.connect()
                	cursor = conn.cursor()
                	sql = "SELECT * FROM plants_info WHERE id = 1"
                	cursor.execute(sql)
                	results = cursor.fetchall()
                	for row in results:
                        	session['mac'] = row[0]
                	cursor.close()
                	conn.close()
		address = session['mac']
		address = "C4:7C:8D:60:93:25"
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
			temperature=float(temperature/10);
			session['tem']=temperature
			session['sun']=sunlight
			session['moi']=moisture
			session['fer']=fertility
			session['time']=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			session['battery']=battery
			session['firmware']=version
			flash('Data updated successfully','success')
		except:
			flash('Could not update sensor value, please try again','danger')
		return render_template('index.html')
	else:
		if not session.get('plants_name'):
			conn = mysql.connect()
                        cursor = conn.cursor()
                        sql = "SELECT * FROM plants_info WHERE id = 1"
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        for row in results:
                                session['plants_name'] = row[1]
			cursor.close()
			conn.close()
		if not session.get('time'):
			conn = mysql.connect()
                	cursor = conn.cursor()
                	sql = "SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1"
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
                      	session['tem']=data_tem
                      	session['sun']=data_sun
                       	session['moi']=data_moi
                      	session['fer']=data_fer
                      	session['time']=data_time
		return render_template('index.html')

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
        cursor.close()
        conn.close()	
	return render_template('plants.html',mac_address=mac_address,plants_name=plants_name,sun_b=sun_bottom,sun_t=sun_top,moi_b=moi_bottom,moi_t=moi_top,tem_b=tem_bottom,tem_t=tem_top,fer_b=fer_bottom,fer_t=fer_top)

@app.route('/editSensor',methods=['GET', 'POST'])
def editSensor():
	if not session.get('logged_in'):
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
        if not session.get('logged_in'):
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
		session['plants_name'] = n_plants_name
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
        flash(str(e))
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
	    cursor.close()
            conn.close()
	    if _password == u_password:
		session['logged_in'] = True
		session['name'] = u_name
		session['user_id'] = u_id
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
	if request.method == 'POST':
		report_type = request.form['select1']
		if report_type == '2':
			x=1
		elif report_type == '3':
			x=1
		elif report_type == '1':
			input_date = request.form['date1']
	tem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	sun = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	moi = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	fer = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
	return render_template('history.html',tem=tem,moi=moi,sun=sun,fer=fer,date=input_date,min_date=min_date,today=today)



if __name__ == "__main__":
        app.run(host='0.0.0.0')
