import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA Y MEMORIA
st.set_page_config(page_title="Software Nutricional - Clínico", layout="wide")

# Inicializar la "memoria" del menú en la sesión actual
if 'menu' not in st.session_state:
    st.session_state.menu = []

# 2. BASE DE DATOS MAESTRA (ADA + MINSAL)
# Se han ajustado los valores nulos a 0 en las comidas típicas para permitir cálculos matemáticos exactos
datos_alimentos = [
    {"id": "lac_001", "nombre": "Leche fluida entera", "grupo": "Leches", "porcion": "1 taza", "carbohidratos": 12, "proteinas": 8, "grasas": 8, "kcal": 160},
    {"id": "lac_002", "nombre": "Incaparina (preparada)", "grupo": "Leches", "porcion": "200 mL", "carbohidratos": 23, "proteinas": 3.9, "grasas": 0.5, "kcal": 114},
    {"id": "lac_003", "nombre": "Yogurt simple descremado", "grupo": "Leches", "porcion": "1 taza", "carbohidratos": 12, "proteinas": 8, "grasas": 0, "kcal": 100},
    {"id": "veg_001", "nombre": "Flor de izote", "grupo": "Vegetales", "porcion": "1/2 taza", "carbohidratos": 5, "proteinas": 2, "grasas": 0, "kcal": 25},
    {"id": "veg_002", "nombre": "Chipilín / Loroco", "grupo": "Vegetales", "porcion": "1/2 taza", "carbohidratos": 5, "proteinas": 2, "grasas": 0, "kcal": 25},
    {"id": "fru_001", "nombre": "Anona / Zunza", "grupo": "Frutas", "porcion": "1/4 unid.", "carbohidratos": 15, "proteinas": 0, "grasas": 0, "kcal": 60},
    {"id": "fru_002", "nombre": "Guineo majoncho verde", "grupo": "Frutas", "porcion": "1/2 unid.", "carbohidratos": 15, "proteinas": 0, "grasas": 0, "kcal": 60},
    {"id": "alm_001", "nombre": "Tortilla de maíz blanco", "grupo": "Cereales", "porcion": "1 unid.", "carbohidratos": 15, "proteinas": 3, "grasas": 1, "kcal": 80},
    {"id": "alm_002", "nombre": "Frijoles (negros/rojos)", "grupo": "Cereales", "porcion": "1/2 taza", "carbohidratos": 15, "proteinas": 3, "grasas": 1, "kcal": 80},
    {"id": "pro_001", "nombre": "Pollo sin piel / Pescado", "grupo": "Proteínas Magras", "porcion": "1 oz", "carbohidratos": 0, "proteinas": 7, "grasas": 2, "kcal": 45},
    {"id": "pro_002", "nombre": "Huevo", "grupo": "Proteínas Semigrasas", "porcion": "1 unid.", "carbohidratos": 0, "proteinas": 7, "grasas": 5, "kcal": 75},
    {"id": "gra_001", "nombre": "Aguacate", "grupo": "Grasas", "porcion": "2 Cdas", "carbohidratos": 0, "proteinas": 0, "grasas": 5, "kcal": 45},
    {"id": "gra_002", "nombre": "Semilla de marañón", "grupo": "Grasas", "porcion": "20 semillas", "carbohidratos": 0, "proteinas": 0, "grasas": 5, "kcal": 45},
    {"id": "tip_001", "nombre": "Pupusa salvadoreña", "grupo": "Comidas Típicas", "porcion": "1 unid.", "carbohidratos": 30, "proteinas": 12, "grasas": 15, "kcal": 320},
    {"id": "tip_002", "nombre": "Tamal", "grupo": "Comidas Típicas", "porcion": "1 unid.", "carbohidratos": 45, "proteinas": 10, "grasas": 20, "kcal": 450},
]
df_alimentos = pd.DataFrame(datos_alimentos)

# 3. BARRA LATERAL DE NAVEGACIÓN Y METAS GLOBALES
st.sidebar.title("Menú Clínico")
st.sidebar.markdown("Dr. William Hernández")
modulo = st.sidebar.radio("Ir a:", ["Evaluación Antropométrica", "Constructor de Dietas"])

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Metas del Paciente")
meta_kcal = st.sidebar.number_input("Kcal Diarias", value=2000, step=50)
meta_carbos = st.sidebar.number_input("Carbohidratos (g)", value=250, step=5)
meta_prot = st.sidebar.number_input("Proteínas (g)", value=100, step=5)
meta_grasas = st.sidebar.number_input("Grasas (g)", value=65, step=5)

# ---------------------------------------------------------
# MÓDULO 1: EVALUACIÓN ANTROPOMÉTRICA
# ---------------------------------------------------------
if modulo == "Evaluación Antropométrica":
    st.title("⚖️ Evaluación Antropométrica")
    st.markdown("Ingrese los datos físicos del paciente para calcular su diagnóstico.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos Básicos")
        edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=25)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino"])
        peso_kg = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0)
        talla_m = st.number_input("Talla (metros)", min_value=0.5, max_value=2.5, value=1.70)
        
    with col2:
        st.subheader("Mediciones Adicionales (cm)")
        cintura = st.number_input("Circunferencia Cintura (cm)", min_value=30.0, max_value=200.0, value=85.0)
        cadera = st.number_input("Circunferencia Cadera (cm)", min_value=30.0, max_value=200.0, value=95.0)
        actividad = st.selectbox("Factor de Actividad", ["Sedentario", "Leve", "Moderado", "Activo", "Muy Activo"])

    st.markdown("---")
    
    st.subheader("Diagnóstico Automático")
    if talla_m > 0:
        imc = peso_kg / (talla_m ** 2)
        icc = cintura / cadera if cadera > 0 else 0
        
        if imc < 18.5: clasificacion = "Bajo peso"
        elif 18.5 <= imc < 24.9: clasificacion = "Normopeso"
        elif 25 <= imc < 29.9: clasificacion = "Sobrepeso"
        else: clasificacion = "Obesidad"
            
        c1, c2, c3 = st.columns(3)
        c1.metric("IMC", f"{imc:.1f}", clasificacion, delta_color="off")
        c2.metric("Índice Cintura-Cadera (ICC)", f"{icc:.2f}", delta_color="off")
        c3.metric("Peso Actual", f"{peso_kg} kg", delta_color="off")

# ---------------------------------------------------------
# MÓDULO 2: CONSTRUCTOR DE MENÚS (RESTA EN VIVO)
# ---------------------------------------------------------
elif modulo == "Constructor de Dietas":
    st.title("🍽️ Constructor Visual de Menús")
    
    # Cálculos en vivo del menú actual
    df_menu = pd.DataFrame(st.session_state.menu)
    
    if not df_menu.empty:
        consumido_kcal = df_menu["Kcal"].sum()
        consumido_carbos = df_menu["Carbohidratos"].sum()
        consumido_prot = df_menu["Proteínas"].sum()
        consumido_grasas = df_menu["Grasas"].sum()
    else:
        consumido_kcal = consumido_carbos = consumido_prot = consumido_grasas = 0

    # PANEL DE METAS (EL MARCADOR)
    st.subheader("📊 Marcador de Macronutrientes")
    m1, m2, m3, m4 = st.columns(4)
    
    # Usamos métricas de Streamlit para mostrar cuánto falta (resta en vivo)
    m1.metric("Kcal Restantes", f"{meta_kcal - consumido_kcal:.1f}", f"{consumido_kcal:.1f} consumidas", delta_color="inverse")
    m2.metric("Carbohidratos Restantes", f"{meta_carbos - consumido_carbos:.1f} g", f"{consumido_carbos:.1f} g consumidos", delta_color="inverse")
    m3.metric("Proteínas Restantes", f"{meta_prot - consumido_prot:.1f} g", f"{consumido_prot:.1f} g consumidos", delta_color="inverse")
    m4.metric("Grasas Restantes", f"{meta_grasas - consumido_grasas:.1f} g", f"{consumido_grasas:.1f} g consumidos", delta_color="inverse")

    st.markdown("---")
    
    # CONTROLES PARA AGREGAR ALIMENTOS
    col_add1, col_add2, col_add3, col_add4 = st.columns([3, 1, 2, 1])
    
    with col_add1:
        alimento_seleccionado = st.selectbox("Buscar Alimento (ADA/MINSAL)", df_alimentos['nombre'].tolist())
    with col_add2:
        porciones = st.number_input("Porciones", min_value=0.25, value=1.0, step=0.25)
    with col_add3:
        tiempo_comida = st.selectbox("Tiempo de Comida", ["Desayuno", "Refrigerio AM", "Almuerzo", "Refrigerio PM", "Cena"])
    with col_add4:
        st.markdown("<br>", unsafe_allow_html=True) # Espaciado para alinear el botón
        if st.button("➕ Agregar"):
            # Extraer datos del alimento seleccionado
            datos_item = df_alimentos[df_alimentos['nombre'] == alimento_seleccionado].iloc[0]
            
            # Guardar en la memoria de la sesión
            st.session_state.menu.append({
                "Tiempo": tiempo_comida,
                "Alimento": datos_item['nombre'],
                "Porciones": porciones,
                "Kcal": datos_item['kcal'] * porciones,
                "Carbohidratos": datos_item['carbohidratos'] * porciones,
                "Proteínas": datos_item['proteinas'] * porciones,
                "Grasas": datos_item['grasas'] * porciones
            })
            st.rerun() # Recargar para actualizar el marcador

    # MOSTRAR EL MENÚ CONSTRUIDO
    st.subheader("📝 Menú del Paciente")
    if not df_menu.empty:
        # Ordenar para que el menú tenga un flujo lógico
        orden_comidas = ["Desayuno", "Refrigerio AM", "Almuerzo", "Refrigerio PM", "Cena"]
        df_menu['Orden'] = pd.Categorical(df_menu['Tiempo'], categories=orden_comidas, ordered=True)
        df_menu = df_menu.sort_values('Orden').drop('Orden', axis=1)
        
        st.dataframe(df_menu, use_container_width=True)
        
        if st.button("🗑️ Limpiar Menú"):
            st.session_state.menu = []
            st.rerun()
    else:
        st.info("El menú está vacío. Selecciona alimentos y agrégalos para comenzar a construir la dieta.")
