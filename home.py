import streamlit as st
from model.load_data import load_hospitais, load_illnesses, load_pacient

st.title('Carregar Dados')

c1, c2, c3= st.columns((1, 1, 1))

c1.write('Clique no botão para popular a tabela de hospitais')
btn_hospital = c1.button(label='Load Hospitais')

c2.write('Clique no botão para popular a tabela de Doenças')
btn_illness = c2.button(label='Load Doenças')

c3.write('Clique no botão para popular a tabela de Pacientes')
btn_pacient = c3.button(label='Load Pacientes')

if (btn_hospital):
  load_hospitais()
if (btn_illness):
  load_illnesses()
if (btn_pacient):
  load_pacient()