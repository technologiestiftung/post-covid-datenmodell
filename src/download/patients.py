from datetime import datetime
from typing import Optional, Literal
'''
This script contains multiple classes for patient information that comes from 'Kerndatensatz' of MII (www.medizininformatik-initiative.de).

The classes not yet all used in the project, but are provided for possible future use with their relevant attributes.

'''
from src.geolocation.address_transformation import get_long_lat_from_postal_code

class PatientAddress:
    '''
    Class is based on 'Modul Person: Patient - Pseudonymisiert'
    See here: https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Person_Version_2/MIIIGModulPerson-TechnischeImplementierung-FHIR-Profile-PseudonymisiertePatientinPatient.html
    '''
    def __init__(self):
        self.street: Optional[str] = None  # street name and house number
        self.city: Optional[str] = None
        self.state: Optional[str] = None
        self.postal_code: str
        self.country: str
        self.latitude: Optional[float] = None # long + lat from postal_code
        self.longitude: Optional[float] = None

class PatientProcedure: 
    '''
    Class is based on MII IG Prozedur DE v2024 
    See here: https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Prozedur_Version_2/MIIIGModulProzedur-TechnischeImplementierung-FHIRProfile-Prozedur-Procedure.html
    '''

    def __init__(self):
        self.id: str
        self.status: Literal["preparation", "in-progress", "not-done", "on-hold", "stopped", "completed", "entered-in-error", "unknown"]
        self.code: Optional[str] = None
        self.body_site: str
        self.note: str

class PatientMedicationStatement: 
    '''
    Class is based on MII IG Modul Medikation - MedicationStatement
    See here: https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Medikation_Version_2/MedicationStatement.html
    '''

    def __init__(self):
        self.id: str
        self.status: Literal["active", "completed", "entered-in-error", "intended", "stopped", "on-hold", "unknown", "not-taken"]
        self.code: Optional[str] = None
        self.reason_code: Optional[str] = None
        self.note: str = ""


class PatientEncounter: 
    '''
    Class is based on MII PR Fall Kontakt mit einer Gesundheitseinrichtung (Encounter)
    See here: https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Fall_Version_2/MIIIGModulFall-TechnischeImplementierung-FHIRProfile-EncounterKontaktGesundheitseinrichtung.html
    
    '''
    def __init__(self):
        self.id: str
        self.satus: Literal["planned", "arrived", "triaged", "in-progress", "onleave", "finished", "cancelled"]
        self.service_type: Optional[str] = None
        self.period_start: datetime
        self.period_end: datetime
        self.diagnosis: Optional[str] = None

class PatientCondition: 
    '''
    Class is based on MII PR Diagnose Condition / MII IG Diagnose DE v2024
    See here: https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Diagnose_Version_2/MIIIGModulDiagnose-TechnischeImplementierung-FHIRProfile-Diagnose-Condition.html
    '''
    def __init__(self):
        self.id: str
        self.clinical_status: Literal["active", "recurrence", "relapse", "inactive", "remission", "resolved"]
        self.code: str
        self.recorded_date: datetime # date of diagnosis
        self.note: str = ""

class Patient: 
    def __init__(self):
        self.id: str
        self.gender: Literal["male", "female", "other", "unknown"]
        self.birth_date: datetime
        self.address: PatientAddress = PatientAddress()
        self.diagnosis_date: str
        
class PatientsDownload: # PatientCollection
    '''
    Class is based on 'Modul Person: Patient - Pseudonymisiert', see here: 
    https://www.medizininformatik-initiative.de/Kerndatensatz/Modul_Person_Version_2/MIIIGModulPerson-TechnischeImplementierung-FHIR-Profile-PseudonymisiertePatientinPatient.html 
    
    '''
    def __init__(self):
        self.patients = []

    def get_patient_by_id(self, patient_id: str):
        """
        Retrieves a patient by their unique ID.
        
        """
        for patient in self.patients:
            if patient.id == patient_id:
                return patient
        return None

    def extract_patients(self, data):
        '''
        Extract patients data from a provided dataset (json) and return a PatientsDownload object.
        
        '''
        patients = []
        for entry in data["entry"]:
            if entry["resource"].get("resourceType") == "Patient":
                patient = Patient()  # Create a new instance of PatientDownload

                try: 
                    patient.id = entry["resource"].get("id", None)
                    patient.gender = entry["resource"].get("gender", None)
                    patient.birth_date = entry["resource"].get("birthDate", None)

                except KeyError: 
                    warnings.warn("Error: Basic Patient data incomplete")

                    
                # Add address data
                try: 
                    patient.address.country = entry["resource"]["address"][0].get("country", None)
                    patient.address.state = entry["resource"]["address"][0].get("state", None)
                    patient.address.city = entry["resource"]["address"][0].get("city", None)
                    patient.address.postal_code = entry["resource"]["address"][0].get("postalCode", None)

                except KeyError:
                    warnings.warn("Error: Patient Address data incomplete")

                # add longitude and latitiude from postal code
                if patient.address.postal_code:
                    patient.address.longitude, patient.address.latitude = get_long_lat_from_postal_code(patient.address.postal_code)

                # Patient street is accessed differently (it may not be given)
                try: 
                    patient.address.street = entry["resource"]["address"][0].get("line", [None])[0]
                except KeyError: 
                    warnings.warn("Error: Patient Street data incomplete")

                self.patients.append(patient)
                
        for entry in data["entry"]:
            # Add diagnosis data
            if entry["resource"].get("resourceType") == "Condition":
                try: 
                    
                    patient_id = entry["resource"]["subject"].get("reference", None).strip("Patient/")
                    relevant_patient = self.get_patient_by_id(patient_id)
                    relevant_patient.diagnosis_date = entry["resource"].get("recordedDate", None).split("T")[0]
                # todo: adjust for large mii dataset
                except KeyError: 
                    warnings.warn("Error: Patient Diagnosis data incomplete")
                    continue
                except AttributeError:
                    warnings.warn("Error: Patient ID not found")
                    continue


        return self.patients
