import pandas as pd
from model.banco import Banco
from random import randint, choice


""" data = pd.read_csv('hospital.csv')
data = data.drop([
  'index',
  'Other Provider License Number',
  'Source of Payment 2',
  'Source of Payment 3',
  'Discharge Year',
  'CCS Diagnosis Code',
  'CCS Diagnosis Description',
  'CCS Procedure Code',
  'CCS Procedure Description',
  'Birth Weight',
  'Operating Certificate Number',
  'Attending Provider License Number',
  'Operating Provider License Number',
  'Zip Code - 3 digits',
  'Total Charges',
  'Source of Payment 1',
  ], axis=1)

def format_length_stay(value) -> int:
  if (value == '120 +'):
    return 120
  return int(value)
data['Length of Stay'] = data['Length of Stay'].apply(format_length_stay)
data = data.sample(500, replace=False)
data.to_parquet('model/hospital.parquet') """

def load_hospitais():
  # id, hospital_name, service_area, county
  banco = Banco()
  data = pd.read_parquet('model/hospital.parquet')
  hospitais = data.groupby(['Facility ID', 'Facility Name', 'Health Service Area', 'Hospital County']).size().reset_index(name='Qtn')
  for x in hospitais.values[:, :4]:
    banco.insert('hospital', (x[0], x[1], x[2], x[3]))
    
def load_illnesses():
  # code, description, severity_description, risk_mortality, medical_surgical
  banco = Banco()
  data = pd.read_parquet('model/hospital.parquet')
  illnesses = data.groupby(['APR DRG Code', 
                            'APR DRG Description', 
                            'APR Medical Surgical Description',
                            
                          ]).size().reset_index(name='Qtn')
  for x in illnesses.values[:, :5]:
    severity = choice(["Menor", "Moderdo", "Maior", "Extremo"])
    mortality = choice(["Menor", "Moderdo", "Maior", "Extremo"])
    banco.insert('illness', (x[0], x[1], severity, mortality, x[2]))
    
def load_pacient():
  banco = Banco()
  data = pd.read_parquet('model/hospital.parquet')
  pacients = data.groupby([ 'Gender', 
                            'Race',
                            'Ethnicity',
                            'Length of Stay',
                            'Type of Admission',
                            'Patient Disposition',
                            'Total Costs',
                            'APR DRG Code',
                            'Facility ID',
                          ]).size().reset_index(name='Qtn')
  for x in pacients.values[:, :9]:
    age = randint(0, 100)
    gender = ''
    race = ''
    ethi = ''
    admission = ''
    
    if x[0] == 'M': gender = 'Masculino'
    elif x[0] == 'F': gender = 'Feminino'
    else: gender = 'Outro'
    
    if x[1] == 'White': race = 'Branco'
    elif x[1] == 'Black/African American': race = 'Preto'
    else: race = 'Outra raça'
    
    if x[2] == 'Spanish/Hispanic': ethi = "Espanhol/hispânico"
    elif x[2] == 'Not Span/Hispanic': ethi = "Não é espanhol/hispânico"
    else: ethi = "Outro"
    
    if x[4] == 'Emergency': admission = "Emergência"
    elif x[4] == 'Elective': admission = "Eletivo"
    elif x[4] == 'Urgent': admission = 'Urgente'
    else: admission = "Outro"

    if x[5] in ['Home or Self Care','Home w/ Home Health Services'] : 
      disposition = "Casa ou autocuidado"
    elif x[5] == ['Psychiatric Hospital or Unit of Hosp', 'Hospice - Medical Facility', 'Hospice - Home', ]: 
      disposition = "Hospício"
    elif x[5] == ['Medicare Cert Long Term Care Hospital', 'Short-term Hospital', 'Inpatient Rehabilitation Facility', ]: 
      disposition = "Hospital"
    else: disposition = "Outro"
    # (age, gender, race, ethnicity, stay, admission, disposition, costs, code, hospital_id)
    banco.insert('pacient', (age, gender, race, ethi, x[3], admission, disposition, x[6], x[7], x[8]))

