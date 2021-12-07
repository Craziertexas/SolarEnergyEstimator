import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

class System:

    def __init__(self):
        print("Initiating...")
        self.LoadWeather()
        self.LoadANNs()
    
    def LoadWeather(self):
        self.Weather = pd.read_csv(r"Data/SolarEnergy/SolarData.csv")
        self.Weather = self.Weather.drop(["AC System Output (W)", "AC System Output (W)", "Size"], axis = 1)
        print("-------------Weather-------------")
        print(self.Weather.head())
        print("---------------------------------")
    
    def LoadANNs(self):
        with open(r"ANN/ConsumptionANN", 'rb') as ANN:
            self.ConsumptionANN = pickle.load(ANN)
        with open(r"ANN/GenerationANN", 'rb') as ANN:
            self.GenerationANN = pickle.load(ANN)
    
    def PerformanceInputs(self):
        ConsumptionInput = pd.read_csv(r"Inputs/XConsumption.csv")
        GenerationInput = pd.read_csv(r"Inputs/XGeneration.csv")
        return GenerationInput, ConsumptionInput
    
    def PerformanceOutputs(self):
        ConsumptionOutput = pd.read_csv(r"Inputs/YConsumption.csv")
        GenerationOutput = pd.read_csv(r"Inputs/YGeneration.csv")
        return GenerationOutput, ConsumptionOutput

    def PerformanceEvaluation(self):
        GInput, CInput = self.PerformanceInputs()
        GOutput, COutput = self.PerformanceOutputs()

        GPredict = self.GenerationANN.predict(GInput)
        CPredict = self.ConsumptionANN.predict(CInput)
        
        GPredict = np.array(GPredict)
        CPredict = np.array(CPredict)

        GPerf = pd.DataFrame()
        CPerf= pd.DataFrame()

        GPerf["Generation"] = GOutput
        GPerf["GenerationPredict"] = GPredict
        GPerf["ERROR"] = abs(GPerf["Generation"] - GPerf["GenerationPredict"])

        CPerf["Consumption"] = COutput
        CPerf["ConsumptionPredict"] = CPredict
        CPerf["ERROR"] = abs(CPerf["Consumption"] - CPerf["ConsumptionPredict"])

        GPerf.to_excel("Performance/Generation.xlsx")
        CPerf.to_excel("Performance/Consumption.xlsx")

        

Sys = System()
Sys.PerformanceEvaluation()

'''
Date = "2018-01-20"
HouseType = 1
Rus = 1
Evs = 1
HVAC = 1
Isolation = 1
Holyday = 1
Seed = 20
Size = 1

YMD = Date.split("-")
Date = 
'''