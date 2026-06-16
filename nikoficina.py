import streamlit as st
import google.generativeai as genai

# Configuração da página e Dark Mode nativo
st.set_page_config(page_title="Guia de Peças AI - Nikson Eletrônica", page_icon="⚡", layout="centered")

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

st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 0px;'>⚡ Nikson Eletrônica</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px; color: gray;'>Assistente IA de Bancada</p>", unsafe_allow_html=True)
st.write("---")

# --- CONFIGURAÇÃO DA API ---
try:
    CHAVE_API = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=CHAVE_API)
    modelo = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error("⚠️ Erro de configuração: Chave da API não encontrada nos Secrets do Streamlit.")
    st.stop()

st.markdown('<div class="instrucao">QUAL CÓDIGO ESTÁ NO COMPONENTE?</div>', unsafe_allow_html=True)

busca = st.text_input("", placeholder="Ex: p20nk50, s20531D, irf3205...").strip()

if busca:
    with st.spinner("🌐 Consultando datasheets na internet e analisando peça..."):
        
        # Prompt ajustado para forçar a busca de informações reais e precisas
        prompt = f"""
        Você é um assistente de bancada eletrônica com acesso à internet. 
        O técnico digitou o seguinte código que leu em um componente: "{busca}"
        
        Sua tarefa:
        1. Identifique o componente real. Lembre-se que técnicos omitem prefixos (ex: p20nk50 = STP20NK50Z) ou confundem números e letras devido ao desgaste da peça (ex: S20531D = IRS2053D).
        2. Busque as especificações técnicas (datasheet) reais e atualizadas desse componente.
        3. Encontre substitutos/equivalentes que sejam fáceis de achar no mercado.
        
        Responda ESTRITAMENTE neste formato Markdown:
        
        ### 📌 Componente Identificado: [Nome Correto e Completo]
        **Categoria:** [Ex: MOSFET N-Channel, Transistor BJT NPN, CI Driver, etc]
        **⚙️ Especificações Originais:** [Tensão, Corrente, Potência, Hfe, etc]
        
        ---
        ### 🔄 Equivalentes Recomendados
        * **[Componente Equivalente 1]:** [Especificações e se suporta o tranco igual o original]
        * **[Componente Equivalente 2]:** [Especificações e se suporta o tranco igual o original]
        * *(Liste até 4 equivalentes robustos e comuns)*
        
        ---
        ### 💡 Dicas de Bancada
        [Dicas diretas de conserto: macetes, o que verificar antes de soldar a peça nova para ela não queimar de novo, isolamento, falsificações comuns, etc.]
        """
        
        try:
            # O parâmetro tools='google_search_retrieval' força a IA a usar a busca do Google para embasar a resposta
            resposta = modelo.generate_content(prompt, tools='google_search_retrieval')
            st.markdown(f'<div class="resposta-ia">{resposta.text}</div>', unsafe_allow_html=True)
        except Exception as e:
            # Fallback caso a versão da biblioteca não suporte o parâmetro tools ou a busca falhe
            try:
                resposta_fallback = modelo.generate_content(prompt)
                st.markdown(f'<div class="resposta-ia">{resposta_fallback.text}</div>', unsafe_allow_html=True)
            except Exception as e_fallback:
                st.error(f"Houve um problema de comunicação com a IA: {e_fallback}")

# Assinatura
st.markdown("<br><hr><p style='text-align: center; color: #666; font-size: 14px;'>Desenvolvido com ⚡ por Otto</p>", unsafe_allow_html=True)
