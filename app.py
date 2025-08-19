# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 20:11:36 2025

@author: jahop
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# --- Datos de ejemplo (20 registros) ---
data = [
    [1, "Proyecto Alfa", "Manual de Operación", "DOC-001", "Carlos López", 1, "Aprobado", "2024-08-01 10:30"],
    [2, "Proyecto Alfa", "Manual de Operación", "DOC-001", "Carlos López", 2, "Obsoleto", "2024-09-15 11:20"],
    [3, "Proyecto Alfa", "Especificaciones Técnicas", "DOC-002", "María Pérez", 1, "En revisión", "2024-09-18 15:40"],
    [4, "Proyecto Beta", "Plan de Mantenimiento", "DOC-010", "Juan Ramírez", 1, "Borrador", "2024-07-22 09:10"],
    [5, "Proyecto Beta", "Plan de Mantenimiento", "DOC-010", "Juan Ramírez", 2, "En revisión", "2024-08-10 13:55"],
    [6, "Proyecto Beta", "Plan de Mantenimiento", "DOC-010", "Juan Ramírez", 3, "Aprobado", "2024-08-30 08:25"],
    [7, "Proyecto Gamma", "Informe de Pruebas", "DOC-020", "Ana Torres", 1, "Borrador", "2024-07-01 17:05"],
    [8, "Proyecto Gamma", "Informe de Pruebas", "DOC-020", "Ana Torres", 2, "Aprobado", "2024-08-02 14:00"],
    [9, "Proyecto Gamma", "Lista de Materiales", "DOC-021", "Luis García", 1, "En revisión", "2024-07-19 09:15"],
    [10, "Proyecto Delta", "Contrato Principal", "DOC-030", "Elena Ruiz", 1, "Aprobado", "2024-06-28 10:45"],
    [11, "Proyecto Delta", "Anexo Contrato", "DOC-031", "Elena Ruiz", 1, "En revisión", "2024-07-30 16:20"],
    [12, "Proyecto Delta", "Anexo Contrato", "DOC-031", "Elena Ruiz", 2, "Aprobado", "2024-08-12 12:10"],
    [13, "Proyecto Epsilon", "Procedimiento de Seguridad", "DOC-040", "Miguel Sánchez", 1, "Borrador", "2024-06-10 08:30"],
    [14, "Proyecto Epsilon", "Procedimiento de Seguridad", "DOC-040", "Miguel Sánchez", 2, "En revisión", "2024-07-05 09:45"],
    [15, "Proyecto Epsilon", "Procedimiento de Seguridad", "DOC-040", "Miguel Sánchez", 3, "Aprobado", "2024-08-22 10:20"],
    [16, "Proyecto Zeta", "Reporte Financiero", "DOC-050", "Laura Gómez", 1, "Aprobado", "2024-06-15 13:25"],
    [17, "Proyecto Zeta", "Reporte Financiero", "DOC-050", "Laura Gómez", 2, "Obsoleto", "2024-07-10 15:50"],
    [18, "Proyecto Zeta", "Reporte Financiero", "DOC-050", "Laura Gómez", 3, "Aprobado", "2024-08-05 11:40"],
    [19, "Proyecto Omega", "Plan de Ejecución", "DOC-060", "Fernando Díaz", 1, "Borrador", "2024-07-01 09:00"],
    [20, "Proyecto Omega", "Plan de Ejecución", "DOC-060", "Fernando Díaz", 2, "En revisión", "2024-08-03 10:30"],
]

# Crear DataFrame
df = pd.DataFrame(data, columns=[
    "ID", "Proyecto", "Documento", "Código", "Responsable", "Versión", "Estado", "Fecha Registro"
])

# --- Título ---
st.title("📑 Sistema de Control Documental")
st.markdown("Base de datos con 20 documentos de ejemplo (gestión por proyectos, versiones y estados).")

# --- Filtros ---
st.sidebar.header("🔍 Filtros")
proyecto_sel = st.sidebar.multiselect("Proyecto", options=df["Proyecto"].unique(), default=df["Proyecto"].unique())
estado_sel = st.sidebar.multiselect("Estado", options=df["Estado"].unique(), default=df["Estado"].unique())
responsable_sel = st.sidebar.multiselect("Responsable", options=df["Responsable"].unique(), default=df["Responsable"].unique())

# Aplicar filtros
df_filtrado = df[
    (df["Proyecto"].isin(proyecto_sel)) &
    (df["Estado"].isin(estado_sel)) &
    (df["Responsable"].isin(responsable_sel))
]

# --- Mostrar resultados ---
st.subheader("📋 Documentos en control")
st.dataframe(df_filtrado, use_container_width=True)

# --- Estadísticas ---
st.subheader("📊 Estadísticas")
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df_filtrado["Estado"].value_counts())
with col2:
    st.bar_chart(df_filtrado["Proyecto"].value_counts())
