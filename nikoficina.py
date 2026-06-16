import streamlit as st
import pandas as pd
import requests
import io
import urllib3

# Esconde o aviso de "conexão não verificada" no terminal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração da página
st.set_page_config(page_title="Guia de Peças - Nikson Eletrônica", page_icon="⚡", layout="centered")

# --- INJEÇÃO DE CSS (MOTION DESIGN E ESTÉTICA) ---
st.markdown("""
    <style>
    /* Destaque da Barra de Pesquisa */
    div[data-baseweb="input"] > div {
        background-color: #2D2D2D !important;
        border: 2px solid #555 !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"] > div > input {
        font-size: 26px !important;
        font-weight: bold;
        text-align: center;
        padding: 15px !important;
        color: #FFFFFF !important;
    }
    
    /* Motion Design: Animação pulsante */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .instrucao {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #FF4B4B;
        margin-top: 20px;
    }
    
    .bouncing-arrow {
        text-align: center;
        font-size: 45px;
        animation: pulse 1.5s infinite;
        margin-bottom: -15px;
    }
    
    /* Estilização dos Cartões */
    .card-componente {
        background-color: #1E1E1E; 
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #FF4B4B;
        margin-bottom: 20px;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.5);
    }
    
    .titulo-peca {
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;
        margin: 0;
        padding-bottom: 10px;
        border-bottom: 1px solid #333;
        margin-bottom: 15px;
    }
    
    .texto-grande {
        font-size: 24px;
        color: #DDDDDD;
        line-height: 1.8;
    }
    
    .especificacoes {
        font-size: 20px;
        color: #A0AEC0;
        margin-top: 10px;
        font-family: monospace;
        background: #1A202C;
        padding: 12px;
        border-radius: 6px;
        border-left: 4px solid #F6E05E;
    }
    
    .equivalentes {
        font-size: 30px;
        color: #00E676; 
        font-weight: bold;
        display: block;
        background-color: #111;
        padding: 20px; /* Padding maior para respiro */
        border-radius: 8px;
        margin-top: 10px;
        line-height: 1.4;
    }
    
    .dica {
        background-color: #2D3748;
        padding: 20px;
        border-radius: 8px;
        font-size: 22px;
        color: #E2E8F0;
        margin-top: 20px;
        border-left: 5px solid #4299E1;
    }
    </style>
""", unsafe_allow_html=True)

URL_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSqOEepf0xDIwyoEHws00rjvDcjbOWe40rFoymzA-2XvUk-nW3eFv7h7guWtbCOvGIHCUNBp2KtJEfG/pub?gid=725739881&single=true&output=csv"

@st.cache_data(ttl=60)
def carregar_dados(url):
    try:
        resposta = requests.get(url, verify=False)
        resposta.raise_for_status() 
        resposta.encoding = 'utf-8'
        df = pd.read_csv(io.StringIO(resposta.text))
        df = df.astype(str).fillna("")
        return df
    except Exception as e:
        st.error(f"Erro ao ler a planilha: {e}")
        return pd.DataFrame()

df = carregar_dados(URL_GOOGLE_SHEETS)

# Cabeçalho
st.markdown("<h1 style='text-align: center; font-size: 50px; margin-bottom: 0px;'>⚡ Nikson Eletrônica</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px; color: gray;'>Áudio Profissional</p>", unsafe_allow_html=True)
st.write("---")

if not df.empty:
    st.markdown('<div class="instrucao">O QUE VOCÊ ESTÁ PROCURANDO HOJE?</div>', unsafe_allow_html=True)
    st.markdown('<div class="bouncing-arrow">👇</div>', unsafe_allow_html=True)
    
    busca = st.text_input("", placeholder="Ex: IRFB4227, 2SC5200...").strip().upper()
    
    st.write("---")
    
    if busca:
        resultado = df[df['Componente'].str.contains(busca, case=False, na=False) | 
                       df['Equivalentes'].str.contains(busca, case=False, na=False)]
        
        if not resultado.empty:
            st.markdown(f"<h3 style='font-size: 26px; color: #4CAF50;'>✅ Encontrado: {len(resultado)} opção(ões) para <b>'{busca}'</b></h3>", unsafe_allow_html=True)
            
            for index, row in resultado.iterrows():
                especs_texto = row['Especificacoes'] if 'Especificacoes' in df.columns else "Sem informações."
                
                card_html = f"""<div class="card-componente">
<div class="titulo-peca">📌 {row['Componente']}</div>
<div class="texto-grande"><b>Categoria:</b> {row['Tipo']}</div>
<div class="especificacoes"><b>⚙️ Especificações:</b> {especs_texto}</div>
<div class="texto-grande" style="margin-top: 15px;"><b>Equivalentes:</b> 
<span class="equivalentes">{row['Equivalentes']}</span>
</div>
<div class="dica"><b>💡 Dica de Bancada:</b><br>{row['Observacoes']}</div>
</div>"""
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='font-size: 26px; color: #FF4B4B;'>⚠️ A peça '{busca}' não está na lista.</h3>", unsafe_allow_html=True)
else:
    st.warning("A aguardar ligação...")

# Assinatura no rodapé
st.markdown("<br><hr><p style='text-align: center; color: #666; font-size: 14px;'>Desenvolvido com ⚡ por Otto</p>", unsafe_allow_html=True)
