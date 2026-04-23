import streamlit as st
import datetime
import re
import requests

# --- MANTIVE SEU CABECALHO E CSS IGUAIS ---
st.set_page_config(page_title="Inspecao Perfiladeira - Aguia Sistemas", layout="wide")

st.markdown("""
    <style>
    .secao-header { background-color: #f0f2f6; border-left: 5px solid #242480; padding: 10px 15px; margin-top: 25px; font-weight: bold; color: #242480; text-transform: uppercase; font-size: 14px; }
    .stButton>button { background-color: #242480; color: white; border-radius: 5px; width: 100%; font-weight: bold; border: none; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <table style="width:100%; border-collapse: collapse; border: 2px solid black; font-family: sans-serif;">
        <tr>
            <td rowspan="3" style="width: 20%; border: 2px solid black; text-align: center; padding: 10px;">
                <h2 style="margin:0; color:#242480;">AGUIA</h2>
                <small>S I S T E M A S</small>
            </td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;"><b>Data da Edicao:</b> 29/01/2026</td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;"><b>Autor(a):</b> Matheus Chila</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Revisao:</b> 6</td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Verificado:</b> Wagner Kazuki de Azambuja</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Setor:</b> Qualidade Industrial</td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Inspecao:</b> a cada 60 minutos</td>
        </tr>
    </table>
    <div style="background-color: #242480; color: white; text-align: center; padding: 12px; font-weight: bold; font-size: 20px; border: 2px solid black; border-top: none;">
        INSPECAO PERFILADEIRA NOVA LC
    </div>
    <br>
""", unsafe_allow_html=True)

with st.form(key="form_inspecao"):
    st.markdown("<div class='secao-header'>Identificacao</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: data_insp = st.date_input("Data", datetime.date.today())
    with c2: hora_insp = st.text_input("Hora (HH:MM)", value="", placeholder="Ex: 14:30")
    with c3: op = st.text_input("O.P.")
    with c4: inspetor = st.text_input("Inspetor")

    st.markdown("<div class='secao-header'>Medidas Registradas</div>", unsafe_allow_html=True)
    col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
    with col_a: med_a = st.number_input("A", format="%.2f", step=0.01)
    with col_b: med_b = st.number_input("B", format="%.2f", step=0.01)
    with col_c: med_c = st.number_input("C", format="%.2f", step=0.01)
    with col_d: med_d = st.number_input("D", format="%.2f", step=0.01)
    with col_e: med_e = st.number_input("E", format="%.2f", step=0.01)
    with col_f: med_f = st.number_input("F", format="%.2f", step=0.01)
    with col_g: med_g = st.number_input("G", format="%.2f", step=0.01)

    st.markdown("<div class='secao-header'>Empenamento e Gap</div>", unsafe_allow_html=True)
    col_e1, col_e2, col_gp = st.columns(3)
    with col_e1: emp1 = st.number_input("Empenamento 1", format="%.2f", step=0.01)
    with col_e2: emp2 = st.number_input("Empenamento 2", format="%.2f", step=0.01)
    with col_gp: gap = st.number_input("Gap", format="%.2f", step=0.01)

    st.markdown("<div class='secao-header'>Observacoes</div>", unsafe_allow_html=True)
    observacoes = st.text_area("Relatorio de anomalias:", height=80)

    submit_button = st.form_submit_button(label="SALVAR REGISTRO")

# --- LOGICA DE ENVIO REFORMULADA ---
if submit_button:
    if not re.match(r"^\d{2}:\d{2}$", hora_insp):
        st.error("Erro: Formato de hora invalido (HH:MM).")
    elif not op or not inspetor:
        st.warning("Atencao: O.P. e Inspetor sao obrigatorios.")
    else:
        try:
            # URL pura de envio
            URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSc0SmUvQcLjdFhDfh3JeJgYJ617dm2OSWIt9lYy5tB21gYkeg/formResponse"
            
            # Convertendo TUDO para string e trocando ponto por virgula se necessario
            payload = {
                "entry.140980643": data_insp.strftime("%d/%m/%Y"), 
                "entry.1282881006": str(hora_insp),
                "entry.1955034204": str(op),
                "entry.1408140739": str(inspetor),
                "entry.1303788411": str(med_a).replace('.', ','),
                "entry.1981189593": str(med_b).replace('.', ','),
                "entry.804951831": str(med_c).replace('.', ','),
                "entry.2073975929": str(med_d).replace('.', ','),
                "entry.4851159": str(med_e).replace('.', ','),
                "entry.853047564": str(med_f).replace('.', ','),
                "entry.1047433529": str(med_g).replace('.', ','),
                "entry.1327956538": str(emp1).replace('.', ','),
                "entry.818151172": str(emp2).replace('.', ','),
                "entry.908846777": str(gap).replace('.', ','),
                "entry.1146532039": str(observacoes)
            }

            # Envio simplificado (sem headers complexos que podem causar 401)
            response = requests.post(URL_FORM, data=payload)

            if response.status_code == 200 or response.status_code == 302:
                st.success("Registro enviado com sucesso!")
            else:
                st.error(f"Erro {response.status_code}. Tente clicar no link do forms uma vez no seu navegador para 'validar' seu IP.")

        except Exception as e:
            st.error(f"Erro: {e}")
