{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
from datetime import datetime\
\
st.set_page_config(page_title="Suivi Ventes Assurances", layout="wide")\
\
st.title("\uc0\u55357 \u56523  Suivi des ventes d\'92assurances compl\'e9mentaires")\
\
# Initialisation de la session\
if "data" not in st.session_state:\
    st.session_state.data = pd.DataFrame(columns=["Date", "Employ\'e9", "Nom du client", "N\'b0 r\'e9servation", "Type d\'92assurance"])\
\
# Formulaire de saisie\
st.header("\uc0\u55357 \u56541  Saisir une vente")\
\
col1, col2, col3 = st.columns(3)\
\
with col1:\
    employe = st.selectbox("Employ\'e9", ["Julie", "Sherman", "Alvin"])\
\
with col2:\
    client = st.text_input("Nom du client")\
\
with col3:\
    reservation = st.text_input("N\'b0 r\'e9servation")\
\
assurances = st.multiselect("Type d\'92assurance vendue", ["Pneumatique", "Bris de glace", "Conducteur suppl\'e9mentaire"])\
\
if st.button("Enregistrer"):\
    for assurance in assurances:\
        st.session_state.data = pd.concat([\
            st.session_state.data,\
            pd.DataFrame.from_records([\{\
                "Date": datetime.now().strftime("%Y-%m-%d"),\
                "Employ\'e9": employe,\
                "Nom du client": client,\
                "N\'b0 r\'e9servation": reservation,\
                "Type d\'92assurance": assurance\
            \}])\
        ], ignore_index=True)\
    st.success("Vente(s) enregistr\'e9e(s) avec succ\'e8s \uc0\u9989 ")\
\
# Afficher les ventes\
st.header("\uc0\u55357 \u56516  Ventes enregistr\'e9es")\
st.dataframe(st.session_state.data, use_container_width=True)\
\
# R\'e9sum\'e9 mensuel\
st.header("\uc0\u55357 \u56522  R\'e9sum\'e9 mensuel")\
if not st.session_state.data.empty:\
    pivot = pd.pivot_table(\
        st.session_state.data,\
        index="Employ\'e9",\
        columns="Type d\'92assurance",\
        aggfunc="size",\
        fill_value=0\
    )\
    pivot["Total"] = pivot.sum(axis=1)\
    st.table(pivot)\
\
# Exporter\
st.header("\uc0\u55357 \u56549  Exporter les donn\'e9es")\
\
col_exp1, col_exp2 = st.columns(2)\
\
with col_exp1:\
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')\
    st.download_button(\
        label="T\'e9l\'e9charger en CSV",\
        data=csv,\
        file_name='ventes_assurances.csv',\
        mime='text/csv'\
    )\
\
with col_exp2:\
    excel_buffer = pd.ExcelWriter("ventes_assurances.xlsx", engine='xlsxwriter')\
    st.session_state.data.to_excel(excel_buffer, index=False)\
    excel_buffer.save()\
    with open("ventes_assurances.xlsx", "rb") as f:\
        st.download_button(\
            label="T\'e9l\'e9charger en Excel",\
            data=f,\
            file_name="ventes_assurances.xlsx",\
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"\
        )\
\
st.markdown("---")\
st.caption("Application r\'e9alis\'e9e avec \uc0\u10084 \u65039  par votre assistant IA")}