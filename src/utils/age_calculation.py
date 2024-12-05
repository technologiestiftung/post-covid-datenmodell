'''
The following code snippet is used to calculate the age of a person based on the birthdate and to find the age group of the person.
The age groups are used for the Use Case SARS-CoV-2-Infektionen_in_Deutschland (by the RKI)
See project source: https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/tree/main
See documentation here: https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/blob/main/%5BDokumentation%5D_SARS-CoV-2-Infektionen_in_Deutschland.pdf
'''
from datetime import datetime



def calculate_age(birthdate: str):
    '''
    Function to calculate the age of a person based on the birthdate.
    Args:
        birthdate (str): birthdate of the person in format "YYYY-MM-DD"
    Returns:
        int: age of the person
    '''
    today = datetime.today()
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def find_age_group(age, age_groups):
    '''
    Function to find the age group of a person based on the age.
    Args:
        age (int): age of the person
        age_groups (list): list of dictionaries containing the age groups
    Returns:
        str | None: age group of the person
    '''
    for group in age_groups:
        if group['min_age'] <= age <= group['max_age']:
            return group['group']
    return None