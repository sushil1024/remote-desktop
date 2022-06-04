'''
Author's Name: 	Sushil Waghmare,
				Siddhesh Pokharkar,
				Shubham Jadhav
Institute's Name: Annasaheb Chudaman Patil College of Engineering, Kharghar, Navi Mumbai.
Subject: Major Project
Department: Computer Engineering
Academic Year: 2021-22
'''

import pyautogui
from flask import render_template, request, Flask, Response, jsonify
from flask_mysqldb import *
from camera_desktop import Camera


app = Flask(__name__)


# database connector
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'r00t'
app.config['MYSQL_DB'] = 'remotedesktop'

mysql = MySQL(app)


# home page
@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


# To determine IP address of the user using the application
@app.route('/usercred', methods=['GET', 'POST'])
def userc():

	# ip address of the unique device
	ip = request.remote_addr
	cur = mysql.connection.cursor()

	# searches for detail of the current ip in the database
	res = cur.execute("SELECT * FROM user WHERE ip = %s;", [ip])

	# if details not found, enter
	if res == 0:

		# to generate random password
		from randpass import genpass

		# infinite loop until 'res' = 1
		while True:
			res = cur.execute("INSERT INTO user VALUES(ROUND((RAND() * (100-1))+1), %s, %s, %s);", [ip, ip, genpass()])

			if res == 1:
				break

	# fetches the details from the database
	cur.execute("SELECT userKey, password FROM user WHERE ip = %s;", [ip])
	mysql.connection.commit()
	data = cur.fetchone()
	cur.close()

	# displays the details on the output screen or web app
	return jsonify(data)


# main remote control access
@app.route('/event', methods=['GET'])
def index():
	return render_template('index.html')


# get frames of every event/activity
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


# video feeds of continuous frames
@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/mouse', methods=['POST'])
def mouse_event():
	# co-ordinates of browser image event
	ex, ey = float(request.form.get('x')), float(request.form.get('y'))
	# size of browser image
	imx, imy = float(request.form.get('X')), float(request.form.get('Y'))
	# size of desktop
	dx, dy = pyautogui.size()
	# co-ordinates of desktop event
	x, y = dx*(ex/imx), dy*(ey/imy)
	# mouse event
	event = request.form.get('type')

	if event == 'click':
		pyautogui.click(x, y)
	elif event == 'dblclick':
		pyautogui.doubleClick(x, y)
	elif event == 'rightclick':
		pyautogui.click(x, y, button='right')

	return Response("success")


@app.route('/keyboard', methods=['POST'])
def keyboard_event():
	# keyoard event
	event = request.form.get('type')
	print(event)
	if event == "text":
		text = request.form.get("text")
		pyautogui.typewrite(text)
	else:
		pyautogui.press(event)
	return Response("success")


if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True, debug=True)
