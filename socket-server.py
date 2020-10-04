#!/usr/bin/env python3
#
# Based on Socket Programming in Python (Guide) by Nathan Jennings
# https://realpython.com/python-sockets/
# Huge thanks to this author for a very good tutorial!


import socket
import json

HOST = 'qubacki123.ct8.pl'  # Standard loopback interface address (localhost)
PORT = 4441       # Port to listen on (non-privileged ports are > 1023)

def saveJSON(Longitude,Latitude):
  json_data = {
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [Longitude, Latitude]
  },
  "properties": {
    "name": "Yacht1"
  }}	

  with open('json_data.json', 'w') as outfile:
            json.dump(json_data, outfile)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print('\nConnected by', addr)            
            data = conn.recv(1024)
            print('Received:', repr(data))
            message = data.decode('utf-8')
            
            coords = message.split(',')
          
            lon = float(coords[0])
            lat = float(coords[1])

            print('Longitude: ' + coords[0])
            print('Latitude: ' + coords[1])
            
            saveJSON(lon,lat)

            if not data:
                break
            #conn.sendall(data)
                

