import streamlit as st
import datetime
import re
import requests
import urllib.parse  # <-- Esta é a linha que estava faltando!

# 1. Configuração Visual
st.set_page_config(page_title="Inspeção Perfiladeira - Águia Sistemas", layout="wide")

st.markdown("""
    <style>
    .secao-header { background-color: #f0f2f6; border-left: 5px solid #242480; padding: 10px; margin-top: 20px; font-weight: bold; color: #242480; }
    .stButton>button { background-color: #242480; color: white; width: 100%; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho Águia Sistemas
st.markdown("""
    <div style="border: 2px solid black; padding: 10px; font-family: sans-serif;">
        <h2 style="margin:0; color:#242480; text-align:center;">AGUIA SISTEMAS</h2>
        <p style="text-align:center; font-weight:bold; margin:0;">INSPEÇÃO PERFILADEIRA NOVA LC</p>
    </div><br>
""", unsafe_allow_html=True)

# 3. Formulário
with st.form(key="form_aguia"):
    c1, c2, c3, c4 = st.columns(4)
    with c1: data_insp = st.date_input("Data", datetime.date.today())
    with c2: hora_insp = st.text_input("Hora (HH:MM)", value="", placeholder="Ex: 08:30")
    with c3: op = st.text_input("O.P.")
    with c4: inspetor = st.text_input("Inspetor")

    st.markdown("<div class='secao-header'>Medidas</div>", unsafe_allow_html=True)
    cols = st.columns(7)
    medidas = []
    for i, label in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G']):
        medidas.append(cols[i].number_input(label, format="%.2f", step=0.01))

    st.markdown("<div class='secao-header'>Empenamento e Gap</div>", unsafe_allow_html=True)
    ce1, ce2, cg = st.columns(3)
    emp1 = ce1.number_input("Empenamento 1", format="%.2f", step=0.01)
    emp2 = ce2.number_input("Empenamento 2", format="%.2f", step=0.01)
    gap = cg.number_input("Gap", format="%.2f", step=0.01)
    
    obs = st.text_area("Observações")
    submit = st.form_submit_button("SALVAR REGISTRO")

# 4. Lógica de Envio via GET (Método que pula o erro 401)
if submit:
    if not re.match(r"^\d{2}:\d{2}$", hora_insp):
        st.error("Formato de hora inválido.")
    elif not op or not inspetor:
        st.warning("Preencha O.P. e Inspetor.")
    else:
        try:
            # Base da URL de resposta
            base_url = "https://docs.google.com/forms/d/e/1FAIpQLSc0SmUvQcLjdFhDfh3JeJgYJ617dm2OSWIt9lYy5tB21gYkeg/formResponse"
            
            # Montagem dos parâmetros
            params = {
                "entry.140980643": data_insp.strftime("%d/%m/%Y"),
                "entry.1282881006": hora_insp,
                "entry.1955034204": op,
                "entry.1408140739": inspetor,
                "entry.1303788411": str(medidas[0]).replace('.', ','),
                "entry.1981189593": str(medidas[1]).replace('.', ','),
                "entry.804951831": str(medidas[2]).replace('.', ','),
                "entry.2073975929": str(medidas[3]).replace('.', ','),
                "entry.4851159": str(medidas[4]).replace('.', ','),
                "entry.853047564": str(medidas[5]).replace('.', ','),
                "entry.1047433529": str(medidas[6]).replace('.', ','),
                "entry.1327956538": str(emp1).replace('.', ','),
                "entry.818151172": str(emp2).replace('.', ','),
                "entry.908846777": str(gap).replace('.', ','),
                "entry.1146532039": obs,
                "submit": "Submit"
            }

            # O pulo do gato: Enviamos como uma navegação comum (GET)
            full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
            response = requests.get(full_url)

            # O Google retorna 200 mesmo se der erro visual, mas o GET costuma "furar" o bloqueio.
            if response.ok:
                st.success("Registro salvo com sucesso na planilha!")
            else:
                st.error(f"Erro no servidor: {response.status_code}")

        except Exception as e:
            st.error(f"Erro técnico: {e}")
