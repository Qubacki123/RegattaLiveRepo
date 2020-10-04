#JZR 2020 TKIS PG
#
# Based on sample code and documentation from Waveshare website
# https://www.waveshare.com/sim7000e-nb-iot-hat.htm
# Also, based on Socket Programming in Python (Guide) by Nathan Jennings
# https://realpython.com/python-sockets/

#necessary library import
import serial
import time
import os
import socket

#socket definition
HOST = 'qubacki123.ct8.pl'
PORT = 4441

#serial port definition
ser = serial.Serial("/dev/ttyS0",115200)
ser.flushInput()

#variable definition
GNSS_is_on = False
recent_serial_answer = ''
timeGPS = ''
latitude = ''
longitude = ''
speed = ''
course = ''

def push_geo_data():
	global latitude, longitude
	
	message = longitude +','+ latitude
	message_b = message.encode('utf-8')
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			s.connect((HOST, PORT))
			s.sendall(message_b)
		except:
			print('!!! Cannot contact server !!!\n')
	
	

def send_at(command,back,timeout):
	""" 
		The function to send AT commands. 
  
		Parametres: 
			command (String): AT command to be sent.
			back (String): Expected answer from the command.
			timeout (Float): Time to be passed after sending the command.  
		  
		Returns: 
			0: Failed while communicating. 
			1: Received an empty answer.
			2: Received an expected answer.
	"""
	global recent_serial_answer
	
	#received message definition
	received = ''

	#actual sending of an AT command
	ser.write((command+'\r\n').encode())
	
	#timeout after sending the command
	time.sleep(timeout)
	
	#condition to check whether there is an answer from the serial port waiting to be read
	if ser.inWaiting():
			
		#reading of an answer and assigning it to the received variable
		received = ser.read(ser.inWaiting())
		recent_serial_answer = received.decode()
	
	#condition to check whether received answer is not an empty string
	if received != '':

		#condition to check whether the command resulted as expected 
		if back in received.decode():
			
			#correct answer as expected
			print('-----ANSWER-START--------------')
			#print(received.decode())
			print(str(recent_serial_answer))
			print('-----ANSWER-END----------------\n')
			return 2
		
		#incorrect answer - communication error
		else:						
			print(command + ' ERROR')
			print(command + ' back:\t' + received.decode())
			return 0
	
	#received an empty answer		
	else:	
		print('Received an empty answer')
		return 1


def turn_on_GNSS():
	""" 
		The function to turn on the GNSS receiver. 
  
		Parametres: 
			none 
		  
		Returns: 
			none
	"""
	print('\nTurning on the GNSS receiver...')
	print('..........Please wait..........\n\n')
	
	command_GNSS_on = 'AT+CGNSPWR=1'	
	answer = send_at(command_GNSS_on,'OK',0.5)
	global GNSS_is_on

	if answer == 2:
		print('\nAT+CGNSPWR=1 successfull\n')
		print('GNSS receiver is now active\n')
		GNSS_is_on = True    

	else:
		print('AT+CGNSPWR=1 ERROR\n')
		print('Could not turn on the GNSS receiver')
		GNSS_is_on = False
		
	time.sleep(2)

	
def GNSS_parser():
	""" 
		The function to parse information from NMEA. 
  
		Parametres: 
			message: most recent message from CGNSINF
		  
		Returns:
			prints output to console
	"""
	global latitude, longitude, course, speed, pdop, timeGPS
	
	message_split = recent_serial_answer.splitlines()
	
	for item in message_split:
		if 'CGNSINF:' in item:
			message_info = item
	
	
	message_parsed = message_info.split(',')
			
	#index at -1 relative to AT manual
	timeGPS = str(message_parsed[2])
	latitude = str(message_parsed[3])
	longitude = str(message_parsed[4])
	speed = str(message_parsed[6])
	course = str(message_parsed[7])
	pdop = str(message_parsed[11])
	
	if len(latitude)>3:
		push_geo_data()
		
			
	print('Time UTC: ' + timeGPS[8:10] + ':' + timeGPS[10:12] + ':' + timeGPS[12:14])
	print('Latitude: ' + latitude)
	print('Longitude: ' + longitude)
	print('Speed: ' + speed)
	print('Course: ' + course)
	
	
		
	

def get_GNSS_info():
	""" 
		The function to display NMEA messages. 
  
		Parametres: 
			none 
		  
		Returns: 
			False: Communication error.
	"""
		
	#defining loop to update GNSS information using a built-in command
	NMEA_loop = True	
	while NMEA_loop:
		
		
		
	
		answer = send_at('AT+CGNSINF','+CGNSINF',1)
		
		os.system('clear')
		print('-----ANSWER-START--------------')
		print(recent_serial_answer)
		print('-----ANSWER-END----------------\n')
		
		
		
		GNSS_parser()
		
		if answer == 2:
			
			#correct answer but no position fix
			if ',,,,,' in recent_serial_answer:
				print('GPS is not ready\n')
				print('\n*** PLEASE ADJUST THE ANTENNA ***\n')
				print('\n\nPress CTRL + C to exit')
				time.sleep(1)
				
			else:
				print('\n\nPress CTRL + C to exit')
		
		#answer different than 2 - error
		else:
			print('Error: %d'%answer)
			NMEA_loop = False
			return False
			
		
		
		
		


try:
	time.sleep(5)
	
	os.system('clear')
	
	turn_on_GNSS()

	#raw_input('\n\nHit ENTER to proceed...\n')
	
	os.system('clear')
	
	if GNSS_is_on:
		get_GNSS_info()
	else:
		print('GNSS receiver is off')	
	
	print('Exiting script.........')

except:
	if ser != None:
		ser.close()	
	
if ser != None:
		ser.close()
		
