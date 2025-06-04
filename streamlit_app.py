import streamlit as st
import zipfile
import io
from datetime import date

st.set_page_config(page_title="Assistente de Formulários", layout="centered")
st.title("Assistente Automático de Formulários RDP/RMP")

formulario = st.selectbox("Escolha o tipo de formulário", ["SQI004A - Requisitos", "SQI004H - Custos"])
tipo = st.radio("Tipo de Formulário", ["RDP", "RMP"])
codigo_rdp = st.text_input("Código RDP", "001-25")
codigo_rmp = st.text_input("Código RMP", "000-00")
cliente = st.text_input("Cliente", "CONCESSIONÁRIA ALFA")
preco = st.text_input("Preço de Mercado (R$)", "150,00")
contato = st.text_input("Contato", "João Silva")
potencial = st.text_input("Potencial de Mercado", "10.000")
codigo_cliente = st.text_input("Código do Cliente", "AB123")
codigo_intelli = st.text_input("Código Produto Intelli", "QQ-456")
engenharia = st.text_input("Engenharia", "Maria Souza")
comercial = st.text_input("Comercial", "Carlos Lima")
data_inicio = st.date_input("Data de Início", value=date.today())
data_fim = st.date_input("Data Estimada Conclusão", value=date.today())

if st.button("Gerar Formulário"):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        if formulario.startswith("SQI004A"):
            zf.write("templates/SQI004A_modelo.odt", arcname="SQI004A_preenchido.odt")
        elif formulario.startswith("SQI004H"):
            zf.write("templates/SQI004H_modelo.odt", arcname="SQI004H_preenchido.odt")
    buffer.seek(0)
    st.download_button("📥 Baixar Formulário Preenchido", data=buffer, file_name="formulario_gerado.zip", mime="application/zip")
