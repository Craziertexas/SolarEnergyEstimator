import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from datetime import datetime

#Cargar Datos
with open(r"Data/SolarEnergy/SolarData.csv") as file:
    Data = pd.DataFrame(pd.read_csv(file, sep = ","))

print("-----------------Generation Data-----------------")
print(Data.info())
print("-------------------------------------------------")

Data = Data.astype(np.float64)

#Correlacion de datos
Correlacion = Data.corr()
sns.heatmap(Correlacion, annot = True)
plt.title("Matriz de Correlaciones")
plt.figure(1)
plt.show()

#NormalizedData = (Data - Data.min())/(Data.max() - Data.min())

XData = Data.drop(["AC System Output (W)", "DC Array Output (W)", "Day", "Hour","Month"], axis = 1)
YData = Data["AC System Output (W)"]

XTrain, XTest, YTrain, YTest = train_test_split(XData,YData, test_size = 0.5)

XTest.to_csv(r"Inputs/XGeneration.csv", index = False)
YTest.to_csv(r"Inputs/YGeneration.csv", index = False)

print("-----------------ANN Parameters-----------------")
print("Input: ")
print(XTrain.head())
print("------------------------------------------------")
print("Output: ")
print(YTrain.head())
print("------------------------------------------------")

ANN = MLPRegressor(random_state = 231, max_iter = 1000, hidden_layer_sizes = [50], 
                   shuffle = True, verbose = True, tol = 0.000001, n_iter_no_change = 20)
                   
ANN.fit(XTrain, YTrain)

YScore = ANN.score(XTest, YTest)
print(YScore)

YPredict = ANN.predict(XTest)
YError = metrics._regression.mean_absolute_error(YTest, YPredict)
print(YError)

#pickle.dump(ANN, open(r"ANN/GenerationANN", "wb"))
