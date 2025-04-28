#importar as bibliotecas
import streamlit as st
import fitz
from groq import Groq
import os   

# Caminho dinâmico da imagem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(CURRENT_DIR, "logo.png")


# Configurar chave da Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# função para extrair os arquivos     
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Você é um assistente de IA que auxilia a diagnosticar doenças e condições médicas com base em informações de saúde e sintomas fornecidas pelo usuario."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}     ]
    )
    return response.choices[0].message.content


# CRIAR A INTERFACE
def main():
    st.title("House I.A.")
  #  st.image("logo.png", width=800, caption="House I.A.")
    # Incluir uma imagem de acordo ao sistema escolhido
    with st.sidebar:
        st.header("UPLoader Files")
        uploader = st.file_uploader("Adicione arquivos", type="pdf", accept_multiple_files=True)
    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
    user_input = st.text_input("Digite a sua pergunta")
    
    if user_input and "document-text" in st.session_state:
            response = chat_with_groq(user_input, st.session_state["document-text"])
            st.write("Resposta", response)

if __name__ == "__main__":
    main()
    