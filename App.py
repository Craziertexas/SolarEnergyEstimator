from System import System
import pandas as pd
import matplotlib.pyplot as plt

Sys = System()
SW = True

date = "2018-01-20"
HouseType = 0
RUs = 1
EVs = 0
HVAC = 1
Isolation = 1
Holiday = 1
Seed = 20
Size = 1

while SW:
    try:
        print("--------------------Welcome!--------------------")
        print("Please Select the action to perform")
        print("1. Modify System parameters")
        print("2. Predict Generation")
        print("3. Predict Consumption")
        print("4. Predict Coverage")
        print("5. Predict Month Coverage")
        print("6. Predict Year Coverage")
        print("7. System evaluation")
        print("8. Exit")

        optionwait = True
        while optionwait:
            try:
                option = int(input("->"))
                optionwait = False
            except:
                print("Only option numbers allowed!")
    
        
        if (option == 1):
            print()
            print("Please input your House Type:")
            print("0. Laneway")
            print("1. Duplex")
            print("2. Modern")
            print("3. Apartment")
            print("4. Character")
            print("5. Special")
            print("6. Bungalow")
            optionwait = True
            while optionwait:
                try:
                    HouseType = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Please input the number of residential units in your house:")
            optionwait = True
            while optionwait:
                try:
                    RUs = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Please input the size of your electric vehicle battery (KWh):")
            optionwait = True
            while optionwait:
                try:
                    EVs = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Do you have any electric aconditioning system? (YES: 1, NO: 0):")
            optionwait = True
            while optionwait:
                try:
                    HVAC = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Your House has walls with thermal isolation? (YES: 1, NO: 0):")
            optionwait = True
            while optionwait:
                try:
                    Isolation = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Input an aproximation of a daily electricity demand (KWh):")
            optionwait = True
            while optionwait:
                try:
                    Seed = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()
            print("Input the nominal Output Power of your solar energy system (KWh):")
            optionwait = True
            while optionwait:
                try:
                    Size = int(input("->"))
                    optionwait = False
                except:
                    print("Only option numbers allowed!")
            print()

        if (option == 2):
            print()
            print("Input the date to estimate (YYYY-MM-DD):")
            date = input("->")

            Input = {
                "date": date,
                "HouseType": HouseType,
                "RUs": RUs,
                "EVs": EVs,
                "HVAC": HVAC,
                "Isolation": Isolation,
                "Holiday": Holiday,
                "Seed": Seed,
                "Size": Size
            }
            print("-------------------- Input Parameters --------------------")
            print(Input)
            print("------------------------------------------------")
            print("Generation (KW): ",Sys.PredictGeneration(Input))
        
        if (option == 3):
            print()
            print("Input the date to estimate (YYYY-MM-DD):")
            date = input("->")

            Input = {
                "date": date,
                "HouseType": HouseType,
                "RUs": RUs,
                "EVs": EVs,
                "HVAC": HVAC,
                "Isolation": Isolation,
                "Holiday": Holiday,
                "Seed": Seed,
                "Size": Size
            }
            print("-------------------- Input Parameters --------------------")
            print(Input)
            print("------------------------------------------------")
            print("Demand (KW): ",Sys.PredictConsumption(Input))
        
        if (option == 4):
            print()
            print("Input the date to estimate (YYYY-MM-DD):")
            date = input("->")

            Input = {
                "date": date,
                "HouseType": HouseType,
                "RUs": RUs,
                "EVs": EVs,
                "HVAC": HVAC,
                "Isolation": Isolation,
                "Holiday": Holiday,
                "Seed": Seed,
                "Size": Size
            }
            Coverage,Generation,Consumption = Sys.EvaluateDayCoverage(Input)
            print("-------------------- Input Parameters --------------------")
            print(Input)
            print("------------------------------------------------")
            print("Coverage (%): ",Coverage)
            print("Generation (KW): ",Generation)
            print("Demand (KW): ", Consumption)
        
        if (option == 5):
            print()
            print("Input the year and month to estimate (YYYY-MM):")
            date = input("->")

            Input = {
                "date": date + "-01",
                "HouseType": HouseType,
                "RUs": RUs,
                "EVs": EVs,
                "HVAC": HVAC,
                "Isolation": Isolation,
                "Holiday": Holiday,
                "Seed": Seed,
                "Size": Size
            }

            MonthCoverage = Sys.EvaluateMonthCoverage(Input, True)
            print("-------------------- Input Parameters --------------------")
            print(Input)
            print("------------------------------------------------")
            print("-------------------- Month Coverage --------------------")
            print(MonthCoverage.head())
            print("------------------------------------------------")

            fig1 = plt.figure(1)
            plt.plot(MonthCoverage["Coverage"])
            plt.title("Month Coverage for " + date)
            plt.xlabel("Days")
            plt.ylabel("Coverage (%)")

            fig2 = plt.figure(2)
            plt.plot(MonthCoverage["Generation"])
            plt.title("Month Generation for " + date)
            plt.xlabel("Days")
            plt.ylabel("Generation (KW)")

            fig3 = plt.figure(3)
            plt.plot(MonthCoverage["Consumption"])
            plt.title("Month Demand for " + date)
            plt.xlabel("Days")
            plt.ylabel("Demand (KW)")

            plt.show()
        if (option == 6):
            print()
            print("Input the year to estimate (YYYY):")
            date = input("->")

            Input = {
                "date": date + "-01-01",
                "HouseType": HouseType,
                "RUs": RUs,
                "EVs": EVs,
                "HVAC": HVAC,
                "Isolation": Isolation,
                "Holiday": Holiday,
                "Seed": Seed,
                "Size": Size
            }

            YearCoverage = Sys.EvaluateYearCoverage(Input, True)
            print("-------------------- Input Parameters --------------------")
            print(Input)
            print("------------------------------------------------")
            print("-------------------- Year Coverage --------------------")
            print(YearCoverage.head())
            print("------------------------------------------------")

            fig1 = plt.figure(1)
            plt.plot(YearCoverage["Coverage"])
            plt.title("Year Coverage for " + date)
            plt.xlabel("Days")
            plt.ylabel("Coverage (%)")

            fig2 = plt.figure(2)
            plt.plot(YearCoverage["Generation"])
            plt.title("Year Generation for " + date)
            plt.xlabel("Days")
            plt.ylabel("Generation (KW)")

            fig3 = plt.figure(3)
            plt.plot(YearCoverage["Consumption"])
            plt.title("Year Demand for " + date)
            plt.xlabel("Days")
            plt.ylabel("Demand (KW)")

            plt.show()
        
        if (option == 7):
            print("Evaluating System....")
            Sys.PerformanceEvaluation()
            print("Done!")

        if (option == 8):
            SW = False

    except Exception as e:
        print("An execption ocurred during runtime")
        print(e)