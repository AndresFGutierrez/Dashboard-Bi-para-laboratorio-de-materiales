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

# Top N selector
top_n = st.sidebar.slider("Seleccionar Top N geometrías (según menor COF promedio):", 3, 20, 10)

# Calcular promedio COF por geometría
avg_cof = df.groupby("shape")["COF"].mean().sort_values(ascending=True).reset_index()

# Filtrar Top N
top_shapes = avg_cof.head(top_n)["shape"].tolist()

# Filtro principal del dataset
df_filtered = df[df["shape"].isin(top_shapes)]

# Sidebar extra: permitir seleccionar manualmente dentro del Top N
shapes_selected = st.sidebar.multiselect(
    "Seleccionar geometrías específicas:",
    options=top_shapes,
    default=top_shapes
)
df_filtered = df_filtered[df_filtered["shape"].isin(shapes_selected)]

# --- KPIs ---
st.title("📊 Dashboard de Análisis Tribológico (Top Geometrías)")
st.markdown("Mostrando las **Top {} geometrías** con menor coeficiente de fricción promedio.".format(top_n))

col1, col2, col3, col4 = st.columns(4)
col1.metric("COF Promedio", f"{df_filtered['COF'].mean():.4f}")
col2.metric("LCC Promedio [N]", f"{df_filtered['LCC'].mean():.2f}")
col3.metric("h_min Promedio [m]", f"{df_filtered['h_min'].mean():.2e}")
col4.metric("Eficiencia (LCC/COF)", f"{(df_filtered['LCC']/df_filtered['COF']).mean():.2f}")

st.markdown("---")

# --- Gráfico 1: COF vs E (Curva Stribeck) ---
fig1 = px.line(
    df_filtered, x="E", y="COF", color="shape", markers=True,
    title=f"Curva Stribeck - COF vs Eccentricidad (Top {top_n})",
    labels={"E": "Eccentricidad", "COF": "Coeficiente de Fricción"}
)
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico 2: LCC vs E ---
fig2 = px.line(
    df_filtered, x="E", y="LCC", color="shape", markers=True,
    title="Capacidad de Carga (LCC) vs Eccentricidad",
    labels={"LCC": "Carga de Soporte (N)"}
)
st.plotly_chart(fig2, use_container_width=True)

# --- Gráfico 3: COF Promedio por Shape ---
fig3 = px.bar(
    avg_cof.head(top_n), x="shape", y="COF", color="shape", text="COF",
    title=f"COF Promedio por Geometría (Top {top_n})"
)
st.plotly_chart(fig3, use_container_width=True)

# --- Gráfico 4: Relación LCC/COF ---
df_filtered["Eficiencia"] = df_filtered["LCC"] / df_filtered["COF"]
fig4 = px.scatter(
    df_filtered, x="E", y="Eficiencia", color="shape", size="h_min",
    title=f"Relación Eficiencia (LCC/COF) vs Eccentricidad (Top {top_n})"
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Desarrollado por Andrés Gutiérrez | Proyecto BI - Laboratorio de Materiales")
