import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ---------------------------
# FUNCIONES
# ---------------------------
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

def ajustar_mm(df):
    S = df["Sustrato"].values
    v = df["Velocidad"].values
    popt, _ = curve_fit(michaelis_menten, S, v, bounds=(0, np.inf))
    Vmax, Km = popt
    return Vmax, Km

# ---------------------------
# INTERFAZ DE LA APP
# ---------------------------
st.title("🧪 Análisis de Cinética Enzimática - Modelo de Michaelis-Menten")

st.write("""
Esta aplicación te permite ajustar el modelo de **Michaelis-Menten** 
a tus datos experimentales de velocidad inicial vs. concentración de sustrato.
""")

opcion = st.radio("Selecciona cómo quieres ingresar los datos:", ["📋 Ingresar manualmente", "📁 Subir archivo CSV"])

# ---------------------------
# OPCIÓN 1: INGRESAR MANUALMENTE
# ---------------------------
if opcion == "📋 Ingresar manualmente":
    st.write("Introduce tus datos de concentración de sustrato y velocidad:")

    # Crear una tabla editable
    data = pd.DataFrame({
        "Sustrato": [0.0]*10,
        "Velocidad": [0.0]*10
    })
    df = st.data_editor(data, num_rows="dynamic")

# ---------------------------
# OPCIÓN 2: SUBIR ARCHIVO
# ---------------------------
else:
    archivo = st.file_uploader("Sube tu archivo CSV con columnas 'Sustrato' y 'Velocidad'", type=["csv"])
    if archivo is not None:
        df = pd.read_csv(archivo)
        st.write("Datos cargados correctamente:")
        st.dataframe(df)
    else:
        st.stop()

# ---------------------------
# AJUSTE DEL MODELO
# ---------------------------
if st.button("🔍 Calcular parámetros cinéticos"):
    try:
        Vmax, Km = ajustar_mm(df)
        st.success(f"✅ Vmax = {Vmax:.4f}")
        st.success(f"✅ Km = {Km:.4f}")

        # Graficar ajuste
        S = df["Sustrato"]
        v = df["Velocidad"]
        S_fit = np.linspace(0, max(S)*1.1, 100)
        v_fit = michaelis_menten(S_fit, Vmax, Km)

        fig, ax = plt.subplots()
        ax.scatter(S, v, label="Datos experimentales")
        ax.plot(S_fit, v_fit, color="red", label="Ajuste Michaelis-Menten")
        ax.set_xlabel("[S] (concentración de sustrato)")
        ax.set_ylabel("v (velocidad de reacción)")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
