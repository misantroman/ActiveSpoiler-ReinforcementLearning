import random
import os.path
from keras import Sequential
from keras.layers import Dense#, np
from keras.optimizers import Adam

	
class NNLearner():
    def __init__(self,game):
        self.state_size = (game.total_states)
        self.action_size = len(game.action_space)
        self.memory = list()#deque(maxlen=5000)
        self.max_memory = 5000
        self.learning_rate = 0.1    # discount factor 
        self.ratio_explotacion = 0.5 #inizialice, ends at 0.93 after 300 episodes
        self.exploration_min = 0.07
        self.exploration_decay = 0.9935 
        self.model_learning_rate = 1e-4  # learningr rate factor for adam 
        self.discount_factor = 0.1
        self.model = self._crear_modelo()
        self.game = game
        self.update_iteration=0

    def _crear_modelo(self):
		#check if theres a saved model of the NN
		if os.path.isfile('documents/spoiler_model.h5') is False:
			print('first time, no saved model,create one from scratch')
		    model = Sequential()  #le cambiamos el inicializador a uno uniforme?
		    model.add(Dense(16, input_shape=self.state_size, activation='relu')) #revisar si cambiamos el input directo al edo
		    model.add(Dense(32, activation='relu'))
		    model.add(Dense(16, activation='relu'))
		    model.add(Dense(self.action_size, activation='linear')) #activation=softmax
		    model.compile(loss='mse', optimizer=Adam(lr=self.model_learning_rate)) #loss=categorical_crossentropy  optimizer=sgd
		else:
			model = load_model('documents/spoiler_model.h5')
			model.summary()
			model.get_weights()
        return model

    def update(self, game, old_state, action, reward, state, done): #se cambio reached endxdone
		self.update_iteration+=1
        if done or self.update_iteration>=999:  # entrenamos si acabo epoch (if done cambiar por reached end)
			#apagara motor
            self.remember(old_state, action, reward,
                          state, done)
            self.aprendizaje(min(150,len(self.memory)))
            self.update_iteration=0 #reiniciar a cero update iteration

        else:
            # guardamos entrenamiento
            self.remember(old_state, action, reward,
                          state, done)

    def remember(self, old_state, action, reward, state, done):   #next step new state
        self.memory.append((self.prepare_state(old_state), self.prepare_action(action), reward, self.prepare_state(state), done))
        if len(self.memory) > self.max_memory:
            del self.memory[0] # se quita el primero

    def get_next_step(self, state, game):
        next_step = np.random.choice(list(game.action_space)) #choose a random action
        if np.random.uniform() <= self.ratio_explotacion:     #if un valor aleatoria dentro del rango del ratio de explotacion es TRUE explota!
            q = self.model.predict(self.prepare_state(state)) # predice el q y ESCOGE UNA ACCION DE ACUERDO A POLICY
            idx_action = np.argmax(q[0])          #no deberia ser solo una q? #revisar si es lineal o softmax
            next_step = list(game.action_space)[idx_action]   # si no has una acion aleatoria escogida previamente
        return next_step

    def aprendizaje(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        minibatch.append(self.memory[-1]) # final estate
        for state, action, reward, next_state, done in minibatch:
            actual_q_value_options = self.model.predict(state)
            actual_q_value = actual_q_value_options[0][action]  #creo que borrar 0
            future_max_q_value = reward
            if not done:
                future_max_q_value = reward + self.discount_factor*np.amax(self.model.predict(next_state)[0])

            actual_q_value_options[0][action] = actual_q_value + self.learning_rate*(future_max_q_value - actual_q_value)
            self.model.fit(state, actual_q_value_options, epochs=1, verbose=0)
			model.save('documents/spoiler_model.h5')
        # change exploration rate
        if 1-self.ratio_explotation > self.exploration_min:
            ratio_exploration = 1-self.ratio_explotation
            ratio_exploration *= self.exploration_decay
            self.ratio_explotation = 1- ratio_exploration

    def prepare_state(self, state):  # 2d to list 
        array_1d = np.zeros(self.state_size)
		state1[0] = interp(state1[0], [4.25,8.25],[0,40])
		state1[1] = interp(state1[1], [-2,2],[0,400])
        idx = int((state1[0])*(state1[1]))#te da la posicion del edo, poniendo los edos como una lista del tmaño de todos los posibles edos
        array_1d[idx] = 1 #le asigna un uno a esa posicion
        return (array_1d.reshape((1, -1)))

    def prepare_action(self, action_taken):
        return (list(self.game.action_space).index(action_taken))

