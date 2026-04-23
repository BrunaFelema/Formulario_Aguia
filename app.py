import streamlit as st
import datetime
import re
import requests
import json

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Inspeção Perfiladeira - Águia Sistemas", layout="wide")

# 2. CSS PARA REPLICAR O VISUAL "RNC" COM CONTEÚDO TÉCNICO
AZUL_AGUIA = "#1D3557"
CINZA_FUNDO_INPUT = "#F0F2F6"

st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    /* Sidebar */
    .sidebar-logo {{ display: block; margin: 30px auto 20px; width: 60%; }}
    .status-badge {{
        background-color: #D1FAE5; color: #065F46; padding: 10px; 
        border-radius: 8px; font-weight: bold; text-align: center; width: 80%; margin: 20px auto;
    }}

    /* Card de Dados de Controle */
    .header-card {{
        background-color: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 10px;
        padding: 20px; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}
    .header-logo {{ width: 60px; margin-right: 20px; }}
    .header-title-label {{ color: #757575; font-weight: 600; text-transform: uppercase; font-size: 12px; margin-bottom: 10px; }}

    /* Títulos de Seção (Barra Azul) */
    .section-header {{
        border-left: 5px solid {AZUL_AGUIA}; background-color: #f7f9fc; color: {AZUL_AGUIA};
        padding: 10px 15px; text-transform: uppercase; font-weight: 600; font-size: 14px;
        border-radius: 0 4px 4px 0; margin: 20px 0 15px 0;
    }}

    /* Tabela de Passos Estilizada */
    .passos-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px; }}
    .passos-table td {{ border: 1px solid #E0E0E0; padding: 8px; }}
    .passo-col-num {{ background-color: #F8FAFC; font-weight: bold; width: 10%; text-align: center; color: {AZUL_AGUIA}; }}

    /* Botão */
    .stButton>button {{
        background-color: {AZUL_AGUIA}; color: white; border-radius: 8px; width: 100%;
        font-weight: bold; border: none; padding: 12px; margin-top: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR
st.sidebar.markdown(f'<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9S9S-h1hI1_D5gNq_gYn-kGjD8GjQkY5Qjg&s" class="sidebar-logo">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="status-badge">🟢 Banco de Dados Conectado</div>', unsafe_allow_html=True)

# 4. CONTEÚDO PRINCIPAL
# A. Dados de Controle (Conforme image_158023.png e image_158424.png)
st.markdown(f"""
    <div class="header-card">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9S9S-h1hI1_D5gNq_gYn-kGjD8GjQkY5Qjg&s" class="header-logo">
        <div style="flex-grow: 1;">
            <div class="header-title-label">DADOS DE CONTROLE</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; font-size: 12px;">
                <div><b>Data da Edição:</b> 29/01/2026</div>
                <div><b>Autor:</b> Matheus Chila</div>
                <div><b>Verificado:</b> Wagner Kazuki de Azambuja</div>
                <div><b>Revisão:</b> 6</div>
                <div><b>Setor:</b> Qualidade Industrial</div>
                <div><b>Inspeção:</b> <span style="color:red;">A cada 60 minutos</span></div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<h1 style="color:{AZUL_AGUIA}; text-align:center; font-size:28px;">INSPEÇÃO PERFILADEIRA NOVA LC</h1>', unsafe_allow_html=True)

# B. Passo a Passo (Instruções de Trabalho conforme image_158023.png)
st.markdown('<div class="section-header">INSTRUÇÕES DE TRABALHO (PASSO A PASSO)</div>', unsafe_allow_html=True)
st.markdown("""
    <table class="passos-table">
        <tr>
            <td class="passo-col-num">1º PASSO</td>
            <td>Perfil - marcar as medidas de A, B, C, D, E e F conforme a imagem. Comparar medida D com a diferença entre A e F.</td>
        </tr>
        <tr>
            <td class="passo-col-num">2º PASSO</td>
            <td>Medir o comprimento G do perfil.</td>
        </tr>
        <tr>
            <td class="passo-col-num">3º PASSO</td>
            <td>Para medir os empenamentos 1 e 2, encostar um perfil no outro conforme as imagens e medir o vão formado entre eles, a medida deve ser dividida por 2.</td>
        </tr>
        <tr>
            <td class="passo-col-num">4º PASSO</td>
            <td>Para medir o Gap, posicionar o gabarito conforme a imagem e efetuar medida com o paquímetro.</td>
        </tr>
    </table>
""", unsafe_allow_html=True)

# C. Formulário de Registro
with st.form(key="form_inspecao"):
    st.markdown('<div class="section-header">REGISTROS DE QUALIDADE</div>', unsafe_allow_html=True)
    
    # Linha 1: Identificação
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        data_insp = st.date_input("Data", datetime.date.today(), format="DD/MM/YYYY")
    with c2:
        hora_insp = st.text_input("Hora (HH:MM)", placeholder="Ex: 08:30")
    with c3:
        op = st.text_input("O.P.")
    with c4:
        inspetor = st.text_input("Inspetor")

    # Linha 2: Medidas A-G
    col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
    with col_a: med_a = st.number_input("A", format="%.2f", step=0.01)
    with col_b: med_b = st.number_input("B", format="%.2f", step=0.01)
    with col_c: med_c = st.number_input("C", format="%.2f", step=0.01)
    with col_d: med_d = st.number_input("D", format="%.2f", step=0.01)
    with col_e: med_e = st.number_input("E", format="%.2f", step=0.01)
    with col_f: med_f = st.number_input("F", format="%.2f", step=0.01)
    with col_g: med_g = st.number_input("G", format="%.2f", step=0.01)

    # Linha 3: Empenamento e Gap
    ce1, ce2, cg = st.columns(3)
    with ce1: emp1 = st.number_input("Empenamento 1", format="%.2f", step=0.01)
    with ce2: emp2 = st.number_input("Empenamento 2", format="%.2f", step=0.01)
    with cg: gap = st.number_input("Gap", format="%.2f", step=0.01)

    # Observações
    obs = st.text_area("Observações / Relatório de Anomalias", height=80)

    submit_button = st.form_submit_button(label="SALVAR REGISTRO NA PLANILHA")

# 5. LÓGICA DE ENVIO (MANTIDA)
if submit_button:
    if not re.match(r"^\d{2}:\d{2}$", hora_insp):
        st.error("Erro: Formato de hora inválido (HH:MM).")
    elif not op or not inspetor:
        st.warning("O.P. e Inspetor são obrigatórios.")
    else:
        URL_API = "https://script.google.com/macros/s/AKfycbwBwSPWVtbXBYzm5dMjsMVnmlLftZ6O0iyYYEYp43jOl3_vt3nQOKh4WFZYWPA5qhCl/exec"
        
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
            "obs": obs
        }

        try:
            with st.spinner('Gravando no sistema...'):
                response = requests.post(URL_API, data=json.dumps(payload))
            if response.status_code == 200:
                st.success("✅ Registro salvo com sucesso na planilha!")
                st.balloons()
            else:
                st.error(f"Erro no servidor: {response.status_code}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
