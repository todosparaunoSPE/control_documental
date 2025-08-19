# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 20:11:36 2025

@author: jahop
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Base de datos simulada en CSV
DB_FILE = "documentos.csv"

# Cargar la base de datos
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["ID", "Nombre", "Responsable", "Fecha", "Proyecto", "Version", "Archivo"])

# --- Información institucional ---
autor = "Javier Horacio Pérez Ricárdez"
empresa = "PRESTADORA DE SERVICIOS CORPORATIVOS GENERALES (PRESCO)"
fecha_hoy = datetime.now().strftime("%d/%m/%Y")

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/File_document_icon.png", width=100)
st.sidebar.markdown(f"👤 **Desarrollado por:** {autor}")
st.sidebar.markdown(f"🏢 **Empresa:** {empresa}")
st.sidebar.markdown(f"📅 **Fecha:** {fecha_hoy}")

# --- Autenticación simple ---
st.sidebar.title("🔑 Acceso al sistema")
rol = st.sidebar.selectbox("Selecciona tu rol", ["Consulta", "Administrador"])

# --- Título principal ---
st.title("📂 Sistema de Control Documental")
st.markdown(f"Prototipo corporativo desarrollado para **{empresa}**")

# --- Función para asignar versión ---
def obtener_version(nombre, proyecto):
    docs = df[(df["Nombre"] == nombre) & (df["Proyecto"] == proyecto)]
    if docs.empty:
        return 1
    else:
        return docs["Version"].max() + 1

# --- Subida de documentos (solo Admin) ---
if rol == "Administrador":
    st.subheader("➕ Cargar un nuevo documento")
    with st.form("upload_form"):
        nombre = st.text_input("Nombre del documento")
        responsable = st.text_input("Responsable")
        proyecto = st.text_input("Proyecto/Área")
        archivo = st.file_uploader("Seleccionar archivo", type=["pdf", "docx", "xlsx"])
        submitted = st.form_submit_button("Guardar documento")

        if submitted and nombre and responsable and proyecto and archivo:
            version = obtener_version(nombre, proyecto)

            # Crear carpeta docs
            os.makedirs("docs", exist_ok=True)
            file_name = f"{nombre}_v{version}_{archivo.name}"
            file_path = os.path.join("docs", file_name)

            with open(file_path, "wb") as f:
                f.write(archivo.read())

            new_entry = {
                "ID": len(df) + 1,
                "Nombre": nombre,
                "Responsable": responsable,
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Proyecto": proyecto,
                "Version": version,
                "Archivo": file_path,
            }
            df = df._append(new_entry, ignore_index=True)
            df.to_csv(DB_FILE, index=False)
            st.success(f"✅ Documento guardado como versión v{version}.")

# --- Búsqueda de documentos ---
st.subheader("🔍 Buscar documentos")
busqueda = st.text_input("Ingrese palabra clave (nombre, responsable o proyecto)")

if busqueda:
    resultados = df[df.apply(lambda row: busqueda.lower() in row.astype(str).str.lower().to_string(), axis=1)]
    st.write(resultados[["ID", "Nombre", "Proyecto", "Version", "Responsable", "Fecha"]])
else:
    st.write(df[["ID", "Nombre", "Proyecto", "Version", "Responsable", "Fecha"]])

# --- Descarga de documentos ---
st.subheader("⬇️ Descargar documentos")
for idx, row in df.iterrows():
    with open(row["Archivo"], "rb") as file:
        st.download_button(
            label=f"📥 {row['Nombre']} v{row['Version']} ({row['Proyecto']})",
            data=file,
            file_name=os.path.basename(row["Archivo"])
        )
