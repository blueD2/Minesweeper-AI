# import the necessary modules for your ANN below:
# For instance: import numpy as np
import numpy as np

class ANN(object):
    def __init__(self, num_inputs, num_hidden_nodes0, num_hidden_nodes1, num_outputs, weights):
        self.weights = weights 
        num_hidden_weights0 = (num_inputs+1) * num_hidden_nodes0
        num_hidden_weights1 = (num_hidden_nodes0+1) * num_hidden_nodes1
        self.hidden_weights0 = np.array(self.weights[:num_hidden_weights0]).reshape(num_hidden_nodes0,num_inputs+1)
        self.hidden_weights1 = np.array(self.weights[num_hidden_weights0:num_hidden_weights0+num_hidden_weights1]).reshape(num_hidden_nodes1,num_hidden_nodes0+1)
        self.output_weights = np.array(self.weights[num_hidden_weights0+num_hidden_weights1:]).reshape(num_outputs,num_hidden_nodes1+1)

    def activation(self,x):
        # x is the net input to the neuron (previously represented as "z" during the class)
        # a is the activation value ( a = activation(z) )
        # activation function could be sigmoid function: 1/(1+exp(-x))
        a = 1/(1+np.exp(-x))
        return a

    def evaluate(self,inputs):
        # Compute outputs from the fully connected feed-forward ANN:
        # So basically, you will perform the operations that you did on HW4:
        # Let's assume that you have one hidden layer with 2 hidden nodes. Then you would have
        # a matrix of weights (first layer of weights beetween the input and hidden layers) of
        # size: 2 x (4+1)=2 x 10, and another matrix of weights (second layer between the hidden
        # layer and the output layer) of size: 2 x (2+1) = 6, resulting in total of 16 weights.
        # First, compute z(2) vector which is 2-by-1:
        # z(2,1) = +1 x weight[0] + x(1) x weight[1] + ... + x(4) x weight[4]
        # z(2,2) = +1 x weight[5] + x(1) x weight[6] + ... + x(4) x weight[9]
        # a(2,1) = activation(z(2,1))
        # a(2,2) = activation(z(2,2))

        #need to dot a 1 x inputs + 1 array with a hidden weights x hidden nodes matrix => 1 x hidden nodes array with outputs
        inputs.append(1)#why does this work
        hiddenNodeWeights0 = self.hidden_weights0.transpose()
        hiddenValues0 = np.dot(inputs, hiddenNodeWeights0 )
        hiddenOutputs0 = []
        for x in hiddenValues0:
            hiddenOutputs0.append( self.activation( x ) )
        #bias value
        hiddenOutputs0.append(1)
        
        hiddenNodeWeights1 = self.hidden_weights1.transpose()
        hiddenValues1 = np.dot(hiddenOutputs0, hiddenNodeWeights1 )
        hiddenOutputs1 = []
        for x in hiddenValues1:
            hiddenOutputs1.append( self.activation( x ) )
        #bias value
        hiddenOutputs1.append(1)
        
        #should result in a 1 x hidden nodes matrix with the output from each node
        outputNodeWeights = self.output_weights.transpose()
        outputValues = np.dot(hiddenOutputs1, outputNodeWeights )
        outputs = []
        for y in outputValues:
            outputs.append( self.activation( y ) )

        return outputs
        


