import streamlit as st
import google.generativeai as genai

# Configuração da página e Dark Mode nativo para evitar ecrãs brancos no telemóvel
st.set_page_config(page_title="Guia de Peças AI - Nikson Eletrónica", page_icon="⚡", layout="centered")

# --- INJEÇÃO DE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; color: #FFFFFF !important; }
    .stApp header { background-color: transparent !important; }
    div[data-baseweb="input"] > div { background-color: #2D2D2D !important; border: 2px solid #555 !important; border-radius: 10px !important; }
    div[data-baseweb="input"] > div > input { font-size: 26px !important; font-weight: bold; text-align: center; padding: 15px !important; color: #FFFFFF !important; }
    .instrucao { text-align: center; font-size: 28px; font-weight: bold; color: #FF4B4B; margin-top: 20px; margin-bottom: 20px; }
    .resposta-ia { 
        background-color: #1E1E1E; 
        padding: 30px; 
        border-radius: 12px; 
        border-left: 8px solid #4CAF50; 
        margin-top: 20px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.5); 
        font-size: 18px; 
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 0px;'>⚡ Nikson Eletrónica</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px; color: gray;'>Assistente IA de Bancada</p>", unsafe_allow_html=True)
st.write("---")

# --- CONFIGURAÇÃO DA API ---
try:
    # Tenta obter a chave guardada nos Secrets do Streamlit
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    modelo = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("⚠️ Erro crítico: A chave GEMINI_API_KEY não foi encontrada nos Secrets. Por favor, adicione a chave no painel do Streamlit.")
    st.stop()

st.markdown('<div class="instrucao">QUAL É O CÓDIGO DO COMPONENTE?</div>', unsafe_allow_html=True)

busca = st.text_input("", placeholder="Ex: p20nk50, 20n50k, s20531D...").strip()

if busca:
    with st.spinner("🧠 A analisar o componente e a procurar equivalentes..."):
        
        # O prompt detalhado que funciona sem precisar de ferramentas externas
        prompt = f"""
        És um engenheiro eletrónico sénior a ajudar um técnico de bancada muito experiente.
        O técnico tem em mãos um componente e leu a seguinte referência: "{busca}"
        
        Atenção: Na bancada é normal omitirem-se prefixos (ex: 20n50k significa FQA20N50 ou STP20NK50Z) ou confundirem-se letras devido ao desgaste.
        A tua missão é deduzir qual é o componente exato e fornecer as especificações reais de acordo com os datasheets da indústria.
        
        Responde ESTRITAMENTE neste formato Markdown:
        
        ### 📌 Componente Identificado: [Nome Correto e Completo]
        **Categoria:** [Ex: MOSFET N-Channel, Transistor BJT, etc.]
        **⚙️ Especificações Originais:** [Tensão, Corrente, Potência, etc.]
        
        ---
        ### 🔄 Equivalentes Recomendados
        * **[Componente 1]:** [Especificações e fiabilidade]
        * **[Componente 2]:** [Especificações e fiabilidade]
        
        ---
        ### 💡 Dicas de Bancada
        [Dicas para a reparação: o que costuma queimar junto com esta peça, avisos sobre isolamento ou falsificações no mercado.]
        """
        
        try:
            # Chamada direta e limpa, à prova de falhas
            resposta = modelo.generate_content(prompt)
            st.markdown(f'<div class="resposta-ia">{resposta.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Ocorreu um erro ao comunicar com a IA: {e}")

# Rodapé
st.markdown("<br><hr><p style='text-align: center; color: #666; font-size: 14px;'>Desenvolvido com ⚡ por Otto</p>", unsafe_allow_html=True)
