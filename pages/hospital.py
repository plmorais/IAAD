import streamlit as st
from model.banco import Banco

st.title("Hospital")

def inputs_hospital():
  with st.form(key="include_hospital", clear_on_submit = False):
    input_hospital_code = st.number_input(label="Código do Hospital")
    input_hospital_name = st.text_input(label="Nome do Hospital")
    input_service_area = st.text_input(label="Area de Serviço")
    input_county = st.text_input(label="Condado")
    imput_button_submit = st.form_submit_button("Enviar")

  if imput_button_submit:
    hospital = (
      input_hospital_code,
      input_hospital_name,
      input_service_area,
      input_county
    )
    banco = Banco()
    banco.insert('hospital', hospital)
    

inputs_hospital()