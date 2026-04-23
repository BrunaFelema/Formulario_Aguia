import streamlit as st
import datetime
import re
import requests
import json

# 1. Configuração da Página
st.set_page_config(page_title="Inspeção Perfiladeira - Águia Sistemas", layout="wide")

# Estilização CSS para manter o padrão visual da Águia Sistemas
st.markdown("""
    <style>
    .secao-header {
        background-color: #f0f2f6;
        border-left: 5px solid #242480;
        padding: 10px 15px;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: bold;
        color: #242480;
        text-transform: uppercase;
        font-size: 14px;
    }
    .stButton>button {
        background-color: #242480;
        color: white;
        border-radius: 5px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Cabeçalho Técnico (Layout da Tabela)
st.markdown("""
    <table style="width:100%; border-collapse: collapse; border: 2px solid black; font-family: sans-serif;">
        <tr>
            <td rowspan="3" style="width: 20%; border: 2px solid black; text-align: center; padding: 10px;">
                <h2 style="margin:0; color:#242480;">AGUIA</h2>
                <small>S I S T E M A S</small>
            </td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;"><b>Data da Edição:</b> 29/01/2026</td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;"><b>Autor(a):</b> Matheus Chila</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Revisão:</b> 6</td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Verificado:</b> Wagner Kazuki de Azambuja</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Setor:</b> Qualidade Industrial</td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;"><b>Inspeção:</b> a cada 60 minutos</td>
        </tr>
    </table>
    <div style="background-color: #242480; color: white; text-align: center; padding: 12px; font-weight: bold; font-size: 20px; border: 2px solid black; border-top: none;">
        INSPEÇÃO PERFILADEIRA NOVA LC
    </div>
    <br>
""", unsafe_allow_html=True)

# 3. Formulário de Registro
with st.form(key="form_inspecao"):
    st.markdown("<div class='secao-header'>Identificação da Inspeção</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_insp = st.date_input("Data", datetime.date.today())
    with col2:
        hora_insp = st.text_input("Hora (HH:MM)", placeholder="Ex: 14:30")
    with col3:
        op = st.text_input("O.P.")
    with col4:
        inspetor = st.text_input("Inspetor")

    st.markdown("<div class='secao-header'>Medidas Registradas (A - G)</div>", unsafe_allow_html=True)
    col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
    with col_a: med_a = st.number_input("A", format="%.2f", step=0.01)
    with col_b: med_b = st.number_input("B", format="%.2f", step=0.01)
    with col_c: med_c = st.number_input("C", format="%.2f", step=0.01)
    with col_d: med_d = st.number_input("D", format="%.2f", step=0.01)
    with col_e: med_e = st.number_input("E", format="%.2f", step=0.01)
    with col_f: med_f = st.number_input("F", format="%.2f", step=0.01)
    with col_g: med_g = st.number_input("G", format="%.2f", step=0.01)

    st.markdown("<div class='secao-header'>Empenamento e Gap</div>", unsafe_allow_html=True)
    col_emp1, col_emp2, col_gap = st.columns(3)
    with col_emp1: emp1 = st.number_input("Empenamento 1", format="%.2f", step=0.01)
    with col_emp2: emp2 = st.number_input("Empenamento 2", format="%.2f", step=0.01)
    with col_gap: gap = st.number_input("Gap", format="%.2f", step=0.01)

    st.markdown("<div class='secao-header'>Observações</div>", unsafe_allow_html=True)
    observacoes = st.text_area("Relatório de anomalias:", height=80)

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="SALVAR REGISTRO NA PLANILHA")

# 4. Lógica de Envio para o Google Sheets via API (Apps Script)
if submit_button:
    # Validação simples
    if not re.match(r"^\d{2}:\d{2}$", hora_insp):
        st.error("Erro: Formato de hora inválido. Use HH:MM.")
    elif not op or not inspetor:
        st.warning("Atenção: O.P. e Inspetor são obrigatórios.")
    else:
        # A SUA URL DA API QUE VOCÊ GEROU NO PASSO ANTERIOR
        URL_API = "https://script.google.com/macros/s/AKfycbwBwSPWVtbXBYzm5dMjsMVnmlLftZ6O0iyYYEYp43jOl3_vt3nQOKh4WFZYWPA5qhCl/exec"
        
        # Criando o pacote de dados (JSON)
        payload = {
            "data": data_insp.strftime("%d/%m/%Y"),
            "hora": hora_insp,
            "op": op,
            "inspetor": inspetor,
            "a": str(med_a).replace('.', ','),
            "b": str(med_b).replace('.', ','),
            "c": str(med_c).replace('.', ','),
            "d": str(med_d).replace('.', ','),
            "e": str(med_e).replace('.', ','),
            "f": str(med_f).replace('.', ','),
            "g": str(med_g).replace('.', ','),
            "emp1": str(emp1).replace('.', ','),
            "emp2": str(emp2).replace('.', ','),
            "gap": str(gap).replace('.', ','),
            "obs": observacoes
        }

        try:
            # Envia os dados para o Apps Script
            with st.spinner('Salvando dados na planilha...'):
                response = requests.post(URL_API, data=json.dumps(payload))
            
            if response.status_code == 200:
                st.success("✅ Registro enviado com sucesso para a planilha da Águia Sistemas!")
                st.balloons()
            else:
                st.error(f"Erro no servidor Google: {response.status_code}. Verifique se a implantação está como 'Qualquer pessoa'.")
        
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
