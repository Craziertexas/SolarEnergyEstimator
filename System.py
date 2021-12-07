import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import calendar

class System:

    def __init__(self):
        print("Initiating...")
        self.LoadWeather()
        self.LoadANNs()
    
    def LoadWeather(self):
        self.Weather = pd.read_csv(r"Data/SolarEnergy/SolarData.csv")
        self.Weather = self.Weather.drop(["AC System Output (W)", "DC Array Output (W)"], axis = 1)
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

        GPerf.to_excel(r"Performance/Generation.xlsx")
        CPerf.to_excel(r"Performance/Consumption.xlsx")
    
    def PredictGeneration(self, Input):
        Date = Input["date"]
        Size = Input["Size"]

        Date = Date.split("-")
        Day = int(Date[2])
        Month = int(Date[1])

        Input = self.Weather.loc[(self.Weather["Day"] == Day)&(self.Weather["Month"] == Month)&(self.Weather["Size"] == 1)].copy()
        Input = Input.drop(["Day", "Month", "Size", "Hour"], axis=1)
        Input.insert(5, "Size", Size)

        Predictions = self.GenerationANN.predict(Input)

        Generation = 0
        for Prediction in Predictions:
            Generation = Generation + Prediction

        Generation = Generation/1e3

        return Generation
    
    def PredictConsumption(self, Input):

        YMD = Input["date"].split("-")
        Input["date"] = datetime(int(YMD[0]),int(YMD[1]),int(YMD[2])).timetuple().tm_yday

        Features = pd.DataFrame()
        Features = Features.append(Input, ignore_index=True)
        Features = Features.drop(["Size"], axis = 1)

        Consumption = self.ConsumptionANN.predict(Features)
        return Consumption[0]
    
    def EvaluateDayCoverage(self, Input):
        Generation = Sys.PredictGeneration(Input)
        Consumption = Sys.PredictConsumption(Input)

        Coverage = Generation/Consumption
        return Coverage,Generation,Consumption
    
    def EvaluateMonthCoverage(self, Input):
        YMD = Input["date"].split("-")
        NDays = calendar.monthrange(int(YMD[0]), int(YMD[1]))[1]
        MonthCoverage = pd.DataFrame()
        for Day in range(1,NDays + 1):
            InputBuffer = Input
            InputBuffer["date"] = str(YMD[0]) + "-" + str(YMD[1]) + "-" + str(Day)
            Coverage,Generation,Consumption = self.EvaluateDayCoverage(InputBuffer)
            Coverage = Coverage*100
            MonthCoverage = MonthCoverage.append({"Day": Day, "Coverage": Coverage, "Generation": Generation, "Consumption": Consumption}, ignore_index = True)
        return MonthCoverage
    
    def EvaluateYearCoverage(self, Input):
        YMD = Input["date"].split("-")
        YearCoverage = pd.DataFrame()
        for Month in range(1,13):
            NDays = calendar.monthrange(int(YMD[0]), Month)[1]
            for Day in range(1,NDays + 1):
                InputBuffer = Input
                InputBuffer["date"] = str(YMD[0]) + "-" + str(Month) + "-" + str(Day)
                Coverage,Generation,Consumption = self.EvaluateDayCoverage(InputBuffer)
                Coverage = Coverage*100
                YearCoverage = YearCoverage.append({"Month": Month,"Day": Day, "Coverage": Coverage, "Generation": Generation,"Consumption": Consumption}, ignore_index = True)
        return YearCoverage

        

Sys = System()

Input = {
    "date": "2018-01-20",
    "HouseType": 0,
    "RUs": 1,
    "EVs": 0,
    "HVAC": 1,
    "Isolation": 1,
    "Holiday": 1,
    "Seed": 20,
    "Size": 10
}

print(Sys.EvaluateYearCoverage(Input))
