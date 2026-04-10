import streamlit as st
import urllib.parse
import urllib.request
import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Inspeção Perfiladeira", layout="wide")

# 2. Estilização CSS
st.markdown("""
    <style>
    .secao-header {
        background-color: #f0f2f6;
        border-left: 5px solid #283b5e;
        padding: 10px 15px;
        margin-top: 25px;
        margin-bottom: 15px;
        font-weight: bold;
        color: #333;
        text-transform: uppercase;
        font-size: 14px;
    }
    .titulo-principal {
        text-align: center;
        color: #283b5e;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .bd-conectado {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        margin-top: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #283b5e;'>ÁGUIA<br><small>S I S T E M A S</small></h2>", unsafe_allow_html=True)
    st.caption("Sistema Integrado")
    st.markdown("<div class='bd-conectado'>BD Conectado</div>", unsafe_allow_html=True)

# 4. Cabeçalho Principal
st.markdown("<h2 class='titulo-principal'>INSPEÇÃO PERFILADEIRA NOVA LC</h2>", unsafe_allow_html=True)

# --- DADOS DE CONTROLE REAIS ---
col_autor, col_verif, col_freq = st.columns(3)
with col_autor:
    st.text_input("Autor(a) / Data Edição", value="Matheus Chila | 29/01/2026", disabled=True)
with col_verif:
    st.text_input("Verificado por", value="Wagner Kazuki de Azambuja", disabled=True)
with col_freq:
    st.text_input("Frequência de Inspeção", value="A cada 60 minutos", disabled=True)

# --- INSTRUÇÕES DA TAREFA ---
with st.expander("📖 VER INSTRUÇÕES DE MEDIÇÃO (Passo a Passo)"):
    st.markdown("""
    * **1° PASSO:** Perfil - marcar as medidas de A, B, C, D, E e F conforme a imagem. Comparar medida D com a diferença entre A e F.
    * **2° PASSO:** Medir o comprimento G do perfil.
    * **3° PASSO:** Para medir os empenamentos 1 e 2, encostar um perfil no outro conforme as imagens e medir o vão formado entre eles, a medida deve ser dividida por 2.
    * **4° PASSO:** Para medir o Gap, posicionar o gabarito conforme a imagem e efetuar medida com o paquímetro.
    """)

# ================= INÍCIO DO FORMULÁRIO =================
with st.form(key="form_inspecao"):

    # --- INFORMAÇÕES GERAIS ---
    st.markdown("<div class='secao-header'>Informações Gerais</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_insp = st.date_input("Data", datetime.date.today())
    with col2:
        hora_insp = st.time_input("Hora", datetime.datetime.now().time())
    with col3:
        op = st.text_input("O.P.")
    with col4:
        inspetor = st.text_input("Inspetor")

    # --- MEDIDAS (A até G) ---
    st.markdown("<div class='secao-header'>Registros de Qualidade - Medidas</div>", unsafe_allow_html=True)
    col_a, col_b, col_c, col_d, col_e, col_f, col_g = st.columns(7)
    with col_a:
        med_a = st.number_input("A", format="%.2f", step=0.01)
    with col_b:
        med_b = st.number_input("B", format="%.2f", step=0.01)
    with col_c:
        med_c = st.number_input("C", format="%.2f", step=0.01)
    with col_d:
        med_d = st.number_input("D", format="%.2f", step=0.01)
    with col_e:
        med_e = st.number_input("E", format="%.2f", step=0.01)
    with col_f:
        med_f = st.number_input("F", format="%.2f", step=0.01)
    with col_g:
        med_g = st.number_input("G", format="%.2f", step=0.01)

    # --- EMPENAMENTO E GAP ---
    st.markdown("<div class='secao-header'>Empenamento e Gap</div>", unsafe_allow_html=True)
    col_emp1, col_emp2, col_gap = st.columns(3)
    with col_emp1:
        emp1 = st.number_input("Emp. 1", format="%.2f", step=0.01)
    with col_emp2:
        emp2 = st.number_input("Emp. 2", format="%.2f", step=0.01)
    with col_gap:
        gap = st.number_input("Gap", format="%.2f", step=0.01)

    # --- OBSERVAÇÕES ---
    st.markdown("<div class='secao-header'>Observações</div>", unsafe_allow_html=True)
    observacoes = st.text_area("Anotações adicionais:", height=100)

    # --- BOTÃO DE ENVIO ---
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="Salvar Inspeção 🚀")

# ================= LÓGICA DE ENVIO =================
if submit_button:
    if not op or not inspetor:
        st.warning("Por favor, preencha a O.P. e o nome do Inspetor.")
    else:
        try:
            # URL de resposta extraída do seu link
            URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf2uGDngL6tPY474Zat9cDIpLawV5s7uyHZXoDFhA3hlieEPA/formResponse"
            
            # Mapeamento com as chaves exatas do seu Forms
            dados = {
                "entry.304430330": data_insp.strftime("%d/%m/%Y"), 
                "entry.280988980": hora_insp.strftime("%H:%M"),    
                "entry.385276294": op,
                "entry.15366618": inspetor,
                "entry.283351221": med_a,
                "entry.1884866072": med_b,
                "entry.157460815": med_c,
                "entry.169179972": med_d,
                "entry.949147072": med_e,
                "entry.792819612": med_f,
                "entry.920257028": med_g,
                "entry.879358480": emp1,
                "entry.3262184": emp2,
                "entry.506258603": gap,
                "entry.1610873220": observacoes
            }

            data = urllib.parse.urlencode(dados).encode("utf-8")
            req = urllib.request.Request(URL_FORM, data=data)
            urllib.request.urlopen(req)
            
            st.success("Inspeção salva com sucesso na Base de Dados! ✅")
            st.balloons()

        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
