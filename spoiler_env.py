import random as rdm
import numpy as np
import os.path
from tensorflow.keras.models import load_model

Action_space =(Ang_pos, Ang_neg, hold_on)

class Spoiler:
	
    def __init__(self):
    	#spoiler
		self.min_position = 4.25  #spoiler
		self.max_position = 8.25
		self.cero_ang = 6.25
		self.speed = 0.1
		self.action_range = 4/0.1
		#acc imu
		self.acc_range = 4/0.01
		self.threshold = 0.15 #0.15g acceleration
		self.danger_thres = 0.65 #revisar para meter en funcion de rewards
		#state
        self.state = np.array([6.25	,0]) #[position en unidades de duty,acc rounded to 0.01 [g]] INITIAL STATE
		self.total_states = int(action_range * acc_range)
		self.positions_space = np.array([])	
		#actions space
        self.action_space = {'Ang_pos': np.array[self.speed, 0]),
                             'Ang_neg': np.array[-self.speed,0]),
                             'hold_on': np.array[0,0]),
                            }

		#rewards & punishments
        self.step_penalization = [0.1,-0.5,-5]
		self.danger_punishment = -20 #enter danger zone  #revisar donde lo metemos
		self.terminal_rewards = [300, -300]   #[winingstate,loosingstate]  #modificar main.

		#counters       
		self.total_reward = 0
		self.total_it = 0
		self.total_winning_it = 0
		#if winning it = 0.9 total_it then winning state

    def reset(self):
        self.total_reward = 0
        self.total_it = 0
		self.total_winning_it = 0
        self.state = [6.25,0]   #set aileron and acc to zero
        return self.state
	
	def send_position_2_servo(self, state[0]):
		 d.ChangeDutyCycle(state[0])

    def get_acc(self,addr):#read IMU
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        value= round(value/16384,2)		#round acc to 2 decimals
		self.state[1] = value		#round acc to 2 decimals
        return self.state[1]


	def terminal_state(self, done):   #esta dentro del step
		if self.total_winning_it >= 0.8*self.total_it:
			self.total_reward += self.terminal_rewards[0]  
			print("winning episode")
		else:
			self.total_reward += self.terminal_rewards[1]  
			print("loosing episode")
	return self.total_reward
		
    def step(self, action):
        self._apply_action(action)
        self.get_acc() #puede ir dentro de apply action
        self.get_reward()
        if p == 0:   #ajustar a variable de duty cycle del motor dc
        	done == True
        	self.terminal_state(done)
        else: done == False # final revisar donde poner done, sera cuando carro pare
        return self.state,reward , done

    def _apply_action(self, action):   #podria ser con el diccionario
		self.state[0] += self.action_space[action]
		"""
		if action == 'Ang_pos':
			self.state[0] += speed
		elif action == 'Ang_neg':
			self.state[0] -= speed
		elif action == 'hold_on':
			self.state[0] += 0
		"""
		self.state[0] = np.clip(self.state[0], self.min_position, self.max_position) #clip limits
		self.send_position_2_servo() #mandar al servo el nuevo estado
		#llamar funcion de leer acc para devolver el edo completo
		return state
		
	def get_reward(self, state[1]#acceleration):
		acc = abs(state[1])
		self.total_it += 1  				 #tienen que reiniciarse
		if acc < self.threshold:             #winning
			reward = self.step_penalization[0]  
			self.total_winning_it += 1
		elif acc > self.threshold and acc < self.danger_threshold:
			reward = self.step_penalization[1] 
		else:							#loosing
			entering_loosing = 1
			reward = self.step_penalization[2] 
			if self.entering_loosing == 1:   #happens just once
				entering_loosing +=1
				reward += self.danger_punishment

		self.total_reward += reward
		return 	self.total_reward, reward
		


