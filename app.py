import streamlit as st
import urllib.parse
import urllib.request
import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Inspeção Perfiladeira - Águia Sistemas", layout="wide")

# 2. Estilização CSS para ajustar o visual
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
    .bd-conectado {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #283b5e;'>ÁGUIA<br><small>S I S T E M A S</small></h2>", unsafe_allow_html=True)
    st.markdown("<div class='bd-conectado'>BD Conectado</div>", unsafe_allow_html=True)
    st.info("Utilize este formulário para registrar as inspeções de hora em hora.")

# 4. CABEÇALHO FIXO ESTRUTURADO (Fiel à imagem de controle da Águia Sistemas)
st.markdown("""
    <table style="width:100%; border-collapse: collapse; border: 2px solid black; font-family: sans-serif;">
        <tr>
            <td rowspan="3" style="width: 20%; border: 2px solid black; text-align: center; padding: 10px;">
                <h2 style="margin:0; color:#283b5e;">ÁGUIA</h2>
                <small>S I S T E M A S</small>
            </td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Data da Edição:</b> 29/01/2026
            </td>
            <td style="width: 40%; border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Autor(a):</b> Matheus Chila
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Revisão:</b> 6
            </td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Verificado:</b> Wagner Kazuki de Azambuja
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Setor:</b> Qualidade Industrial
            </td>
            <td style="border: 1px solid black; padding: 5px; font-size: 13px;">
                <b>Inspeção:</b> a cada 60 minutos
            </td>
        </tr>
    </table>
    <div style="background-color: red; color: white; text-align: center; padding: 12px; font-weight: bold; font-size: 22px; border: 2px solid black; border-top: none;">
        INSPEÇÃO PERFILADEIRA NOVA LC
    </div>
    <br>
""", unsafe_allow_html=True)

# 5. INSTRUÇÕES DA TAREFA (Passo a Passo extraído do seu texto)
with st.expander("📖 CLIQUE PARA VER AS INSTRUÇÕES DE MEDIÇÃO"):
    st.markdown("""
    * **1° PASSO:** Perfil - marcar as medidas de A, B, C, D, E e F conforme a imagem. Comparar medida D com a diferença entre A e F.
    * **2° PASSO:** Medir o comprimento G do perfil.
    * **3° PASSO:** Para medir os empenamentos 1 e 2, encostar um perfil no outro e medir o vão formado entre eles, a medida deve ser dividida por 2.
    * **4° PASSO:** Para medir o Gap, posicionar o gabarito conforme a imagem e efetuar medida com o paquímetro.
    """)

# ================= INÍCIO DO FORMULÁRIO DE REGISTRO =================
with st.form(key="form_inspecao"):

    st.markdown("<div class='secao-header'>Registros de Qualidade - Identificação</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        data_insp = st.date_input("Data", datetime.date.today())
    with col2:
        hora_insp = st.time_input("Hora", datetime.datetime.now().time())
    with col3:
        op = st.text_input("O.P.")
    with col4:
        inspetor = st.text_input("Inspetor")

    st.markdown("<div class='secao-header'>Medidas do Perfil (A até G)</div>", unsafe_allow_html=True)
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

    st.markdown("<div class='secao-header'>Verificações de Empenamento e Gap</div>", unsafe_allow_html=True)
    col_emp1, col_emp2, col_gap = st.columns(3)
    with col_emp1:
        emp1 = st.number_input("Emp. 1", format="%.2f", step=0.01)
    with col_emp2:
        emp2 = st.number_input("Emp. 2", format="%.2f", step=0.01)
    with col_gap:
        gap = st.number_input("Gap", format="%.2f", step=0.01)

    st.markdown("<div class='secao-header'>Observações Adicionais</div>", unsafe_allow_html=True)
    observacoes = st.text_area("Descreva qualquer anomalia aqui:", height=80)

    # BOTÃO DE SUBMISSÃO
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="SALVAR REGISTRO DE INSPEÇÃO ✅")

# ================= LÓGICA DE ENVIO PARA O GOOGLE FORMS =================
if submit_button:
    if not op or not inspetor:
        st.error("ERRO: Os campos O.P. e Inspetor são obrigatórios!")
    else:
        try:
            # URL de destino do seu formulário
            URL_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf2uGDngL6tPY474Zat9cDIpLawV5s7uyHZXoDFhA3hlieEPA/formResponse"
            
            # Dados mapeados conforme o link que você gerou
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

            # Executa o envio via POST silencioso
            data_encoded = urllib.parse.urlencode(dados).encode("utf-8")
            req = urllib.request.Request(URL_FORM, data=data_encoded)
            urllib.request.urlopen(req)
            
            st.success("Dados enviados com sucesso para a planilha! ✅")
            st.balloons()

        except Exception as e:
            st.error(f"Erro técnico ao enviar dados: {e}")
