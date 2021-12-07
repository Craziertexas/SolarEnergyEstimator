import pandas as pd
pd.options.mode.chained_assignment = None
from datetime import datetime

SolarData = pd.DataFrame()

#Carga de datos
for SolarSize in range(1,6):
    with open(r"Data/SolarEnergy/pvwatts_hourly_"+str(SolarSize)+".csv") as file:
        buffer = pd.read_csv(file, sep = ",")
        buffer["Size"] = SolarSize
        SolarData = SolarData.append(buffer, ignore_index = True, verify_integrity= True, sort = True)

#Exportar Data
SolarData.to_csv(r"Data/SolarEnergy/SolarData.csv", sep = ",", index = False)