
import RPi.GPIO as GPIO
import time
import read_load

motor_map = {
	1: 16,
	2: 20,
	3: 19,
	4: 26
}

GPIO.setmode(GPIO.BCM)

for val in motor_map.values():
	GPIO.setup(val, GPIO.OUT)
	
def get_fill():
	res = read_load.getLoad()/-2570.0
	return res

def disp(args):
        print args
	try:
		if sum([arg[1] for arg in args]) > 1:
			raise Exception("Drink proportions add up to more than 100%!")
		for drink, part in args:
			if drink < 1 or drink > 4:
				raise Exception("Invalid drink given ({0})".format(drink))
		read_load.init()
		
		total = 0.0
		
		for drink, part in args:
			print("dispensing {0}% of drink {1}".format(part*100, drink))
			GPIO.output(motor_map[drink], 1)
			while get_fill() < total + part:
				pass
			GPIO.output(motor_map[drink], 0)
			time.sleep(1)
			total += part
		
		print("Done.")
	except:
		for val in motor_map.values():
			GPIO.output(val, 0)
		raise
	
	
