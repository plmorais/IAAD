import streamlit as st
from model.banco import Banco
from time import sleep



st.set_page_config(
  page_title = 'Paciente',
  layout = 'wide',
)

st.title("Formulário de paciente")
banco = Banco()

def inputs_doencas(layout):
  with st.expander("Adicione um paciente"):
    hospitais = {'':''}
    for hospital in banco.get_all('hospital'):
      h = (hospital[1:][0].title(), hospital[1:][1].title(), hospital[1:][2].title(),)
      hospitais[h] = hospital[0]
    illnesses = {'':''}
    for illness in banco.get_all('illness', 'code, description, medical_surgical'):
      illnesses[(illness[1:][0].title(), illness[1:][1].title())] = illness[0]
      
    with st.form(key="include_paciente"):
      input_age = st.number_input(label="Insira sua idade", format="%d", step=1)
      input_gender = st.selectbox(label="Selecione seu gênero",options=['',"Feminino","Masculino","Outro"])
      input_race = st.selectbox(label="Selecione sua raça",options=['',"Branco","Preto","Outro"])
      input_ethnicity = st.selectbox(label="Insira seu etnia",options=['',"Não é espanhol/hispânico","Espanhol/hispânico","Outro"])
      input_stay = st.number_input(label="Insira seu tempo de estadia", format="%d", step=1)
      input_admission = st.selectbox(label="Insira qual seu tipo de admissão",options=['',"Emergência","Eletivo","Outro"])
      input_disposition = st.selectbox(label="Insira sua dispoição",options=['',"Casa ou autocuidado","Casa com serviços de saúde domiciliar","Outro"])
      input_hospital = st.selectbox(label='Hospital (nome, area, condado)', options=hospitais)
      input_illness = st.selectbox(label='Hospital (nome, area, condado)', options=illnesses)
      input_costs = st.number_input(label="Insira seu custo")
      submit = st.form_submit_button("Enviar")

      # (age, gender, race, ethnicity, stay, admission, disposition, costs, code, hospital_id)
      
      if submit:
        flag = [
          input_age == '',
          input_gender == '',
          input_race == '',
          input_ethnicity == '',
          input_stay == 0,
          input_admission == '',
          input_disposition == '',
          input_illness == '',
          input_hospital == '',
          input_costs == 0
        ]
        if(flag.count(True) == 0):
          pacient = (
            input_age,
            input_gender,
            input_race,
            input_ethnicity,
            input_stay,
            input_admission,
            input_disposition,
            input_costs,
            illnesses[input_illness],
            hospitais[input_hospital]
          )
          print(pacient)
          if(banco.insert('pacient', pacient) == 200):
            st.title(':green[Paciente cadastrado com sucesso]')
          else:
            st.title(':orange[Paciente já está cadastrado]')
        else:
          st.title(f':red[Deixou {flag.count(True)} campos em banco]')
      
def read_doencas(layout, at):
  container = layout.container()
  layout.title('Consultar Dados')
  fields = (.5, .5, .6, .6, .4, .5, .5, 1, 1, 1, 1.5,)
  colunas = layout.columns(fields)
  campos = ['ID', 'Age', 'Gender',  'Ethnicity', 'Rance', 'Stay', 'Admission', 'Costs', 'Desc. illness', 'Hospital Name' 'Excluir']
  for coluna, campo in zip(colunas,campos):
    coluna.write(campo)
  items = banco.get_pacient()
  #(age, gender, race, ethnicity, stay, admission, disposition, costs, code, hospital_id) a
  c_1, _ = st.columns((8, 2))
  for i, item in enumerate(items):
    c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10 = layout.columns(fields)
    c0.write(item['id'])
    c1.write(item['age'])
    c2.write(item['gender'])
    c3.write(item['ethnicity'])
    c4.write(item['race'])
    c5.write(item['stay'])
    c6.write(item['admission'])
    c7.write(item['costs'])
    c8.write(item['description'])
    c9.write(item['hospital_name'])
    delete = c10.button('Excluir', key=str(item['id']))
    
    if delete:
      banco.delete('pacient', item['id'])
      st.experimental_rerun()
      
def update_doencas(at):
  with at.form(key="update_doencas", clear_on_submit = False):
    c1, c2 = st.columns((1, 1))
    last_code = c1.number_input(label="Código APR DRG", step=1, )
    new_code = c2.number_input(label='Novo Código APR DRG', step=1)
    update_description = st.text_input(label="Descrição do Diagnóstico")
    update_serverity_descrip = st.selectbox(
      label="Descrição da gravidade da doença", 
      options=['',"Menor", "Moderdo", "Maior", "Extremo"]
    )
    update_risk_mortality = st.selectbox(
      label="Risco de Mortalidade", 
      options=['',"Menor", "Moderdo", "Maior", "Extremo"]
    )
    update_medical_surgical = st.selectbox(
      label="Tipo de Caso", 
      options=['', "Cirurgico", "Médico", "Outro"]
    )
    update_button = st.form_submit_button("Atualizar")
    
    #('code INT PRIMARY KEY, description, severity_description TEXT, risk_mortality TEXT, medical_surgical TEXT')
    if update_button:
      update_txt= ''
      if(update_description != ''):
        update_txt += f' description="{update_description}"'
      if(update_serverity_descrip != ''):
        update_txt += f' severity_description="{update_serverity_descrip}"'
      if(update_risk_mortality != ''):
        update_txt += f' risk_mortality="{update_risk_mortality}"'
      if(update_medical_surgical != ''):
        update_txt += f' medical_surgical="{update_medical_surgical}"'
      if(new_code != last_code):
        update_txt += f' id="{new_code}"'
      print(update_txt.replace('" ', '", '))
      if(banco.update('illness', update_txt.replace('" ', '", '), last_code) == 200):
        at.title(':green[Doencas atualizado com sucesso]')
      else:
        at.title(':orange[Doencas não cadastrado]') 
      sleep(.5)
      st.experimental_rerun()

insert, at = st.tabs(["Inserir Doencas", "Procurar Doencas"])
inputs_doencas(insert)
update_doencas(at)

read = st.container()
read_doencas(read, at)

