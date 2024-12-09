'''
The following functions are used to calculate the age of a person based on the birthdate and to find the age group of the person.
The age groups are used for the Use Case SARS-CoV-2-Infektionen_in_Deutschland (by the RKI)
See project source: https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/tree/main
See documentation here: https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/blob/main/%5BDokumentation%5D_SARS-CoV-2-Infektionen_in_Deutschland.pdf
'''
from datetime import datetime
from dateutil.relativedelta import relativedelta



def calculate_age(birthdate: str)-> int:
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


def find_age_group(age, age_groups)-> str:
    '''
    Function to find the age group of a person based on the age.
    Args:
        age (int): age of the person
        age_groups (list): list of dictionaries containing the age groups

        Example age group: 
        {"group": "A00-A04", "min_age": 0, "max_age": 4}

    Returns:
        str | None: age group of the person
    '''
    for group in age_groups:
        if group['min_age'] <= age <= group['max_age']:
            return group['group']
    return None


def calculate_months_from_date(date: str, months: int)-> (str, str): 
    '''
    Function to calculate a date months before and after a given date.
    Args:
        date (str): date in format "YYYY-MM-DD"
        months (int): number of months to calculate before and after the given date
    Returns:
        tuple: a tuple containing the date 6 months before and after the given date
    '''
    
    try:
        # Convert the string to a datetime object
        given_date = datetime.strptime(date, '%Y-%m-%d')
        
        # Calculate 6 months before and after
        six_months_before = given_date - relativedelta(months=6)
        six_months_after = given_date + relativedelta(months=6)
        
        # Convert back to string format
        return six_months_before.strftime('%Y-%m-%d'), six_months_after.strftime('%Y-%m-%d')
    
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

def calculate_min_max_months_from_data_collection(data_collection: list)-> (str, str):
    '''
    Function to calculate the minimum and maximum date from a list of dates.
    Args:
        data_collection (list): list of dates in format "YYYY-MM-DD"
    Returns:
        tuple: a tuple containing the minimum and maximum date from the list
    '''
    try:
        # Convert the string to a datetime object
        date_list = [datetime.strptime(date, '%Y-%m-%d') for date in data_collection]
        
        # Calculate the minimum and maximum date
        min_date = min(date_list)
        max_date = max(date_list)
        
        # Convert back to string format
        return min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')
    
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."