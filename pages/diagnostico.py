import streamlit as st;
from model.banco import Banco
from time import sleep

st.title("Diagnóstico")
banco = Banco()

def inputs_doencas(layout, ):
  with layout.form(key="include_diagnostic", clear_on_submit = False):
    input_apr_drg_code = st.number_input(label='Código APR DRG', step=1)
    input_description = st.text_input(label="Descrição do Diagnóstico")
    input_serverity_descrip = st.selectbox(
      label="Descrição da gravidade da doença", 
      options=['',"Menor", "Moderdo", "Maior", "Extremo"]
    )
    input_risk_mortality = st.selectbox(
      label="Risco de Mortalidade", 
      options=['',"Menor", "Moderdo", "Maior", "Extremo"]
    )
    input_medical_surgical = st.selectbox(
      label="Tipo de Caso", 
      options=['', "Cirurgico", "Médico", "Outro"]
    )
    submit = st.form_submit_button("Enviar")
    # (code, description, severity_description, risk_mortality, medical_surgical)
    
    if submit:
      flag = [
        input_description == '',
        input_serverity_descrip == '',
        input_risk_mortality == '',
        input_medical_surgical == ''
      ]
      if(flag.count(True) == 0):
        illness = (
          input_apr_drg_code,
          input_description,
          input_serverity_descrip,
          input_risk_mortality,
          input_medical_surgical
        )
        banco = Banco()
        if(banco.insert('illness', illness) == 200):
          st.title(':green[Doença cadastrado com sucesso]')
        else:
          st.title(':orange[Código APR DRG já está cadastrado]')
      else:
        st.title(f':red[Deixou {flag.count(True)} campos em banco]')
      
def read_doencas(layout, at):
  container = layout.container()
  layout.title('Consultar Dados')
  fields = (1,3,2,2,1.2,1.5,)
  colunas = layout.columns(fields)
  campos = ['Code','Description','Servity Desc.','Risk Mortality', 'Surgical', 'Excluir']
  for coluna, campo in zip(colunas,campos):
    coluna.write(campo)
  items = banco.get_all('illness')
  #(code, description, severity_description, risk_mortality, medical_surgical)
  for i, item in enumerate(items):
    layout.write('<hr>', unsafe_allow_html=True)
    c1,c2,c3,c4, c5,c6 = layout.columns(fields)
    c1.write(item[0])
    c2.write(item[1])
    c3.write(item[2])
    c4.write(item[3])
    c5.write(item[4])
    delete = c6.button('Excluir', key=str(item[0]))
    
    if delete:
      banco.delete('illness', item[0])
      st.experimental_rerun()
      
def update_doencas(at):
  with at.form(key="update_doencas", clear_on_submit = False):
    c1, c2 = st.columns((1, 1))
    last_code = c1.number_input(label="Código APR DRG", step=1, )
    new_code = c2.number_input(label='Novo Código APR DRG', step=1)
    update_description = st.text_input(label="Descrição do Diagnóstico")
    update_serverity_descrip = st.selectbox(
      label="Descrição da gravidade da doença", 
      options=['',"Menor", "Moderado", "Maior", "Extremo"]
    )
    update_risk_mortality = st.selectbox(
      label="Risco de Mortalidade", 
      options=['',"Menor", "Moderado", "Maior", "Extremo"]
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
        update_txt += f' code={new_code}'
      print(update_txt.replace('" ', '", '), last_code)
      if(banco.update('illness', update_txt.replace('" ', '", '), last_code) == 200):
        at.title(':green[Doencas atualizado com sucesso]')
      else:
        at.title(':orange[Doencas não cadastrado]') 
      sleep(.5)
      st.experimental_rerun()

insert, read, at = st.tabs(["Inserir Doencas", "Procurar Doencas", 'Atualizar'])
inputs_doencas(insert)
read_doencas(read, at)
update_doencas(at)
