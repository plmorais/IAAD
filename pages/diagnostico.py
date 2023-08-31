import streamlit as st;
from model.banco import Banco

st.title("Diagnóstico")

with st.form(key="include_diagnostic"):
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