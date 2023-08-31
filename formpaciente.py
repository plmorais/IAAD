# IAAD
import streamlit as st

st.title("Formulário de paciente")

st.sidebar.title("Menu")
st.sidebar.selectbox ('O que voce está procurando ?',['Hospital','Paciente','Doença'])

with st.form(key="include_paciente"):
    input_age = st.number_input(label="Insira sua idade", format="%d", step=1)
    input_gender = st.selectbox(label="Selecione seu gênero",options=["Feminino","Masculino","Outro"])
    input_race = st.selectbox(label="Selecione sua raça",options=["Branco","Preto","Outro"])
    input_ethnicity = st.selectbox(label="Insira seu etnia",options=["Não é espanhol/hispânico","Espanhol/hispânico","Outro"])
    input_stay = st.number_input(label="Insira seu tempo de estadia", format="%d", step=1)
    input_admission = st.selectbox(label="Insira qual seu tipo de admissão",options=["Emergência","Eletivo","Outro"])
    input_disposition = st.selectbox(label="Insira sua dispoição",options=["Casa ou autocuidado","Casa com serviços de saúde domiciliar","Outro"])
    input_costs = st.number_input(label="Insira seu custo")
    input_button_submit = st.form_submit_button("Enviar")

if input_button_submit :
    st.write(f'Idade: {input_age}')
    st.write(f'Gênero:{input_gender}')
    st.write(f'Raça:{input_race}')
    st.write(f'Etnia:{input_ethnicity}')
    st.write(f'Tempo de estadia:{input_stay}')
    st.write(f'Qual seu tipo de admissão:{input_admission}')
    st.write(f'Qual sua dispoição:{input_disposition}')
    st.write(f'Qual seu custo:{input_costs}')
