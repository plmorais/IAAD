import streamlit as st

st.title("Hospital")

with st.form(key="include_hospital"):
    input_hospital_code = st.number_input(label="Código do Hospital")
    input_hospital_name = st.text_input(label="Nome do Hospital")
    input_service_area = st.text_input(label="Area de Serviço")
    input_county = st.text_input(label="Condado")
    imput_button_submit = st.form_submit_button("Enviar")

if imput_button_submit:
    st.write(f'Código do Hospital: {input_hospital_code}') 
    st.write(f'Nome do Hospital: {input_hospital_name}') 
    st.write(f'Area de Serviço: {input_service_area}')
    st.write(f'Condado: {input_county}')