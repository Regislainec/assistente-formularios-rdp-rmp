import io
import zipfile
from jinja2 import Template
import streamlit as st

@st.cache_resource
def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return Template(f.read())

st.set_page_config(page_title="Assistente de Preenchimento", layout="centered")
st.title("Assistente de Preenchimento de Formulários `.odt`")

st.header("Dados Gerais")
codigo_rdp = st.text_input("Código RDP", "000-25")
codigo_rmp = st.text_input("Código RMP", "000-25")
cliente = st.text_input("Cliente", "CONCESSIONÁRIA ABC")
preco_mercado = st.text_input("Preço de Mercado (R$)", "120.00")
contato = st.text_input("Contato", "João Silva")
potencial_mercado = st.text_input("Potencial de Mercado (pçs/ano)", "5000")
codigo_cliente = st.text_input("Código do Produto do Cliente", "CLI-456")
codigo_intelli = st.text_input("Código Intelli", "QQ-000")
motivo = st.text_input("Motivo", "Necessidade de Mercado")
processos = st.multiselect("Processos Envolvidos", ["Estampagem", "Usinagem", "Montagem", "Repuxo", "Fundição", "Injeção de Termoplásticos", "Trefilação", "Extrusão"], default=["Estampagem"])
ferramentas = st.multiselect("Ferramentas Envolvidas", ["Estampagem", "Usinagem", "Montagem", "Repuxo", "Fundição", "Injeção de Termoplásticos", "Trefilação", "Extrusão"], default=["Montagem"])
anexos = st.multiselect("Anexos", ["Desenhos", "Fotos", "Catálogos", "Amostra", "Especificações", "Normas"], default=["Desenhos", "Catálogos"])
observacoes = st.text_area("Observações", "Produto urgente para novo cliente.")
data_inicio = st.date_input("Data de Início do Processo")
data_conclusao = st.date_input("Data de Conclusão do Processo")
engenharia_aprovacao = st.text_input("Aprovação Engenharia (Nome)", "Maria Souza")
comercial_aprovacao = st.text_input("Aprovação Comercial (Nome)", "Carlos Lima")
cliente_aprovacao = st.checkbox("Cliente Aprovado?", value=True)

if st.button("Gerar Formulários `.odt` e baixar ZIP"):
    tplA = load_template("templates/SQI004A_template.txt")
    tplH = load_template("templates/SQI004H_template.txt")
    tplE = load_template("templates/SQI004E_template.txt")

    dados = {
        "codigo_rdp": codigo_rdp,
        "codigo_rmp": codigo_rmp,
        "cliente": cliente,
        "preco_mercado": preco_mercado,
        "contato": contato,
        "potencial_mercado": potencial_mercado,
        "codigo_cliente": codigo_cliente,
        "codigo_intelli": codigo_intelli,
        "motivo": motivo,
        "processos": processos,
        "ferramentas": ferramentas,
        "anexos": anexos,
        "observacoes": observacoes,
        "data_inicio": data_inicio.strftime('%d/%m/%Y'),
        "data_conclusao": data_conclusao.strftime('%d/%m/%Y'),
        "engenharia_aprovacao": engenharia_aprovacao,
        "comercial_aprovacao": comercial_aprovacao,
        "cliente_aprovacao": cliente_aprovacao
    }

    txtA = tplA.render(dados)
    txtH = tplH.render(dados)
    txtE = tplE.render(dados)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('saida_SQI004A.odt', txtA)
        zipf.writestr('saida_SQI004H.odt', txtH)
        zipf.writestr('saida_SQI004E.odt', txtE)
    buffer.seek(0)

    st.download_button("Baixar ZIP com os formulários", data=buffer, file_name="formularios_preenchidos.zip", mime="application/zip")
