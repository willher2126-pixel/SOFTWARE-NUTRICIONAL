import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Software Nutricional - Clínico", layout="wide")

# 2. BASE DE DATOS MAESTRA (ADA + MINSAL)
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
]
df_alimentos = pd.DataFrame(datos_alimentos)

# 3. BARRA LATERAL DE NAVEGACIÓN
st.sidebar.title("Menú Clínico")
st.sidebar.markdown("Dr. William Hernández")
modulo = st.sidebar.radio("Ir a:", ["Evaluación Antropométrica", "Constructor de Dietas"])

# ---------------------------------------------------------
# MÓDULO 1: EVALUACIÓN ANTROPOMÉTRICA
# ---------------------------------------------------------
if modulo == "Evaluación Antropométrica":
    st.title("⚖️ Evaluación Antropométrica")
    st.markdown("Ingrese los datos físicos del paciente para calcular su diagnóstico y requerimiento calórico.")
    
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
    
    # Cálculos Automáticos
    st.subheader("Diagnóstico Automático")
    if talla_m > 0:
        imc = peso_kg / (talla_m ** 2)
        icc = cintura / cadera if cadera > 0 else 0
        
        # Clasificación IMC
        if imc < 18.5: clasificacion = "Bajo peso"
        elif 18.5 <= imc < 24.9: clasificacion = "Normopeso"
        elif 25 <= imc < 29.9: clasificacion = "Sobrepeso"
        else: clasificacion = "Obesidad"
            
        c1, c2, c3 = st.columns(3)
        c1.metric("IMC", f"{imc:.1f}", clasificacion)
        c2.metric("Índice Cintura-Cadera (ICC)", f"{icc:.2f}")
        c3.metric("Peso Actual", f"{peso_kg} kg")

# ---------------------------------------------------------
# MÓDULO 2: CONSTRUCTOR DE MENÚS
# ---------------------------------------------------------
elif modulo == "Constructor de Dietas":
    st.title("🍽️ Constructor Visual de Menús")
    
    # Panel de Metas (Marcador)
    st.info("🎯 **Meta Diaria (Ejemplo):** 2000 Kcal | Carbohidratos: 250g | Proteínas: 100g | Grasas: 65g")
    
    # Buscador ADA / MINSAL
    st.subheader("Buscador de Alimentos ADA / MINSAL")
    busqueda = st.text_input("Escribe un alimento (ej. Pupusa, Frijoles, Flor de izote)...")
    
    if busqueda:
        df_filtrado = df_alimentos[df_alimentos['nombre'].str.contains(busqueda, case=False)]
        st.dataframe(df_filtrado[['nombre', 'grupo', 'porcion', 'kcal', 'carbohidratos', 'proteinas', 'grasas']], use_container_width=True)
    else:
        st.dataframe(df_alimentos[['nombre', 'grupo', 'porcion', 'kcal', 'carbohidratos', 'proteinas', 'grasas']], use_container_width=True)
        
    st.markdown("---")
    
    # Gestor de Tiempos de Comida
    st.subheader("Tiempos de Comida del Paciente")
    nuevo_tiempo = st.text_input("Nombre del bloque (ej. Desayuno, Almuerzo en la calle)")
    if st.button("➕ Agregar tiempo de comida"):
        st.success(f"Se ha agregado el bloque: {nuevo_tiempo} (Lógica de almacenamiento en desarrollo para la Fase 3)")
