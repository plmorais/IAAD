import sqlite3
from typing import List, Tuple
class Banco:
  def __init__(self):
    self._con = sqlite3.connect('model/hospital.db')
    self.banco = self._con.cursor()
    self.create_tables()

  def create_tables(self):
    self.create_table('illness', 'code INT PRIMARY KEY, description, severity_description TEXT, risk_mortality TEXT, medical_surgical TEXT')
    
    self.create_table('hospital', 'id INT PRIMARY KEY, hospital_name TEXT NOT NULL, service_area TEXT NOT NULL, county TEXT NOT NULL')
    
    self.create_table('pacient', '''
    pacient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, age int NOT NULL, gender TEXT, race TEXT, 
    ethnicity TEXT, stay int NOT NULL, admission TEXT, disposition TEXT, 
    code INT, hospital_id INT NOT NULL, costs REAL NOT NULL,
    FOREIGN KEY(code) REFERENCES illeness(code) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(hospital_id) REFERENCES hospital(id) ON UPDATE CASCADE ON DELETE CASCADE
    ''') 
    
    self.banco.execute(
      '''
        CREATE TRIGGER IF NOT EXISTS AplicarDesconto
        AFTER INSERT ON pacient
        FOR EACH ROW
        BEGIN
            UPDATE pacient
            SET costs = costs * 0.93 -- Aplica um desconto de 7%
            WHERE NEW.age >= 60 AND NEW.pacient_id = pacient_id;
        END;
      ''')
    self._con.commit()

  def create_table(self, table: str, fields):
    self.banco.execute(f'CREATE TABLE IF NOT EXISTS {table}({fields})')
    self._con.commit()
    
  def insert(self, table: str, values):
    fields = ''
    
    if(table.lower() == 'pacient'):
      fields = '''(age, gender, race, ethnicity, stay,
      admission, disposition, costs, code, hospital_id)'''
    elif(table.lower() == 'hospital'): 
      fields = '''(id, hospital_name, service_area, county)'''
    elif(table.lower() == 'illness'): 
      fields = '''(code, description, severity_description, risk_mortality, medical_surgical)'''
    
    try:
      self.banco.execute(f'''
      INSERT INTO {table}{fields} 
      Values{values}
      ''')    
      self._con.commit()
      return 200
    except:
      return 400
      
  def get_all(self, table: str, fields: str ='*') -> List[Tuple]:
    values : List = []
    for x in self.banco.execute(f'SELECT {fields} FROM {table}'):
      values.append(x)
    return values
  
  def get_pacient(self) -> List[Tuple]:
    values : List = []
    fields = 'pacient.pacient_id, pacient.age, pacient.gender, pacient.ethnicity, pacient.race, pacient.stay, pacient.admission, pacient.costs, illness.description, hospital.hospital_name'
    result = self.banco.execute(f'''
      SELECT {fields} 
      FROM pacient INNER JOIN illness ON pacient.code=illness.code
      INNER JOIN hospital ON hospital.id=pacient.hospital_id
    ''')
    for x in result:
      values.append({
        "id": x[0],
        "age": x[1],
        'gender': x[2],
        'ethnicity': x[3],
        'race': x[4],
        'stay': x[5],
        'admission': x[6],
        'costs': x[7],
        'description': x[8],
        'hospital_name': x[9],
      })
    return values
    #['ID', 'Age', 'Gender', 'Rance', 'Ethnicity', 'Stay', 'Admission', 'Costs', 'Desc. illness', 'Hospital Name' 'Excluir']
    
  def update(self, table: str, fields_edit: str, id: int):
    """ Coloque as aspas duplas em uma string """
    fields_search = 'pacient_id'
    if(table.lower() == 'hospital'): 
      fields_search = 'id'
    elif(table.lower() == 'illness'): 
      fields_search ='code'
    
    try:
      self.banco.execute(f'''
        UPDATE {table}
        SET {fields_edit}                   
        WHERE {fields_search}={id}
      ''')
      self._con.commit()
      return 200
    except:
      return 400

  def delete(self, table: str, id: str):
    if(table.lower() == 'pacient'):
      fields = 'pacient_id'
    elif(table.lower() == 'hospital'): 
      fields = 'id'
    elif(table.lower() == 'illness'): 
      fields = 'code'
    
    self.banco.execute(f'DELETE FROM {table} WHERE {fields}={id}')
    self._con.commit()
 
  def search_pacient(self, filter: str):
    values : List = []
    fields = 'pacient.pacient_id, pacient.age, pacient.gender, pacient.ethnicity, pacient.race, pacient.stay, pacient.admission, pacient.costs, illness.description, hospital.hospital_name'
    """ result = self.banco.execute(f'
      SELECT {fields} 
      FROM pacient INNER JOIN illness ON pacient.code=illness.code
      INNER JOIN hospital ON hospital.id=pacient.hospital_id
    ')
    for x in result:
      values.append({
        "id": x[0],
        "age": x[1],
        'gender': x[2],
        'ethnicity': x[3],
        'race': x[4],
        'stay': x[5],
        'admission': x[6],
        'costs': x[7],
        'description': x[8],
        'hospital_name': x[9],
      })
     """
    result = self.banco.execute(f'''
      SELECT {fields} 
      FROM pacient INNER JOIN illness ON pacient.code=illness.code
      INNER JOIN hospital ON hospital.id=pacient.hospital_id
      WHERE {filter}
    ''')
    
    for x in result:
      values.append({
        "id": x[0],
        "age": x[1],
        'gender': x[2],
        'ethnicity': x[3],
        'race': x[4],
        'stay': x[5],
        'admission': x[6],
        'costs': x[7],
        'description': x[8],
        'hospital_name': x[9],
      })
    return values


""" banco = Banco()
banco.insert('pacient', (60, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 100, 0, 1),)
for x in banco.get_all('pacient'):
  print(x)
   """
""" 
def popular():
  test = [
  (0, 'descri;ao do primeiro', 'white', 'baixo', 'Mode'),
  (1, 'oit', 'black', 'auto', 'extreme'),
  ]
  for x in test:
      banco.insert('illness', x)

  test = [
  (0, 'alberto aistem', 'igarassu', 'pernambuco'),
  (1, 'portugues', 'paulista', 'sao paulo'),
  ]
  for x in test:
    banco.insert('hospital', x)

  test = [
  (15, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 1554.54, 0, 1),
  (15, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 1554.54, 1, 0),
  (15, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 1554.54, 0, 1), 
  (15, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 1554.54, 0, 1), 
  (15, 'm', 'white', 'brazileiro', 15, 'extreme', 'dead', 1554.54, 1, 0),
  ]
  for x in test:
      banco.insert('pacient', x)
      
  for x in banco.get_all('pacient'):
    print(x)

 """