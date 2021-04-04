# import packages
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout

# Deep Model Used by the Agent
class Model:
    def __init__(self, state_size, action_size):
        # state_size -- input, action_size -- output
        self.state_size = state_size
        self.action_size = action_size

        # Build a neural network model and assign it to the variable self.model
        # e.g.  self.model = Sequential()
        # cause the size of state is just 4, a convnet seems not a good choice
        # fully connected multi-layered feed forward neural network can be considered
        self.model = Sequential([
            Dense(24, activation='relu', input_shape=(state_size, )),
            Dropout(0.2),
            Dense(24, activation='relu'),
            Dense(action_size, activation='linear')
        ])
        
    def _save_model(self):
        self.model.save_weights("weights_cartpoledqn.h5")
        
    def _load_model(self, file=None):
        self.model.load_weights(file if file is not None else "weights_cartpoledqn.h5")
 