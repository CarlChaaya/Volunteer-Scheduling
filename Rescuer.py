import pandas as pd

class Rescuer(object):
    def __init__(self, name, sex, promo, role,
                 status, tek, old_ambu, ambu_trainee,
                 old_cm, cm_trainee,preferred, unwanted, CE):
        self.name = name
        self.sex = sex
        self.promo = promo
        self.role = role
        self.status = status
        self.tek = tek
        self.old_ambu = old_ambu
        self.ambu_trainee = ambu_trainee
        self.old_cm = old_cm
        self.cm_trainee = cm_trainee
        self.preferred = preferred
        self.unwanted = unwanted
        self.CE = CE

def day_to_number(day, num_days):
    if num_days != 6:
        if day == 'Monday':
            return 0
        elif day == 'Tuesday':
            return 1
        elif day == 'Wednesday':
            return 2
        elif day == 'Thursday':
            return 3
        elif day == 'Friday':
            return 4
        elif day == 'Saturday':
            return 5
        elif day == 'Sunday':
            return 6
    elif num_days == 6:
        if day == 'Monday':
            return 0
        elif day == 'Tuesday':
            return 1
        elif day == 'Wednesday':
            return 2
        elif day == 'Thursday':
            return 3
        elif day == 'Friday':
            return 4
        elif day == 'Sunday':
            return 5

def extract_Rescuers(df, num_days):
    rescuers = []
    rescuers_dict = {'Male' : [],
                     'Female' : [],
                     'Ambulancier' : [],
                     'CM' : [],
                     'Overall' : [],
                     'Dossard' : [],
                     'Tek' : [],
                     'Old_Ambu' : [],
                     'Ambu_Trainee' : [],
                     'Old_CM' : [],
                     'CM_Trainee' : [],
                     'CE' : []}

    for index, rescuer in df.iterrows():
        name = rescuer['Name/Nickname']
        sex = rescuer['Sex']
        promo = rescuer['Promo']
        role = rescuer['Role']
        status = rescuer['Status']
        tek = True if rescuer['Tek Com?'] == 'Yes' else False
        old_ambu = True if rescuer['Ambulancier for more than 1 generation?'] == 'Yes' else False
        ambu_trainee = True if rescuer['Ambulancier Trainee?'] == 'Yes' else False
        old_cm = True if rescuer['CM for more than 1 generation?'] == 'Yes' else False
        cm_trainee = True if rescuer['CM Trainee'] == 'Yes' else False
        preferred = day_to_number(rescuer['Favorite Option'], num_days)
        unwanted = [day_to_number(x, num_days) for x in rescuer['2 Least Priority/Unavailable options'].split(', ')]
        CE = True if rescuer['CE'] =='Yes' else False

        my_rescuer = Rescuer(name, sex, promo, role, status,
                             tek, old_ambu, ambu_trainee,
                             old_cm, cm_trainee, preferred, unwanted, CE)

        rescuers.append(my_rescuer)

        if sex == 'Male':
            rescuers_dict['Male'].append(my_rescuer)
        else:
            rescuers_dict['Female'].append(my_rescuer)


        if role == 'Ambulancier':
            rescuers_dict['Ambulancier'].append(my_rescuer)
        elif role == 'CM':
            rescuers_dict['CM'].append(my_rescuer)
        elif role == 'Overall':
            rescuers_dict['Overall'].append(my_rescuer)
        else:
            rescuers_dict['Dossard'].append(my_rescuer)


        if tek == True:
            rescuers_dict['Tek'].append(my_rescuer)


        if old_ambu == True:
            rescuers_dict['Old_Ambu'].append(my_rescuer)

        if ambu_trainee == True:
            rescuers_dict['Ambu_Trainee'].append(my_rescuer)


        if old_cm == True and role != 'Ambulancier':
            rescuers_dict['Old_CM'].append(my_rescuer)


        if cm_trainee == True:
            rescuers_dict['CM_Trainee'].append(my_rescuer)


        if CE == True:
            rescuers_dict['CE'].append(my_rescuer)

    return rescuers, rescuers_dict