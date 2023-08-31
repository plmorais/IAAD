import streamlit as st
from model.banco import Banco

banco = Banco()
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

      


def read_hospital(layout):
  container = layout.container()
  layout.title('Consultar Dados')

  colunas = layout.columns((1,2,2,2,1.5,1.5))
  campos = ['Facility ID','Facility Name','Heal Service Area','Hospital County','Editar','Excluir']
  for coluna, campo in zip(colunas,campos):
    coluna.write(campo)
  items = banco.get_all('hospital')

  for i, item in enumerate(items):
    c1,c2,c3,c4,c5,c6 = layout.columns((1,2,2,2,1.5,1.5))
    c1.write(item[0])
    c2.write(item[1])
    c3.write(item[2])
    c4.write(item[3])
    btn_edit = c5.button('Editar', key=f'edit{item[0]}')
    delete = c6.button('Excluir', key=str(item[0]))
    
    if delete:
      banco.delete('hospital', item[0])
      st.experimental_rerun()
    if btn_edit:
      with container.form(key=f"updata", clear_on_submit = False):
        update_hospital_code = st.number_input(label="Código do Hospital", step=1, value=item[0])
        update_hospital_name = st.text_input(label="Nome do Hospital", value=item[1])
        update_service_area = st.text_input(label="Area de Serviço", value=item[2])
        update_county = st.text_input(label="Condado", value=item[3])
        btn_updata = st.form_submit_button("Atualizar")
        if btn_updata:
          print(item)
    
  
  

insert, read = st.tabs(["Inserir Hospital", "Procurar Hospital"])
inputs_hospital(insert)
read_hospital(read)



