import streamlit as st;

st.title("Diagnóstico")

with st.form(key="include_diagnostic"):
    input_description = st.text_input(label="Descrição do Diagnóstico")
    input_serverity_descrip = st.selectbox(label="Descrição da gravidade da doença", options=["Menor", "Moderdo", "Maior", "Extremo"])
    input_risk_mortality = st.selectbox(label="Risco de Mortalidade", options=["Menor", "Moderdo", "Maior", "Extremo"])
    input_medical_surgical = st.selectbox(label="Tipo de Caso", options=["Cirurgico", "Médico", "Outro"])
    imput_button_submit = st.form_submit_button("Enviar")

if imput_button_submit:
    st.write(f'Decrição do Diagnostico: {input_description}') 
    st.write(f'Descrição da gravidade da doença: {input_serverity_descrip}')
    st.write(f'Risco de Mortalidade: {input_risk_mortality}')
    st.write(f'Tipo de Caso: {input_medical_surgical}')