# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 20:11:36 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Base de datos simulada
DB_FILE = "control_documental.csv"

# Cargar base de datos
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=[
        "ID", "Proyecto", "Documento", "Código", "Responsable", "Versión", "Estado", "Fecha Registro"
    ])

st.title("📑 Sistema de Control Documental")
st.markdown("Gestión de documentos de un proyecto, con versiones y estados.")

# --- Agregar documento ---
st.subheader("➕ Registrar documento")
with st.form("form_doc"):
    proyecto = st.text_input("Proyecto")
    documento = st.text_input("Nombre del documento")
    codigo = st.text_input("Código interno")
    responsable = st.text_input("Responsable")
    estado = st.selectbox("Estado", ["Borrador", "En revisión", "Aprobado", "Obsoleto"])
    submitted = st.form_submit_button("Guardar")

    if submitted and proyecto and documento and codigo:
        # Calcular versión automática
        docs_existentes = df[(df["Proyecto"] == proyecto) & (df["Documento"] == documento)]
        version = 1 if docs_existentes.empty else docs_existentes["Versión"].max() + 1

        new_entry = {
            "ID": len(df) + 1,
            "Proyecto": proyecto,
            "Documento": documento,
            "Código": codigo,
            "Responsable": responsable,
            "Versión": version,
            "Estado": estado,
            "Fecha Registro": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        df = df._append(new_entry, ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success(f"✅ Documento '{documento}' guardado en versión v{version}")

# --- Búsqueda y visualización ---
st.subheader("🔍 Buscar documentos")
filtro = st.text_input("Buscar por proyecto, documento, código o responsable")

if filtro:
    resultados = df[df.apply(lambda row: filtro.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.write(resultados)
else:
    st.write(df)

# --- Estadísticas ---
st.subheader("📊 Estadísticas del control documental")
if not df.empty:
    docs_por_estado = df["Estado"].value_counts()
    st.bar_chart(docs_por_estado)
    docs_por_proyecto = df["Proyecto"].value_counts()
    st.bar_chart(docs_por_proyecto)
