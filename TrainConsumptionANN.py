import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from datetime import datetime
from sklearn import metrics

#Cargar Data
with open(r"Data/HouseHold/HouseData.csv") as file:
    Data = pd.read_csv(file, sep = ",")
    Data = Data.dropna(how = "any", axis = 0)
    Data = Data.drop(["Region", "Facing", "House"], axis = 1)

#Fecha a dia del año
for Date in Data["date"].unique():
    YMD = Date.split("-")
    Dt = datetime(int(YMD[0]),int(YMD[1]),int(YMD[2])).timetuple().tm_yday
    Data.loc[Data["date"] == Date, "date"] = Dt

#Semilla de medicion
for ID in Data["ID"].unique():
    BufferID = Data.loc[Data["ID"] == ID]
    for index in BufferID.index:
        Data.loc[[index],'Seed'] = (BufferID['Energy_KWH'].sample()).values[0]

Data = Data.astype(float)

print("-----------------Consumption Data-----------------")
print(Data.info())
print(Data.head())
print("--------------------------------------------------")

#Correlacion
Correlacion = Data.corr()
sns.heatmap(Correlacion, annot = True)
plt.title("Matriz de Correlaciones")
plt.figure(1)
plt.show()

#NormalizedData = (Data - Data.min())/(Data.max() - Data.min())

XData = Data.drop(["Energy_KWH", "ID"], axis = 1)
YData = Data["Energy_KWH"]

XTrain, XTest, YTrain, YTest = train_test_split(XData, YData,test_size = 0.3)

XTest.to_csv(r"Inputs/XConsumption.csv", index = False)
YTest.to_csv(r"Inputs/YConsumption.csv", index = False)

print("-----------------ANN Parameters-----------------")
print("Input: ")
print(XTrain.head())
print("------------------------------------------------")
print("Output: ")
print(YTrain.head())
print("------------------------------------------------")

ANN = MLPRegressor(random_state = 231, max_iter = 100000, hidden_layer_sizes = [1371], 
                   shuffle = True, verbose = True, tol = 0.0000001, n_iter_no_change = 20)

ANN.fit(XTrain, YTrain)

YScore = ANN.score(XTest, YTest)
print("R²: " + str(YScore))

YPredict = ANN.predict(XTest)
YError = metrics._regression.mean_absolute_error(YTest, YPredict)
print("Error: " + str(YError))

#pickle.dump(ANN, open(r"ANN/ConsumptionANN", "wb"))