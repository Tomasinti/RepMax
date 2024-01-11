from datetime import datetime
import streamlit as st 
import pandas as pd
import numpy as np
import altair as alt
from streamlit_option_menu import option_menu
import database as db


# ---------- VARIABLES -----------
ejercicios = ["Press Banca", "Press Militar", "Dominadas", "Peso Muerto", "Sentadilla"]

if "resultados" not in st.session_state:
    st.session_state.resultados = {}

fecha = datetime.today().date().strftime("%d/%m/%y")
periodo = datetime.today().date().strftime("%d/%m/%y")
nuevo_id = None

# ---------- DATABASE --------------

# ---------- PAGINA --------------
page_title = "Calculadora de RM"
page_icon = "🏋🏻‍♂️"
layout = "centered"

# --- CONFIG & MENU---
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
container = st.container(border=True)

#----------- ESTILO STREAMLIT ----------
hide_st_style ="""
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

with container:
    title_text = '<span style="color: #0083B8; font-style: italic;">Rep</span>etición <span style="color: #0083B8; font-style: italic;">Máx</span>ima'
    st.markdown(f'<h1 style="color: #ffffff; font-style: italic; text-align: center; padding-left: 20px;" id="titulin">{title_text}</h1>', unsafe_allow_html=True)
   
# ---------- INPUTS -----------
    container = st.container(border=True)
    with container:
        selected = option_menu(
        menu_title=None,
        options=["Calculadora", "Visualización"],
        icons = ["calculator-fill","bar-chart-fill"],
        orientation="horizontal",
    )
        
        if selected == "Calculadora":
            st.text("Elige tu ejercicio, introduce el peso que levantas y cuántas repeticiones\nmáximas haces y obtén el resultado de tu 1RM.")
            st.header("_Tu RM_", divider='blue')
            with st.form("entry_form", clear_on_submit=True):
                ejercicio = st.selectbox("Seleccione el ejercicio", ejercicios, key="ejercicio")
                peso = st.session_state.peso = st.number_input("Ingrese el peso (KG)", value=0.0, step=0.1, format="%.1f", key="pesokg")
                repeticiones =st.session_state.repes = st.number_input("Ingrese la cantidad de repeticiones", value=0, step=1, key="repeticion")
                submitted = st.form_submit_button(":blue[Calcular RM]")
                if submitted:
                    if st.session_state.peso > 0 and st.session_state.repes > 0:
                        task = str(ejercicio)
                        rm = st.session_state.peso * st.session_state.repes * 0.03 + st.session_state.peso  # Calcular rm
                        nuevo_id = db.insertar_periodo(fecha, ejercicio, st.session_state.peso, st.session_state.repes, rm)

                        # Almacenar el nuevo resultado con el ID asociado directamente en el diccionario
                        if task not in st.session_state.resultados:
                            st.session_state.resultados[task] = {"id": nuevo_id, "data": []}
                        st.session_state.resultados[task]["data"].append({"id": nuevo_id, "rm": rm})

                        st.success(f"La Repetición Máxima (RM) calculada es de {rm}KG en {task}.")
                    else:
                        st.info("Por favor, ingrese un valor válido tanto en el peso como en las repeticiones.", icon="❗")

# ... (código posterior)

# ---------- GRAFICO DE BARRAS -----------
        if selected == "Visualización":
            st.text("Visualiza tus RM y sigue de cerca tu progreso en cada ejercicio.")
            st.header("_Graficos_", divider='blue')
            if not any(st.session_state.resultados):
                st.info("Aún no se han ingresado datos para graficar.", icon="❗")
            else:
                ejercicios = list(st.session_state.resultados.keys())

                for ejercicio in ejercicios:
                    expander = st.expander(ejercicio)

                    expander.text("Evolución 1 RM")

                    colores = {
                        "Press Banca": "#1f77b4",
                        "Press Militar": "#1f77b4",
                        "Dominadas": "#1f77b4",
                        "Peso Muerto": "#1f77b4",
                        "Sentadilla": "#1f77b4"
                    }
                    color = colores.get(ejercicio, "#000000")
                    
                    # Construir DataFrame utilizando la nueva estructura
                    data = st.session_state.resultados[ejercicio]["data"]
                    chart_data = pd.DataFrame({
                        "RM": [entry["rm"] for entry in data],
                        "Carga": range(1, len(data) + 1),
                        "Fecha": [fecha] * len(data)
                    })

                    # Convierte la columna de fecha al formato datetime
                    chart_data["Fecha"] = pd.to_datetime(chart_data["Fecha"], format="%d/%m/%y")

                    chart = alt.Chart(chart_data).mark_bar(color="blue", width=25).encode(
                        x=alt.X("Carga:N", title="Carga y Fecha", axis=alt.Axis(ticks=False, bandPosition=1, labelAngle=0), sort=None),
                        y=alt.Y("RM:Q", title="RM en KG", axis=alt.Axis(ticks=False)),
                        tooltip=[alt.Tooltip("Carga:N", title="Carga"), alt.Tooltip("Fecha:T", title="Fecha"), alt.Tooltip("RM:Q", title="RM en KG")],
                    ).properties(height=300)

# Muestra el gráfico con Altair en Streamlit


                    expander.altair_chart(chart, use_container_width=True)

                    eliminar_button = expander.button(f"Eliminar {ejercicio}", key=f"eliminar_{ejercicio}")

                    try:
                        if eliminar_button:
                            # Obtener el ID único asociado al nombre del ejercicio
                            id_asociado = st.session_state.resultados[ejercicio]["id"]
                            if id_asociado:
                                # Eliminar directamente el registro de la base de datos
                                db.eliminar_periodo(id_asociado)
                                st.session_state.resultados.pop(ejercicio, None)
                                st.rerun()
                    except RuntimeError as e:
                        st.error(f"Error: {e}. Por favor, intenta de nuevo.", icon ="☠️")

#---------- BOTON CAFECITO -----------
    

    contenido_markdown = '''
        <div style="display: flex; justify-content: center; align-items: center; padding:20px;">
            <a href='https://cafecito.app/tmalafiej' rel='noopener' target='_blank'><img srcset='https://cdn.cafecito.app/imgs/buttons/button_5.png 1x,
            https://cdn.cafecito.app/imgs/buttons/button_5_2x.png 2x, https://cdn.cafecito.app/imgs/buttons/button_5_3.75x.png 3.75x'
            src='https://cdn.cafecito.app/imgs/buttons/button_5.png' alt='Invitame un café en cafecito.app' />
            </a>
        </div> 
    '''
    st.markdown(contenido_markdown, unsafe_allow_html=True)

