import streamlit as st
import fitz
from groq import Groq

# === CONFIG ===
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# === FUNÇÕES UTILITÁRIAS ===

def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

def chat_with_groq(prompt, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos."},
            {"role": "user", "content": f"{context}\n\nPergunta: {prompt}"}
        ]
    )
    return response.choices[0].message.content    

def gerar_cronograma(materias, tempo_total):
    total_peso = sum(materias.values())
    cronograma = {}
    for materia, dificuldade in materias.items():
        tempo_materia = (dificuldade * tempo_total) // total_peso
        cronograma[materia] = tempo_materia
    return cronograma

# === INTERFACE ===

def main():
    st.title("📚 Organizador Inteligente de Estudos")

    with st.sidebar:
        st.header("📎 Envie seus materiais")
        uploader = st.file_uploader("Adicione arquivos PDF", type="pdf", accept_multiple_files=True)
        if uploader:
            text = extract_files(uploader)
            st.session_state["document-text"] = text

    st.subheader("🧠 Sistema de Organização de Estudos")

    with st.expander("1️⃣ Cadastro de Matérias e Dificuldade"):
        materias = {}
        num_materias = st.number_input("Quantas matérias deseja cadastrar?", min_value=1, max_value=20, value=3)
        for i in range(num_materias):
            nome = st.text_input(f"Matéria {i+1}", key=f"mat{i}")
            dificuldade = st.slider(f"Dificuldade de {nome}", 1, 5, 3, key=f"dif{i}")
            if nome:
                materias[nome] = dificuldade

    with st.expander("2️⃣ Tempo disponível por dia"):
        tempo_disponivel = st.slider("Minutos disponíveis por dia", 30, 600, 120)

    if materias and tempo_disponivel:
        st.subheader("📅 Cronograma Gerado")
        cronograma = gerar_cronograma(materias, tempo_disponivel)
        for mat, tempo in cronograma.items():
            st.write(f"- {mat}: {tempo} minutos por dia")

        st.subheader("🔔 Lembretes Inteligentes")
        for mat in materias:
            st.success(f"Lembrete: Estude **{mat}** hoje!")

    if "document-text" in st.session_state:
        st.subheader("💬 Tire dúvidas com seus PDFs")
        pergunta = st.text_input("Digite sua pergunta:")
        if pergunta:
            resposta = chat_with_groq(pergunta, st.session_state["document-text"])
            st.write("**Resposta:**", resposta)


if __name__ == "__main__":
    main()
