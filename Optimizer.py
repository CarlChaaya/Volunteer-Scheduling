from ortools.sat.python import cp_model
import pandas as pd
from Rescuer import *
import random
#data_path = 'D:\Downloads\Rescuers_Sample.xlsx'
#output_path = r'D:\Downloads\Rescuers_Sample_Solution.xlsx'

def Optimizer(data_path, output_path, num_days = 7, tolerance_level = 1, optimal = False):

    model = cp_model.CpModel()

    data = pd.read_excel(data_path)
    rescuers, rescuers_dict = extract_Rescuers(data, num_days)
    day_range = range(num_days)

    shifts = {}

    # Creating Boolean Variables:
    for day in day_range:
        for rescuer in rescuers:
            shifts[(day, rescuer.name)] = model.NewBoolVar(rescuer.name + str(day))

    # Adding some Randomness to the mix:
    for i in range(round(1/20*(1/tolerance_level)*len(rescuers))):
        randomnumber = random.randint(0, len(rescuers) -1)
        if rescuers[randomnumber].CE == False:
            if randomnumber%num_days not in rescuers[randomnumber].unwanted:
                rescuers[randomnumber].preferred = randomnumber%num_days

    # Highest Priority: Least Number of rescuers with unwanted days
    if optimal == False:
        model.Minimize(1000 * sum(shifts[(rescuer.unwanted[0], rescuer.name)] for rescuer in rescuers))
        model.Minimize(1000 * sum(shifts[(rescuer.unwanted[1], rescuer.name)] for rescuer in rescuers))
        model.Add(sum(shifts[(rescuer.unwanted[0], rescuer.name)] for rescuer in rescuers) + sum(shifts[(rescuer.unwanted[1], rescuer.name)] for rescuer in rescuers) <= round(tolerance_level/(random.randint(30,40)) * len(rescuers)))
    else:
        model.Add(sum(shifts[(rescuer.unwanted[0], rescuer.name)] for rescuer in rescuers) == 0)
        model.Add(sum(shifts[(rescuer.unwanted[1], rescuer.name)] for rescuer in rescuers) == 0)
    # Creating First Condition: Each rescuer must only have one shift per week:
    for rescuer in rescuers:
        model.Add(sum(shifts[(day, rescuer.name)] for day in day_range) == 1)

    # Creating Second Condition: Equal number of male and female:
    for day in day_range:
        model.Add(round(-1*(1/tolerance_level)) <= (sum(shifts[day, rescuer.name] for rescuer in rescuers_dict['Male']) - sum(shifts[day, rescuer.name] for rescuer in rescuers_dict['Female'])) <= round(1*(1/tolerance_level)))



    # Creating Third Condition: At least 1 CE per team:
    for day in day_range:
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['CE']) >= 1)


    # Creating Fourth Condition: Distribute equally rescuers among teams:
    for day in day_range:
        model.Add(round(-1*(1/tolerance_level)) <= sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Ambulancier']) - len(rescuers_dict['Ambulancier'])//len(day_range) <= round(1*(1/tolerance_level)))
        model.Add(round(-1*(1/tolerance_level)) <= sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['CM']) - len(rescuers_dict['CM'])//len(day_range) <= 1)
        model.Add(round(-1*(1/tolerance_level)) <= sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Overall']) - len(rescuers_dict['Overall'])//len(day_range) <= round(1*(1/tolerance_level)))
        model.Add(round(-1*(1/tolerance_level)) <= sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Dossard']) - len(rescuers_dict['Dossard']) // len(day_range) <= round(1*(1/tolerance_level)))
        model.Add(max(round(-1*(1/(tolerance_level+1))), -2) <= sum(shifts[(day, rescuer.name)] for rescuer in rescuers) - len(rescuers)//len(day_range) <= min(round(1*(1/tolerance_level)),3))

    # Creating Fifth Condition: At least 1 TekCom per team:
    for day in day_range:
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Tek']) >= 1)


    # Creating Sixth Condition: If CM trainee in team, then at least 1 CM old, and If Ambulancier Trainee, then at least 1 Ambulancier old:
    b = []
    c = []
    for day in day_range:
        b.append(model.NewBoolVar('b' + str(day)))
        c.append(model.NewBoolVar('c' + str(day)))

        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Ambu_Trainee']) >= 1).OnlyEnforceIf(b[day])
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['CM_Trainee']) >= 1).OnlyEnforceIf(c[day])

        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Old_Ambu']) >= 1).OnlyEnforceIf(b[day])
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Old_CM']) >= 1).OnlyEnforceIf(b[day])


    # Creating Seventh Condition: Minimize number of people who get unwanted days and maximize wanted days:
    model.Maximize(sum(shifts[(rescuer.preferred, rescuer.name)] for rescuer in rescuers))
    model.Add(sum(shifts[(rescuer.preferred, rescuer.name)] for rescuer in rescuers) >= random.randint(round(0.2*(1/tolerance_level)*len(rescuers)), round(0.5*(1/tolerance_level) * len(rescuers))))

    # Creating Eighth condition: Setting a minimum number for ambulancier and CM:
    for day in day_range:
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['Ambulancier']) >= 1)
        model.Add(sum(shifts[(day, rescuer.name)] for rescuer in rescuers_dict['CM']) >= 1)

    # Creating Ninth condition: Adding another layer of tolerated distribution:
    for day in day_range[:-1]:
        model.Add(sum(shifts[day, rescuer.name] for rescuer in rescuers) - sum(shifts[day + 1, rescuer.name] for rescuer in rescuers) <= round(1*1/tolerance_level))
    model.Add(sum(shifts[day_range[-1], rescuer.name] for rescuer in rescuers) - sum(shifts[0, rescuer.name] for rescuer in rescuers) <= round(1 * 1 / tolerance_level))
    model.Add(sum(shifts[1, rescuer.name] for rescuer in rescuers) - sum(shifts[day_range[0], rescuer.name] for rescuer in rescuers) <= round(1 * 1 / tolerance_level))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
        columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][:num_days]
        if num_days == 6:
            columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
        elif num_days == 5:
            columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        counters = [0]*len(day_range)
        dataframe = pd.DataFrame(columns=columns)
        preferred = 0
        unwanted = 0
        for day in day_range:
            Male = 0
            Female = 0
            Ambulancier = 0
            CM = 0
            Overall = 0
            Dossard = 0
            for rescuer in rescuers:
                if solver.Value(shifts[day, rescuer.name]) == 1:
                    dataframe.loc[counters[day], columns[day]] = rescuer.name
                    counters[day] += 1
                    if rescuer in rescuers_dict['Male']:
                        Male += 1
                    else:
                        Female += 1
                    if rescuer in rescuers_dict['Ambulancier']:
                        Ambulancier += 1
                    elif rescuer in rescuers_dict['CM']:
                        CM += 1
                    elif rescuer in rescuers_dict['Overall']:
                        Overall += 1
                    else:
                        Dossard += 1
                    if rescuer.preferred == day:
                        preferred += 1
                    elif day in rescuer.unwanted:
                        unwanted += 1
                        print(rescuer.name)
            if day == 0:
                dataframe.loc[counters[day] , columns[day]] = None
                dataframe.loc[counters[day] + 1, columns[day]] = None
                dataframe.loc[counters[day] + 2, columns[day]] = None
            dataframe.loc['Male', columns[day]] = Male
            dataframe.loc['Female', columns[day]] = Female
            dataframe.loc['Ambulancier', columns[day]] = Ambulancier
            dataframe.loc['CM', columns[day]] = CM
            dataframe.loc['Overall', columns[day]] = Overall
            dataframe.loc['Dossard', columns[day]] = Dossard
        dataframe.loc['Number of Preferred', columns[0]] = preferred
        dataframe.loc['Number of Unwanted', columns[0]] = unwanted
        dataframe.to_excel(output_path)
        return 'Solution Found, Check your folder for Solution_'
    else:
        return 'Solution not Found'
