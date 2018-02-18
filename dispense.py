
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
	try:
		if sum([part for drink, part in args]) > 1:
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

def disp2(*args):
	try:
		if sum([part for (drink, part) in args]) > 1:
			raise Exception("Drink proportions add up to more than 100%!")
		for drink, part in args:
			if drink < 1 or drink > 4:
				raise Exception("Invalid drink given ({0})".format(drink))
		read_load.init()
		
		total = 0.0
		
		drink = []
		for (d, part) in args:
			drink.append([d, part, part*len(args)])
			
		while drink:
			target = 1
			num_drinks = len(drink)
			for (d, p, true_p) in drink:
				if true_p < target:
					target = true_p
				GPIO.output(motor_map[d], 1)
			
			while get_fill() < target:
				pass
			
			new_drink = []
			for (d, p, true_p) in drink:
				if true_p <= target:
					GPIO.output(motor_map[d], 0)
				else:
					new_p = p - target/num_drinks
					new_drink.append([d, new_p, 0])
			for i in range(len(new_drink)):
				new_drink[i][2] = new_drink[i][1]*len(new_drink) + target
				
			drink = new_drink
		print("Done.")
	except:
		for val in motor_map.values():
			GPIO.output(val, 0)
		raise
	
	
