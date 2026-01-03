import streamlit as st
import random

# ==========================================
# 1. TUS PALABRAS (EDITA AQUÍ)
# ==========================================
# Puedes añadir todas las que quieras entre comillas y separadas por comas.
# El sistema elegirá una al azar cada vez.
LISTA_DE_PALABRAS = [
    "Pizza", "Hospital", "Elon Musk", "Playa", "Cementerio", 
    "Superman", "McDonalds", "Iphone", "Drácula", "Biblioteca",
    "Gimnasio", "Dinosaurio", "Navidad", "Titanic", "Wifi"
]

# ==========================================
# CONFIGURACIÓN DE LA APP
# ==========================================
st.set_page_config(page_title="Impostor", page_icon="🕵️")

# Estilo para botones grandes en el móvil
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🕵️ JUEGO DEL IMPOSTOR")

# Inicializar memoria
if 'estado' not in st.session_state:
    st.session_state.estado = 'configuracion' 
if 'jugadores' not in st.session_state:
    st.session_state.jugadores = []
if 'impostores' not in st.session_state:
    st.session_state.impostores = []
if 'palabra' not in st.session_state:
    st.session_state.palabra = ""
if 'turno_actual' not in st.session_state:
    st.session_state.turno_actual = 0
if 'ver_rol' not in st.session_state:
    st.session_state.ver_rol = False

# ==========================================
# FASE 1: CONFIGURACIÓN (LO QUE PEDISTE)
# ==========================================
if st.session_state.estado == 'configuracion':
    st.markdown("### ⚙️ Configura la partida")
    
    # 1. CAJA DE TEXTO PARA NOMBRES
    texto_nombres = st.text_area("Escribe los nombres (uno por línea):", height=150, placeholder="Juan\nMaria\nPedro\nLuis")
    
    # 2. SELECTOR DE NÚMERO DE IMPOSTORES
    num_impostores = st.number_input("¿Cuántos impostores?", min_value=1, max_value=3, value=1)
    
    st.write(f"📝 *Palabras disponibles en el código: {len(LISTA_DE_PALABRAS)}*")

    if st.button("¡REPARTIR CARTAS!"):
        # Convertir texto a lista
        lista_jugadores = [nombre.strip() for nombre in texto_nombres.split('\n') if nombre.strip()]
        
        # Validaciones
        if len(lista_jugadores) < 3:
            st.error("⚠️ Mínimo 3 jugadores.")
        elif num_impostores >= len(lista_jugadores):
            st.error("⚠️ Demasiados impostores para tan poca gente.")
        else:
            # --- LA MAGIA (SELECCIÓN ALEATORIA) ---
            st.session_state.jugadores = lista_jugadores
            st.session_state.palabra = random.choice(LISTA_DE_PALABRAS) # Elige palabra del código
            st.session_state.impostores = random.sample(lista_jugadores, num_impostores) # Elige impostores
            
            # Cambiar de fase
            st.session_state.estado = 'revelar'
            st.session_state.turno_actual = 0
            st.rerun()

# ==========================================
# FASE 2: PASAR EL MÓVIL (VER ROLES)
# ==========================================
elif st.session_state.estado == 'revelar':
    jugador_actual = st.session_state.jugadores[st.session_state.turno_actual]
    
    st.subheader(f"Turno de: {jugador_actual}")
    
    if not st.session_state.ver_rol:
        st.info("Pasa el móvil. Nadie más debe mirar.")
        if st.button(f"Soy {jugador_actual}, VER MI CARTA"):
            st.session_state.ver_rol = True
            st.rerun()
    else:
        st.markdown("---")
        # Lógica de qué mostrar
        if jugador_actual in st.session_state.impostores:
            st.error("😈 ERES EL IMPOSTOR")
            st.write("¡Engaña a todos!")
        else:
            st.success("😇 ERES CIVIL")
            st.write(f"La palabra es: **{st.session_state.palabra}**")
        st.markdown("---")
        
        # Botón para siguiente
        texto_btn = "Ocultar y pasar al siguiente"
        # Si es el último, cambiamos el texto
        if st.session_state.turno_actual == len(st.session_state.jugadores) - 1:
            texto_btn = "Ocultar y EMPEZAR JUEGO"
            
        if st.button(texto_btn):
            st.session_state.ver_rol = False
            st.session_state.turno_actual += 1
            
            if st.session_state.turno_actual >= len(st.session_state.jugadores):
                st.session_state.estado = 'jugando'
            
            st.rerun()

# ==========================================
# FASE 3: JUGANDO Y RESET
# ==========================================
elif st.session_state.estado == 'jugando':
    st.balloons()
    st.header("⏳ ¡TIEMPO DE DEBATE!")
    
    st.info(f"Hay **{len(st.session_state.impostores)}** impostor(es) entre vosotros.")
    st.write("Haced preguntas y descubrid quién miente.")
    
    # Acordeón para ver la solución sin querer
    with st.expander("👁️ VER RESULTADO FINAL (SOLUCIÓN)"):
        st.write(f"La palabra era: **{st.session_state.palabra}**")
        st.write(f"Los impostores eran: **{', '.join(st.session_state.impostores)}**")
        
        # BOTÓN RESET QUE PEDISTE
        if st.button("🔄 Jugar otra partida (Reset)"):
            st.session_state.estado = 'configuracion'
            st.session_state.jugadores = []
            st.session_state.impostores = []
            st.session_state.palabra = ""
            st.rerun()
