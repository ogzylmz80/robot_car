# !/usr/bin/env python
# coding:latin-1
# Autor:Ingmar Stapel, Modifikationen durch Oguz Yilmaz
# Datum:20190810/20200808
# Version: 1.1
# Homepage:https://custom-build-robots.com
# Dieses Programm ermoeglicht es, einen mobilen Roboter auf Basis eines Raspberry Pi
# über ein Web-Interface zu steuern

import sys, os, time, string
import L298NHBridge as HBridge

# importieren von Flask Bibliotheken
from flask import Flask, jsonify, render_template, request

# Weitere Module, die importiert werden koennen
sys.path.append("/home/pi/robot")

app = Flask(__name__)

# Ausschalten des Raspberry Pi
def shutdownPi():
    print("Shutting down...")
    os.system("sudo halt &")

# Reboten des Raspberry Pi
def rebootPi():
    print("Rebbooting...")
    os.system("sudo reboot &")

# Initialisierung der Variablen, die als global definiert sind
# speedRight, speedLeft: Geschwindigkeiten der linken und rechten Motoren
# accelIncrement, decelIncrement: Variablen für die inkrementelle Beschleunigung bzw. Bremsung
def initiate():
    global speedLeft
    global speedRight
    global accelIncrement
    global decelIncrement
    global error_msg
    error_msg  = ""
    speedLeft = 0
    speedRight = 0
    accelIncrement = 0.2
    decelIncrement = -0.2

# Die Entgegennahme von Befehlen, die über die Weboberfläche aufgerufen werden, wird über
# @app.route('<URL>') durch Flask realisiert.
# Anschließend wird jeder Befehl abgearbeitet und ermöglicht die Steuerung des Roboter-Autos

# Flask-Webserver
@app.route('/')
def index():
    return render_template('index.html')

# halt() fährt Pi runter
@app.route('/halt/', methods=['GET'])
def halt():
    shutdownPi()
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "Halt button pressed"}
    return jsonify(ret_data)

# reboot() startet Pi neu
@app.route('/reboot/', methods=['GET'])
def reboot():
    rebootPi()
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "Reboot button pressed"}
    return jsonify(ret_data)
    
# ButtonForward() lässt Roboter-Auto vorwärts fahren
@app.route('/forward/', methods=['GET'])
def ButtonForward():
    global speedLeft
    global speedRight
    
    # Das Roboter-Auto beschleunigt in Schritten von accelIncrement
    # bei jedem Tastendruck des Buttons bis maximal 100%. Dann fährt es maximal schnell vorwärts
    speedLeft = speedLeft + accelIncrement
    speedRight = speedRight + accelIncrement

    if speedLeft > 1:
        speedLeft = 1

    if speedRight > 1:
        speedRight = 1

    # Dem Programm L298NHBridge wird die Geschwindigkeit für
    # den linken und rechten Motor übergeben
    HBridge.setMotorLeft(speedLeft)
    HBridge.setMotorRight(speedRight)
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "FORWARD button pressed"}
    return jsonify(ret_data)
    
# ButtonBackward() lässt Roboter-Auto vorwärts fahren
@app.route('/backward/', methods=['GET'])
def ButtonBackward():
    global speedLeft
    global speedRight
    
    # Das Roboter-Auto bremst in Schritten von decelIncrement
    # bei jedem Tastendruck des Buttons bis maximal 100%. Dann fährt es maximal schnell rückwärts
    speedLeft = speedLeft + decelIncrement
    speedRight = speedRight + decelIncrement

    if speedLeft < -1:
        speedLeft = -1
        
    if speedRight < -1:
        speedRight = -1
        
    # Dem Programm L298NHBridge wird die Geschwindigkeit für
    # den linken und rechten Motor übergeben
    HBridge.setMotorLeft(speedLeft)
    HBridge.setMotorRight(speedRight)
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "BACKWARD button pressed"}
    return jsonify(ret_data)

# ButtonTurnLeft() lässt Roboter-Auto nach links fahren
@app.route('/left/', methods=['GET'])
def ButtonTurnLeft():
    global speedLeft
    global speedRight
    
    # Das Roboter-Auto bremst linken Motor und beschleunigt rechten Motor -> Linksfahrt
    # bei jedem Tastendruck des Buttons bis maximal 100%. Dann fährt es maximal schnell rückwärts
    speedLeft = speedLeft + decelIncrement
    speedRight = speedRight + accelIncrement
    
    if speedLeft < -1:
        speedLeft = -1
        
    if speedRight > 1:
        speedRight = 1
        
    # Dem Programm L298NHBridge wird die Geschwindigkeit für
    # den linken und rechten Motor übergeben
    HBridge.setMotorLeft(speedLeft)
    HBridge.setMotorRight(speedRight)
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "LEFT button pressed"}
    return jsonify(ret_data)

# ButtonTurnRight() lässt Roboter-Auto nach rechts fahren
@app.route('/right/', methods=['GET'])
def ButtonTurnRight():
    global speedLeft
    global speedRight
    
    # Das Roboter-Auto bremst den rechten Motor und beschleunigt linken Motor -> Rechtsfahrt
    # bei jedem Tastendruck des Buttons bis maximal 100%. Dann fährt es maximal schnell rückwärts
    speedLeft = speedLeft + accelIncrement
    speedRight = speedRight + decelIncrement
    
    if speedLeft > 1:
        speedLeft = 1
        
    if speedRight < -1:
        speedRight = -1
        
    # Dem Programm L298NHBridge wird die Geschwindigkeit für
    # den linken und rechten Motor übergeben
    HBridge.setMotorLeft(speedLeft)
    HBridge.setMotorRight(speedRight)
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "RIGHT button pressed"}
    return jsonify(ret_data)

# ButtonStop() stoppt das Roboter-Auto
@app.route('/stop/', methods=['GET'])
def ButtonStop():
    global speedLeft
    global speedRight
    
    # Das Roboter-Auto stoppt. Beide Mototen auf 0
    speedLeft = 0
    speedRight = 0
        
    # Dem Programm L298NHBridge wird die Geschwindigkeit für
    # den linken und rechten Motor übergeben
    HBridge.setMotorLeft(speedLeft)
    HBridge.setMotorRight(speedRight)
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"value": "STOP button pressed"}
    return jsonify(ret_data)

# Die Funktion status() definiert die Meldungen, die das Roboter-Auto and die Weboberflaeche
# zurueckgibt. Hier waere es auch möglioch die Werte von weiteren Sensoren (Sense HAT, ToF-Sensor)
@app.route('/status/', methods=['GET'])
def status():
    global speedLeft
    global speedRight
    global error_msg
    
    # Anzeigen der linken und rechten Geschwindigkeit, auf 2 Stellen gerundet
    display_speedl = round(speedLeft,2)
    display_speedr = round(speedRight,2)
    
    if error_msg == "":
        error_msg = ("No error!")
    
    # Mit diesem Aufruf wird an die Web-Oberfläche, die Info gegeben,
    # welcher Button zuletzt gedrückt wurde
    ret_data = {"speedl": display_speedl, "speedr": display_speedr, "error_msg": error_msg}
    return jsonify(ret_data)

# Aufruf der Initialisierungs-Funktion
initiate()

# Start des Flask-Webservers mit dem Port 8181
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=False)

# Ende des Programs#
