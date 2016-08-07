import sys
sys.path.append('/storage/.kodi/addons/python.RPi.GPIO/lib')
import xbmcaddon
import xbmcgui
import RPi.GPIO as GPIO
import time

def bin2dec(string_num):
    return str(int(string_num, 2))

GPIO.setmode(GPIO.BOARD)

starttime = time.time()
while (time.time()-starttime) < 5.0:
	try:
		data = []

		GPIO.setup(5,GPIO.OUT)
		GPIO.output(5,GPIO.HIGH)
		time.sleep(0.025)
		GPIO.output(5,GPIO.LOW)
		time.sleep(0.02)

		GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		for i in range(0,1000):
			data.append(GPIO.input(5))

		bit_count = 0
		count = 0
		HumidityBit = ""
		TemperatureBit = ""
		crc = ""

		while data[count] == 1:
			count = count + 1
		
		for i in range(0, 40):
			bit_count = 0

			while data[count] == 0:
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 8:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "1"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "1"
				if i>=32 and i<40:
					crc = crc + "1"
			else:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "0"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "0"
				if i>=32 and i<40:
					crc = crc + "0"
	   
		Humidity = bin2dec(HumidityBit)
		Temperature = bin2dec(TemperatureBit)
		
		if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
			break
	except:
		continue		
		
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

hello = "Hello Guys!"
if((time.time()-starttime) < 5.0):
	line2 = "Temperature: "+Temperature+"C"
	line3 = "Humidity: "+Humidity+"%"
else:
	line2 = "OMG, this is so embarrassing :("
	line3 = "I can't read the data!!!"
xbmcgui.Dialog().ok(addonname, hello, line2, line3)
