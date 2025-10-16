import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard Tribológico", layout="wide")

# --- Cargar datos ---
df = pd.read_csv("results (1).txt", sep="\t") 

# --- Limpieza ---
df.columns = df.columns.str.strip()
df = df.replace([np.inf, -np.inf], np.nan).dropna()

# --- Sidebar ---
st.sidebar.title("Filtros")
shapes = st.sidebar.multiselect("Seleccionar geometrías:", df["shape"].unique(), default=df["shape"].unique())
df_filtered = df[df["shape"].isin(shapes)]

st.title("📊 Dashboard de Análisis Tribológico y Sensores Ópticos")
st.markdown("Comparación entre superficies **lisas (S)** y **texturizadas (C-X)**.")

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("COF Promedio", f"{df_filtered['COF'].mean():.4f}")
col2.metric("LCC Promedio [N]", f"{df_filtered['LCC'].mean():.2f}")
col3.metric("h_min Promedio [m]", f"{df_filtered['h_min'].mean():.2e}")
col4.metric("Eficiencia (LCC/COF)", f"{(df_filtered['LCC']/df_filtered['COF']).mean():.2f}")

st.markdown("---")

# --- Gráfico 1: COF vs E (Curva Stribeck) ---
fig1 = px.line(df_filtered, x="E", y="COF", color="shape", markers=True,
               title="Curva Stribeck - COF vs Eccentricidad",
               labels={"E": "Eccentricidad", "COF": "Coeficiente de Fricción"})
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: LCC vs E ---
fig2 = px.line(df_filtered, x="E", y="LCC", color="shape", markers=True,
               title="Capacidad de Carga (LCC) vs Eccentricidad",
               labels={"LCC": "Carga de Soporte (N)"})
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: COF Promedio por Shape ---
avg_cof = df_filtered.groupby("shape")["COF"].mean().reset_index()
fig3 = px.bar(avg_cof, x="shape", y="COF", title="COF Promedio por Geometría",
              color="shape", text="COF")
st.plotly_chart(fig3, use_container_width=True)

# --- Gráfico 4: Relación LCC/COF ---
df_filtered["Eficiencia"] = df_filtered["LCC"] / df_filtered["COF"]
fig4 = px.scatter(df_filtered, x="E", y="Eficiencia", color="shape",
                  size="h_min", title="Relación Eficiencia (LCC/COF) vs E")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Desarrollado por Andrés Gutiérrez | Proyecto BI - Laboratorio de Materiales")
