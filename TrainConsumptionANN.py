import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from datetime import datetime

#Cargar Data
with open(r"Data\HouseHold\HouseData.csv") as file:
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

print("-----------------Training Data-----------------")
print(Data.info())
print(Data.head())
print("-----------------------------------------------")

#Correlacion
Correlacion = Data.corr()
sns.heatmap(Correlacion, annot = True)
plt.title("Matriz de Correlaciones")
plt.figure(1)
plt.show()

NormalizedData = (Data - Data.min())/(Data.max() - Data.min())

print("-----------------Normalized Data-----------------")
print(NormalizedData.info())
print(NormalizedData.head())
print("-----------------------------------------------")

XTrain, XTest, YTrain, YTest = train_test_split(NormalizedData.drop(["Energy_KWH", "ID"], axis = 1),
                                                NormalizedData["Energy_KWH"], test_size = 0.3)
print(XTrain.head())

ANN = MLPRegressor(random_state = 231, max_iter = 100000, hidden_layer_sizes = [20,1000,20], shuffle = True, verbose = True, tol = 0.0000001, n_iter_no_change = 100)
ANN.fit(XTrain, YTrain)

YPredict = ANN.score(XTest, YTest)
print(YPredict)

pickle.dump(ANN, open(r"ANN\ConsumptionANN", "wb"))