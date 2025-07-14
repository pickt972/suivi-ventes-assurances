import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Suivi Ventes Assurances", layout="wide")

st.title("📋 Suivi des ventes d’assurances complémentaires")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Employé", "Nom du client", "N° réservation", "Type d’assurance"])

st.header("📝 Saisir une vente")

col1, col2, col3 = st.columns(3)

with col1:
    employe = st.selectbox("Employé", ["Julie", "Sherman", "Alvin"])

with col2:
    client = st.text_input("Nom du client")

with col3:
    reservation = st.text_input("N° réservation")

assurances = st.multiselect("Type d’assurance vendue", ["Pneumatique", "Bris de glace", "Conducteur supplémentaire"])

if st.button("Enregistrer"):
    for assurance in assurances:
        st.session_state.data = pd.concat([
            st.session_state.data,
            pd.DataFrame.from_records([{
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Employé": employe,
                "Nom du client": client,
                "N° réservation": reservation,
                "Type d’assurance": assurance
            }])
        ], ignore_index=True)
    st.success("Vente(s) enregistrée(s) avec succès ✅")

st.header("📄 Ventes enregistrées")
st.dataframe(st.session_state.data, use_container_width=True)

st.header("📊 Résumé mensuel")
if not st.session_state.data.empty:
    pivot = pd.pivot_table(
        st.session_state.data,
        index="Employé",
        columns="Type d’assurance",
        aggfunc="size",
        fill_value=0
    )
    pivot["Total"] = pivot.sum(axis=1)
    st.table(pivot)

st.header("📥 Exporter les données")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Télécharger en CSV",
        data=csv,
        file_name='ventes_assurances.csv',
        mime='text/csv'
    )

with col_exp2:
    with pd.ExcelWriter("ventes_assurances.xlsx", engine='xlsxwriter') as excel_buffer:
        st.session_state.data.to_excel(excel_buffer, index=False)

    with open("ventes_assurances.xlsx", "rb") as f:
        st.download_button(
            label="Télécharger en Excel",
            data=f,
            file_name="ventes_assurances.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("---")
st.caption("Application réalisée avec ❤️ par votre assistant IA")