#!/usr/bin/python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient   # importing the AWSIotMQTTclient library
import time                                      #importing the time library
from subprocess import check_output            #importing the check_output function from the subprocess library
from re import findall                    #importing the find all function from re library


messageIn = "empty"    #initializing variable messageIn to "empty"


#function to print the receieved MQTT message and store the payload in the messageIN variable
def customCallback( client, userdata, message ):
	print( "From Topic: ")
	print( message.topic )
	print( "Message: " )
	print( message.payload )
	global messageIn
	messageIn = message.payload

#function to get the CPU temperature of the raspberry pi

def get_temp():
        temp = check_output(["vcgencmd", "measure_temp"]).decode("UTF-8")
        return(findall("\d+\.\d+",temp)[0])


#intializing the AWSIoTMQTTClient instance

myMQTTClient = AWSIoTMQTTClient("MyRaspberryPi")


#configuring the endpoint,certificates,and other settings for the AWSIoTMQTTclient instance
myMQTTClient.configureEndpoint("awromsl3r8g0c-ats.iot.ca-central-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("AmazonRootCA1.pem", "351c291b4881636ae18a62fb5a45d7595708a2d2e75b42d8a64efcb6700c9214-private.pem.key","351c291b4881636ae18a62fb5a45d7595708a2d2e75b42d8a64efcb6700c9214-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

#Establishing a connection with AWS IoT and subscribing to a topic with custom callback function
myMQTTClient.connect()
myMQTTClient.subscribe("sdkTest/sub", 1, customCallback)

#publishing the CPU temperature to a topic and waiting for 5 sec
while messageIn != "quit":
	value = get_temp()
	myMQTTClient.publish("sdkTest/pub", "CPU Temp is " +  value + "℃", 0)
	time.sleep(5)


