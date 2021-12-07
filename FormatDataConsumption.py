import pandas as pd
pd.options.mode.chained_assignment = None
from datetime import datetime

#Carga de datos
Regions = ["WYJ", "YVR"]
WeatherData = {}
HouseFeatures = pd.DataFrame()
HouseData = pd.DataFrame()

#Cargar Caracacteristicas de casa
with open(r"Data/HouseHold/Features.csv") as file:
    HouseFeatures = pd.read_csv(file, sep = ",")

#Codificacion Aislante casa
for facing in HouseFeatures["Facing"].unique():
    if (facing == "East") or (facing == "West"):
        HouseFeatures.loc[HouseFeatures["Facing"] == facing, "Isolation"] = 0
    else:
        HouseFeatures.loc[HouseFeatures["Facing"] == facing, "Isolation"] = 1

ElectricAC = ["HP", "FPE", "FAC", "PAC", "BHE", "IFRHE"]
#Codificacion AC
for HVAC in HouseFeatures["HVAC"].values:
    if (type(HVAC) == str):
        result = 0
        for AC in ElectricAC:
            result = HVAC.find(AC)
            if (result != -1):
                break
        if (result != -1):
            HouseFeatures.loc[HouseFeatures["HVAC"] == HVAC, "HVAC"] = 1
        else:
            HouseFeatures.loc[HouseFeatures["HVAC"] == HVAC, "HVAC"] = 0

print("--------------------------- House Features ---------------------------")
print(HouseFeatures)
print("----------------------------------------------------------------------")

#Cargar Datos de energia por casa
for House in range(1, 29):
    with open(r"Data/HouseHold/Residential_" + str(House) + ".csv") as file:
            buffer = pd.read_csv(file, sep = ",")
            buffer['ID'] = House
            HouseData = HouseData.append(buffer, ignore_index = True, verify_integrity= True, sort = True)
print("--------------------------- House Energy ---------------------------")
print(HouseData.head())
print("--------------------------------------------------------------------")

#Cargar dias festivos
with open(r"Data/HouseHold/holidays.csv") as file:
    Holidays = pd.read_csv(file, sep = ",")
print("--------------------------- HoliDays ------------------------------")
print(Holidays.head())
print("-------------------------------------------------------------------")

#Agrupar consumo por dia
Output = pd.DataFrame()
for House in range(1,29):
    print(House)
    BufferHouse = HouseData.loc[HouseData["ID"] == House]
    for Date in BufferHouse["date"].unique():
        BufferDate = BufferHouse.loc[BufferHouse["date"] == Date]
        Output = Output.append({"ID":House, "date": Date, "Energy_KWH":BufferDate["energy_kWh"].sum()}, ignore_index = True)

#Enlazar consumo de energia con caracteristicas de la casa
for House in range(1,29):
    Features = pd.DataFrame(HouseFeatures.loc[HouseFeatures["House"] == House])
    if (not Features.empty):
        FeaturesIndex = Features.index
        for column in Features.columns:
            Output.loc[Output["ID"] == House, column] = Features[column][FeaturesIndex[0]]

#Codificacion Tipo de casa
HouseType = pd.DataFrame()
for tipe in HouseFeatures["HouseType"].unique():
    buffer = Output.loc[(Output["HouseType"] == tipe)&(Output["RUs"] == 0)]
    mean = buffer["Energy_KWH"].mean()
    HouseType = HouseType.append({"Type":tipe, "mean":mean}, ignore_index=True)

print(HouseType)
print(HouseType.sort_values("mean")["Type"].unique())

code = 0
for tipe in HouseType.sort_values("mean")["Type"].unique():
    Output.loc[Output["HouseType"] == tipe, "HouseType"] = code
    code += 1
    

#Agregar dias festivos y fines de semana
for Date in Output["date"].unique():
    YMD = Date.split("-")
    Holiday = 0
    if (not Holidays.loc[Holidays["date"] == Date].empty):
        Holiday = 1
    if (datetime(int(YMD[0]),int(YMD[1]),int(YMD[2])).weekday() > 4):
        Holiday = 1

    Output.loc[Output["date"] == Date, "Holiday"] = Holiday
    
print("--------------------------- Energy by Day ------------------------------")
print(Output.head())
print("------------------------------------------------------------------------")

#Exportar datos
Output.to_csv(r"Data/HouseHold/HouseData.csv", sep = ",", index = False)

