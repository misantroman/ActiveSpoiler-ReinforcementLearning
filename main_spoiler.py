import numpy as np
from learners.NNLearner import NNLearner
from rl_games.ninja_castle import NinjaCastle



import os
if os.path.exists("datos_AcelX_PID.csv"):
    os.remove("datos_AcelX_PID.csv")
import RPi.GPIO as GPIO
from time import sleep,process_time
import smbus
import csv
print("iniciando")
sleep(70)# Initialization

servoPIN1 = 17 #direccion ruedas
servoPIN2 = 26 #inclinacion del aleron
servoPIN3 = 21 #Angulo de ataque
#pin 22 RAROOOOOOO
in1 = 24 #PH 24/23
in2 = 23
en = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
GPIO.setup(servoPIN3, GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)#  GPIO 25 for PWM with 1000Hz/ H bridge
d=GPIO.PWM(servoPIN1, 50)  #GPIO 17 for PWM with 50Hz
a=GPIO.PWM(servoPIN2, 50) # GPIO 26 for PWM with 50Hz
aa=GPIO.PWM(servoPIN3, 50) # GPIO 26 for PWM with 50Hz


#IMU registro
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B

GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)

def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
"""
def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        value=round(value,2)
        return value
""" 
def save_acc(ACCEL_XOUT_H,Ax_list): 
    #leer aceleraciones
    acc_x = read_raw_data(ACCEL_XOUT_H)
    Ax = acc_x/16384.0
    Ax_list.append(Ax)
    return

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
MPU_Init()





episode_num = 0

def load_policy():

def save_policy():

if __name__ == "__main__":
    game = Spoiler()
    learner = NNLearner(game)

    max_points= -9999   #max points achieved inizializer 
    first_max_reached = 0
    total_reward=0
	episodes = 0

	state = game.reset()
	reward, done = None, None
	iter=0
	while (done != True and iter<200):#10000
		#leer y ejecutar joystic
	    old_state = np.array(state)
	    next_action=learner.get_next_step(state,game)
	    state, reward, done = game.step(next_action)
		save_acc(ACCEL_XOUT_H,Ax_list)
	    learner.update(game,old_state, next_action, reward, state, done)

	    iter+=1

	reward10episodes += game.total_reward
	if game.total_reward > max_points:
	    max_points=game.total_reward
	    first_max_reached = played_games
	print("*** played_games[", played_games, "] Points[", game.total_reward,"]  Steps[", iter, "] MaxPoint[", max_points,"]")
		
	if (episode_num % 10) == 0:
		average10 = reward10episodes/10
	print('average reward last 10 episodes:', average10)

    print('played_games[',played_games,'] puntuacion Total[',total_rw,'] puntuacion máxima[',max_points,'] en[',first_max_reached,']')
    print(game.action_space.keys())
    learner.print_policy()


	p.ChangeDutyCycle(0)
	a.ChangeDutyCycle(6.25)
	aa.ChangeDutyCycle(11)
	print("stop motor")
	print("GPIO Clean up")
	print(Ax_list)
	sleep(3)
	GPIO.cleanup()
	print(Ax_list)
	from itertools import zip_longest
	export_data = zip_longest(Ax_list, fillvalue = '')
	with open('datos_AcelX_PID.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
		  wr = csv.writer(myfile)
		  wr.writerow(("Ax"))
		  wr.writerows(export_data)
	myfile.close()
