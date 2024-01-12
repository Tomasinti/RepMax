import streamlit as st

# ---------- VARIABLES -----------
ejercicios = ["Press Banca", "Press Militar", "Dominadas", "Peso Muerto", "Sentadilla"]

if "resultados" not in st.session_state:
    st.session_state.resultados = {}

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
                        

                        # Almacenar el nuevo resultado con el ID asociado directamente en el diccionario
                        if task not in st.session_state.resultados:
                            st.session_state.resultados[task] = {"data": []}
                        st.session_state.resultados[task]["data"].append({ "rm": rm})

                        st.success(f"La Repetición Máxima (RM) calculada es de {rm}KG en {task}.")
                    else:
                        st.info("Por favor, ingrese un valor válido tanto en el peso como en las repeticiones.", icon="❗")


