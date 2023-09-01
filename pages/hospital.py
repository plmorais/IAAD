import streamlit as st
from model.banco import Banco
from time import sleep
banco = Banco()
data_hospital = ()
st.title("Hospital")

def inputs_hospital(layout, key='include_hospital'):

  with layout.form(key=f"{key}", clear_on_submit = False):
    input_hospital_code = st.number_input(label="Código do Hospital", step=1)
    input_hospital_name = st.text_input(label="Nome do Hospital")
    input_service_area = st.text_input(label="Area de Serviço")
    input_county = st.text_input(label="Condado")
    input_button_submit = st.form_submit_button("Enviar")
    
    if input_button_submit:
      flag = [
        input_county=='',
        input_service_area=='',
        input_hospital_name=='',
      ]
      if(flag.count(True) == 0):
        hospital = (
          input_hospital_code,
          input_hospital_name,
          input_service_area,
          input_county
        )
        if(banco.insert('hospital', hospital) == 200):
          layout.title(':green[Hospital cadastrado com sucesso]')
        else:
          layout.title(':orange[já está cadastrado]')     
      else:
        layout.title(':red[Deixou campos em banco]')

def read_hospital(layout, at):
  container = layout.container()
  layout.title('Consultar Dados')

  colunas = layout.columns((1,2,2,2,1.5))
  campos = ['Facility ID','Facility Name','Heal Service Area','Hospital County','Excluir']
  for coluna, campo in zip(colunas,campos):
    coluna.write(campo)
  items = banco.get_all('hospital')

  for i, item in enumerate(items):
    c1,c2,c3,c4,c6 = layout.columns((1,2,2,2,1.5))
    c1.write(item[0])
    c2.write(item[1])
    c3.write(item[2])
    c4.write(item[3])
    delete = c6.button('Excluir', key=str(item[0]))
    
    if delete:
      banco.delete('hospital', item[0])
      st.experimental_rerun()      
    
def update_hospital(at):
  with at.form(key="update_hospital", clear_on_submit = False):
    c1, c2 = st.columns((1, 1))
    last_code = c1.number_input(label="Código do Hospital", step=1, )
    new_code = c2.number_input(label="Novo código para o Hospital", step=1, )
    update_name = st.text_input(label="Nome do Hospital")
    update_service = st.text_input(label="Area de Serviço")
    update_county = st.text_input(label="Condado")
    update_button = st.form_submit_button("Atualizar")
    
    #('id INT PRIMARY KEY, hospital_name TEXT NOT NULL, service_area TEXT NOT NULL, county TEXT NOT NULL')
    if update_button:
      update_txt= ''
      if(update_name != ''):
        update_txt += f'hospital_name="{update_name}"'
      if(update_county != ''):
        update_txt += f' county="{update_county}"'
      if(update_service != ''):
        update_txt += f' service_area="{update_service}"'
      if(new_code != last_code):
        update_txt += f' id="{new_code}"'
      print(update_txt.replace('" ', '", '))
      if(banco.update('hospital', update_txt.replace('" ', '", '), last_code) == 200):
        at.title(':green[Hospital atualizado com sucesso]')
      else:
        at.title(':orange[Hospital não cadastrado]') 
      sleep(.5)
      st.experimental_rerun()

insert, read, at = st.tabs(["Inserir Hospital", "Procurar Hospital", 'Atualizar'])
inputs_hospital(insert)
read_hospital(read, at)
update_hospital(at)


