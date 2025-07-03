
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
import plotly.express as px
import re
import time

st.set_page_config(page_title="Analisador Virtual - Big Tech RHday", layout="wide")

menu = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "🏷️ Upload Currículos", "🚀 Analisador Excellence Big Tech", "📅 RHday"]
)

if "arquivos" not in st.session_state:
    st.session_state["arquivos"] = []

if menu == "🏠 Home":
    st.title("Fala, Micheline, tudo bem?")
    placeholder = st.empty()
    texto = "Sou seu Analista Virtual"
    displayed = ""
    for letra in texto:
        displayed += letra
        placeholder.write(f"_{displayed}_")
        time.sleep(0.1)

elif menu == "🏷️ Upload Currículos":
    st.title("📤 Upload de Currículos")
    st.markdown("Envie **PDF, DOCX ou TXT**. Use nomes de arquivo claros para facilitar a análise.")

    arquivos = st.file_uploader(
        "Selecione ou solte os arquivos aqui:",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if arquivos:
        st.session_state["arquivos"] = arquivos
        st.success(f"✅ {len(arquivos)} arquivo(s) carregado(s) com sucesso!")

elif menu == "🚀 Analisador Excellence Big Tech":
    st.title("🚀 Analisador Virtual — Excellence Big Tech")

    arquivos = st.session_state.get("arquivos", [])
    if not arquivos:
        st.warning("⚠️ Nenhum arquivo carregado. Use o Upload Currículos primeiro.")
    else:
        data = []
        estados = {
            "PE": (-8.28, -35.07), "SP": (-23.55, -46.63), "RJ": (-22.90, -43.20),
            "BA": (-12.97, -38.50), "MG": (-19.92, -43.94), "PR": (-25.43, -49.27),
            "MA": (-2.55, -44.30)
        }
        keywords_uf = {
            "Recife": "PE", "Pernambuco": "PE", "São Paulo": "SP", "Bahia": "BA",
            "Minas": "MG", "Rio de Janeiro": "RJ", "Curitiba": "PR",
            "Maranhão": "MA", "São Luís": "MA"
        }

        for arquivo in arquivos:
            texto = ""
            if arquivo.type == "application/pdf":
                reader = PdfReader(arquivo)
                for page in reader.pages:
                    texto += page.extract_text() + "\n"
            elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = Document(arquivo)
                for para in doc.paragraphs:
                    texto += para.text + "\n"
            elif arquivo.type == "text/plain":
                texto = arquivo.read().decode("utf-8")

            uf_detectada = "Indefinido"
            for keyword, code in keywords_uf.items():
                if keyword.lower() in texto.lower():
                    uf_detectada = code
                    break

            certs_detectadas = []
            cert_keywords = ["PMP", "Scrum", "AWS", "Oracle", "Machine Learning"]
            for cert in cert_keywords:
                if cert.lower() in texto.lower():
                    certs_detectadas.append(cert)

            skills_detectadas = []
            skills_keywords = ["Python", "SQL", "Excel", "Power BI", "Tableau", "Machine Learning",
                               "Logística", "Análise de Dados", "Projetos", "Planejamento", "ETL"]
            for skill in skills_keywords:
                if skill.lower() in texto.lower():
                    skills_detectadas.append(skill)

            combos = []
            if "python" in texto.lower() and "pandas" in texto.lower():
                combos.append("Python + Pandas")
            if "sql" in texto.lower() and "etl" in texto.lower():
                combos.append("SQL + ETL")
            if combos:
                skills_detectadas.extend(combos)

            linhas = texto.strip().split("\n")
            nome = linhas[0].strip() if linhas else "Talento Excellence"

            exp = ""
            match = re.search(r"(\d+) anos", texto.lower())
            if match:
                exp = match.group(1)

            pontuacao = 0
            if exp and int(exp) >= 5:
                pontuacao += 10
            if certs_detectadas:
                pontuacao += 10
            if skills_detectadas:
                pontuacao += 10

            if pontuacao >= 20:
                status_auto = "Pronto para Entrevista"
            elif pontuacao >= 10:
                status_auto = "Revisar Dados"
            else:
                status_auto = "Precisa Revisão"

            headline = f"{nome} — Foco em {', '.join(skills_detectadas[:3]) if skills_detectadas else 'Área Técnica'}"

            resumo_tecnico = f"""
📌 **Headline:** {headline}

🌎 **UF:** {uf_detectada} | 📅 **Experiência:** {exp}+ anos | 🏆 **Pontuação:** {pontuacao}/30

🎓 **Certificações:** {', '.join(certs_detectadas) if certs_detectadas else 'Nenhuma'}

🛠️ **Principais Skills:** {', '.join(skills_detectadas) if skills_detectadas else 'Não detectadas'}

✅ **Status:** {status_auto}
"""

            data.append({
                "Nome": arquivo.name,
                "UF": uf_detectada,
                "Pontuação": pontuacao,
                "Status": status_auto,
                "Análise": texto[:500] + "...",
                "ResumoTec": resumo_tecnico
            })

        df = pd.DataFrame(data)

        st.markdown("## 📋 Resultados da Análise")
        for idx, row in df.iterrows():
            with st.expander(f"📄 {row['Nome']}"):
                st.markdown(row['ResumoTec'], unsafe_allow_html=True)
                st.write(row['Análise'])

elif menu == "📅 RHday":
    st.title("📅 RHday — Agenda da Recrutadora")

    data = st.date_input("📅 Data")
    hora = st.time_input("⏰ Horário")
    nota = st.text_area("📝 Anotação da reunião/entrevista:")

    if st.button("💾 Salvar Evento"):
        if "agenda" not in st.session_state:
            st.session_state["agenda"] = []
        st.session_state["agenda"].append({
            "data": str(data),
            "hora": str(hora),
            "nota": nota
        })
        st.success(f"Evento salvo para {data} às {hora}.")

    if "agenda" in st.session_state and st.session_state["agenda"]:
        st.markdown("### 📌 Eventos Agendados:")
        for item in st.session_state["agenda"]:
            st.info(f"📅 {item['data']} ⏰ {item['hora']} — {item['nota']}")
