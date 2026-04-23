import streamlit as st
import datetime
import re
import requests
import json

# 1. CONFIGURAÇÃO DA PÁGINA (WIDE LAYOUT PARA REPLICAR O MODELO)
st.set_page_config(page_title="Inspeção Perfiladeira - Águia Sistemas", layout="wide")

# 2. DEFINIÇÃO DE CORES E ESTILOS CSS PROFISSIONAIS (INSPIRADO NA IMAGE_3.PNG)
AZUL_AGUIA = "#1D3557" # Azul escuro do logo
CINZA_FUNDO_INPUT = "#F0F2F6"
VERDE_BADGE = "#D1FAE5" # Verde claro para o status
VERDE_TEXTO_BADGE = "#065F46" # Verde escuro para o texto do status

st.markdown(f"""
    <style>
    /* Ocultar elementos padrão do Streamlit para um visual mais limpo */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Configuração Geral de Fontes */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Estilização da Sidebar (Barra Lateral) */
    .css-1d391kg {{
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }}
    .sidebar-logo {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 60%;
        margin-top: 30px;
        margin-bottom: 20px;
    }}
    .sidebar-title {{
        text-align: center;
        font-size: 14px;
        color: #757575;
        font-weight: 500;
        margin-top: 10px;
    }}
    .status-badge {{
        background-color: {VERDE_BADGE};
        color: {VERDE_TEXTO_BADGE};
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        width: 80%;
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px;
    }}

    /* Estilização do Conteúdo Principal */
    .main .block-container {{
        padding-top: 40px;
    }}

    /* Estilização do Card de Cabeçalho (DADOS DE CONTROLE) */
    .header-card {{
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 20px;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }}
    .header-logo {{
        width: 60px;
        margin-right: 20px;
        margin-top: 10px;
    }}
    .header-content {{
        flex-grow: 1;
    }}
    .header-title-main {{
        color: #757575;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 14px;
        margin-bottom: 15px;
    }}
    
    /* Título Principal da Página */
    .page-title {{
        color: {AZUL_AGUIA};
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 30px;
    }}

    /* Estilização dos Títulos de Seção (Barra Azul) */
    .section-header {{
        border-left: 5px solid {AZUL_AGUIA};
        background-color: #f7f9fc;
        color: {AZUL_AGUIA};
        padding: 12px 20px;
        text-transform: uppercase;
        font-weight: 600;
        font-size: 15px;
        border-radius: 4px;
        margin-top: 25px;
        margin-bottom: 15px;
    }}

    /* Estilização dos Inputs (Fundo Cinza) */
    .stTextInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {{
        background-color: {CINZA_FUNDO_INPUT};
        border-radius: 6px;
        border: 1px solid #D1D5DB;
        color: #374151;
        font-size: 14px;
    }}
    .stNumberInput>div>div>input {{
        background-color: {CINZA_FUNDO_INPUT};
        border-radius: 6px;
        border: 1px solid #D1D5DB;
        color: #374151;
        font-size: 14px;
        padding-top: 8px;
        padding-bottom: 8px;
    }}

    /* Estilização do Botão Salvar (Azul Escuro) */
    .stButton>button {{
        background-color: {AZUL_AGUIA};
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
        border: none;
        padding: 12px;
        margin-top: 20px;
        transition: background-color 0.2s;
    }}
    .stButton>button:hover {{
        background-color: #162C4A;
        color: white;
    }}

    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (BARRA LATERAL) - CONFORME IMAGE_3.PNG
# Usando Markdown para carregar a imagem centralizada e estilizada
st.sidebar.markdown(f'<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9S9S-h1hI1_D5gNq_gYn-kGjD8GjQkY5Qjg&s" class="sidebar-logo">', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-title">Sistema Integrado</p>', unsafe_allow_html=True)

# Badge de status conectado
st.sidebar.markdown(f'<div class="status-badge">🟢 BD Conectado</div>', unsafe_allow_html=True)


# 4. CONTEÚDO PRINCIPAL
# A. Card de Cabeçalho (DADOS DE CONTROLE) - REPLICANDO IMAGE_3.PNG
# Mapeando os dados de controle que você já tinha para o novo visual
data_edicao = "29/01/2026"
revisao = "6"
autor = "Matheus Chila"
verificado_por = "Wagner Kazuki de Azambuja"
setor = "Qualidade Industrial"
inspecao = "a cada 60 minutos"

st.markdown(f"""
    <div class="header-card">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9S9S-h1hI1_D5gNq_gYn-kGjD8GjQkY5Qjg&s" class="header-logo">
        <div class="header-content">
            <div class="header-title-main">DADOS DE CONTROLE</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <div style="font-size:13px;"><b>Revisão:</b> {revisao}</div>
                <div style="font-size:13px;"><b>Autor:</b> {autor}</div>
                <div style="font-size:13px;"><b>Autorizado por:</b> {verificado_por}</div>
                <div style="font-size:13px;"><b>Setor:</b> {setor}</div>
                <div style="font-size:13px;"><b>Doc:</b> Inspeção Perfiladeira</div>
                <div style="font-size:13px;"><b>Última Atualização:</b> {data_edicao}</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# B. Título Principal da Página
st.markdown('<p class="page-title">INSPEÇÃO PERFILADEIRA NOVA LC</p>', unsafe_allow_html=True)

# C. Formulário de Dados
with st.form(key="form_inspecao"):
    
    # Seção 1: Identificação
    st.markdown('<div class="section-header">INFORMAÇÕES DA INSPEÇÃO</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        data_insp = st.date_input("Data da Inspeção", datetime.date.today())
    with c2:
        hora_insp = st.text_input("Hora (HH:MM)", placeholder="Ex: 08:30")
    with c3:
        op = st.text_input("O.P.")
    with c4:
        inspetor = st.text_input("Inspetor")

    # Seção 2: Medidas A-G
    st.markdown('<div class="section-header">REGISTRO DE MEDIDAS (A - G)</div>', unsafe_allow_html=True)
    col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
    with col_a: med_a = st.number_input("Medida A", format="%.2f", step=0.01)
    with col_b: med_b = st.number_input("Medida B", format="%.2f", step=0.01)
    with col_c: med_c = st.number_input("Medida C", format="%.2f", step=0.01)
    with col_d: med_d = st.number_input("Medida D", format="%.2f", step=0.01)
    with col_e: med_e = st.number_input("Medida E", format="%.2f", step=0.01)
    with col_f: med_f = st.number_input("Medida F", format="%.2f", step=0.01)
    with col_g: med_g = st.number_input("Medida G", format="%.2f", step=0.01)

    # Seção 3: Empenamentos e Gap
    st.markdown('<div class="section-header">EMPENAMENTO E GAP</div>', unsafe_allow_html=True)
    ce1, ce2, cg = st.columns(3)
    with ce1: emp1 = st.number_input("Empenamento 1", format="%.2f", step=0.01)
    with ce2: emp2 = st.number_input("Empenamento 2", format="%.2f", step=0.01)
    with cg: gap = st.number_input("Gap", format="%.2f", step=0.01)

    # Seção 4: Observações
    st.markdown('<div class="section-header">OBSERVAÇÕES ADICIONAIS</div>', unsafe_allow_html=True)
    observacoes = st.text_area("Relatório de anomalias (Opcional):", height=100)

    # Botão de Envio
    st.markdown('<div style="text-align: right; width: 100%;">', unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="SALVAR REGISTRO NA PLANILHA")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. LÓGICA DE ENVIO (MANTIDA 100% IGUAL À VERSÃO ANTERIOR QUE FUNCIONOU)
if submit_button:
    # Validações Básicas
    if not re.match(r"^\d{2}:\d{2}$", hora_insp):
        st.error("Erro: Formato de hora inválido. Use HH:MM.")
    elif not op or not inspetor:
        st.warning("Atenção: O.P. e Inspetor são obrigatórios.")
    else:
        # A SUA URL DA API - CONTINUA A MESMA
        URL_API = "https://script.google.com/macros/s/AKfycbwBwSPWVtbXBYzm5dMjsMVnmlLftZ6O0iyYYEYp43jOl3_vt3nQOKh4WFZYWPA5qhCl/exec"
        
        # Preparação do Pacote de Dados (Convertendo decimais para ponto flutuante ou string com vírgula para Sheets)
        # Manterei a conversão para string com vírgula conforme fizemos na versão funcional
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
            # Envio dos dados para a API (JSON POST)
            with st.spinner('Gravando dados na planilha...'):
                response = requests.post(URL_API, data=json.dumps(payload))
            
            if response.status_code == 200:
                st.success("✅ Registro enviado com sucesso para a planilha da Águia Sistemas!")
                st.balloons()
            else:
                st.error(f"Erro no servidor Google: {response.status_code}. Contate Matheus Chila.")
        
        except Exception as e:
            st.error(f"Erro de conexão com a planilha: {e}")
