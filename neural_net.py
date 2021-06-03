import numpy as np
import pandas as pd


from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn.model_selection import train_test_split, cross_val_score

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

training = pd.read_csv('./dengue.csv')
testing = pd.read_csv('./test.csv')


# load the dataset
dataset = loadtxt('dengue_with_severity.csv', delimiter=',')
# split into input (X) and output (y) variables
X = dataset[:, 0:22]
y = dataset[:, 22]
model = Sequential()
model.add(Dense(22, input_dim=22, activation='relu'))
model.add(Dense(22, activation='relu'))
model.add(Dense(22, activation='relu'))
model.add(Dense(22, activation='relu'))
model.add(Dense(22, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam', metrics=['accuracy'])

model.fit(X, y, epochs=10, batch_size=1)
print(model.predict(
    [[1, 5, 1, 3, 1, 8, 1, 3, 1, 8, 1, 8, 1, 8, 0, 3, 1, 8, 1, 8, 0, 3]])[0][0])
# print(y)

model.save("./")
# # mapping strings to numbers
# le = preprocessing.LabelEncoder()
# le.fit(y)
# y = le.transform(y)

# x_train, x_test, y_train, y_test = train_test_split(
#     x, y, test_size=0.23, random_state=42)
# testx = testing[cols]
# testy = testing['prognosis']
# testy = le.transform(testy)


# clf1 = DecisionTreeClassifier()
# clf = clf1.fit(x_train, y_train)

# scores = cross_val_score(clf, x_test, y_test, cv=2)


# model = SVC()
# model.fit(x_train, y_train)


# # print(np.array(y_train))


# class NeuralNetwork():

#     def __init__(self):
#         # seeding for random number generation
#         np.random.seed(1)

#         # converting weights to a 3 by 1 matrix with values from -1 to 1 and mean of 0
#         self.synaptic_weights = 2 * np.random.random((13, 1)) - 1

#     def sigmoid(self, x):
#         # applying the sigmoid function
#         return 1 / (1 + np.exp(-x))

#     def sigmoid_derivative(self, x):
#         # computing derivative to the Sigmoid function
#         return x * (1 - x)

#     def train(self, training_inputs, training_outputs, training_iterations):

#         # training the model to make accurate predictions while adjusting weights continually
#         for iteration in range(training_iterations):
#             # siphon the training data via  the neuron
#             output = self.think(training_inputs.transpose())

#             # computing error rate for back-propagation
#             error = training_outputs.transpose() - output
#             # error = error.reshape(13, 33)
#             # print(error)
#             # performing weight adjustments
#             print(training_inputs.shape)
#             print((error * self.sigmoid_derivative(output)).shape)

#             # adjustments = np.dot(training_inputs, error *
#             #  self.sigmoid_derivative(output))

#             # self.synaptic_weights += adjustments
#             self.synaptic_weights += 0.2

#     def think(self, inputs):
#         # passing the inputs via the neuron to get output
#         # converting values to floats

#         inputs = inputs.astype(float)
#         output = self.sigmoid(np.dot(inputs, self.synaptic_weights))
#         return output


# if __name__ == "__main__":

#     # initializing the neuron class
#     neural_network = NeuralNetwork()

#     print("Beginning Randomly Generated Weights: ")
#     print(neural_network.synaptic_weights)

#     # training data consisting of 4 examples--3 input values and 1 output
#     training_inputs = x_train.to_numpy()

#     training_outputs = y_train.transpose()

#     # training taking place
#     neural_network.train(training_inputs, training_outputs, 1)

#     print("Ending Weights After Training: ")
#     print(neural_network.synaptic_weights)

#     user_input_one = str(input("User Input One: "))
#     user_input_two = str(input("User Input Two: "))
#     user_input_three = str(input("User Input Three: "))

#     print("Considering New Situation: ", user_input_one,
#           user_input_two, user_input_three)
#     print("New Output data: ")
#     print(neural_network.think(
#         np.array([user_input_one, user_input_two, user_input_three])))
#     print("Wow, we did it!")
