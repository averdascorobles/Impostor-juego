import streamlit as st
import random

st.set_page_config(page_title="La Caja Fuerte del Impostor", page_icon="🔐")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 22px;
        font-weight: bold;
    }
    .status-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 La Caja Fuerte")

# --- INICIALIZAR MEMORIA ---
if 'estado' not in st.session_state:
    st.session_state.estado = 'banco' # banco, config_jugadores, revelar, jugando
if 'banco_palabras' not in st.session_state:
    st.session_state.banco_palabras = []
if 'jugadores' not in st.session_state:
    st.session_state.jugadores = []
if 'impostores_actuales' not in st.session_state:
    st.session_state.impostores_actuales = []
if 'palabra_actual' not in st.session_state:
    st.session_state.palabra_actual = ""
if 'turno' not in st.session_state:
    st.session_state.turno = 0
if 'ver_rol' not in st.session_state:
    st.session_state.ver_rol = False

# --- BARRA LATERAL (Info) ---
with st.sidebar:
    st.header("📦 Estado de la Caja")
    count = len(st.session_state.banco_palabras)
    st.write(f"Palabras guardadas: **{count}**")
    if count > 0:
        st.success("¡Hay munición para jugar!")
    else:
        st.warning("La caja está vacía.")
        
    if st.button("🗑️ Vaciar Caja (Reiniciar todo)"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# FASE 1: LLENAR EL BANCO (LA URNA)
# ==========================================
if st.session_state.estado == 'banco':
    st.markdown("### 1️⃣ Llenad la caja de palabras")
    st.info("Pasa el móvil. Escribe una palabra divertida y dale a 'Guardar'. Nadie verá lo que escribes.")

    # Formulario que se limpia solo
    with st.form("form_banco", clear_on_submit=True):
        # type="password" para que salgan puntitos •••••
        nueva_palabra = st.text_input("Escribe tu palabra secreta:", type="password")
        enviado = st.form_submit_button("📥 Guardar en la Caja")
        
        if enviado:
            if nueva_palabra:
                st.session_state.banco_palabras.append(nueva_palabra)
                st.toast(f"¡Palabra guardada! Total: {len(st.session_state.banco_palabras)}")
            else:
                st.warning("Escribe algo antes de guardar.")

    st.markdown("---")
    st.write(f"Palabras acumuladas hasta ahora: **{len(st.session_state.banco_palabras)}**")
    
    if len(st.session_state.banco_palabras) >= 2:
        if st.button("✅ ¡Ya tenemos suficientes! Configurar Jugadores"):
            st.session_state.estado = 'config_jugadores'
            st.rerun()

# ==========================================
# FASE 2: QUIÉNES JUEGAN
# ==========================================
elif st.session_state.estado == 'config_jugadores':
    st.markdown("### 2️⃣ ¿Quiénes juegan hoy?")
    
    texto_nombres = st.text_area("Nombres (uno por línea)", 
                                 value="\n".join(st.session_state.jugadores) if st.session_state.jugadores else "",
                                 height=150,
                                 placeholder="Ana\nBeto\nCarla")
    
    num_impostores = st.number_input("Número de Impostores", 1, 3, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Añadir más palabras"):
            st.session_state.estado = 'banco'
            st.rerun()
    with col2:
        if st.button("🚀 ¡EMPEZAR RONDA!"):
            lista = [n.strip() for n in texto_nombres.split('\n') if n.strip()]
            if len(lista) < 3:
                st.error("Mínimo 3 jugadores.")
            elif not st.session_state.banco_palabras:
                st.error("¡La caja de palabras está vacía! Volved atrás.")
            else:
                # GUARDAR JUGADORES
                st.session_state.jugadores = lista
                
                # SACAR PALABRA DE LA CAJA (Y BORRARLA PARA QUE NO REPITA)
                # Seleccionamos índice aleatorio
                idx_azar = random.randrange(len(st.session_state.banco_palabras))
                # La sacamos de la lista y la guardamos como actual
                st.session_state.palabra_actual = st.session_state.banco_palabras.pop(idx_azar)
                
                # ELEGIR IMPOSTORES
                st.session_state.impostores_actuales = random.sample(lista, num_impostores)
                
                st.session_state.estado = 'revelar'
                st.session_state.turno = 0
                st.rerun()

# ==========================================
# FASE 3: REVELAR (PASA EL MÓVIL)
# ==========================================
elif st.session_state.estado == 'revelar':
    jugador = st.session_state.jugadores[st.session_state.turno]
    
    st.subheader(f"Turno de: {jugador}")
    
    if not st.session_state.ver_rol:
        st.info("🤫 Pasa el móvil. Solo tú puedes ver esto.")
        if st.button(f"Ver mi carta ({jugador})"):
            st.session_state.ver_rol = True
            st.rerun()
    else:
        st.markdown("---")
        if jugador in st.session_state.impostores_actuales:
            st.error("😈 ERES EL IMPOSTOR")
            st.write("Finge que sabes la palabra. Escucha a los demás.")
        else:
            st.success("😇 ERES CIVIL")
            st.write("La palabra de la caja es:")
            st.markdown(f"## **{st.session_state.palabra_actual}**")
        st.markdown("---")
        
        texto_btn = "Ocultar y siguiente"
        if st.session_state.turno == len(st.session_state.jugadores) - 1:
            texto_btn = "⚔️ ¡A JUGAR!"
            
        if st.button(texto_btn):
            st.session_state.ver_rol = False
            st.session_state.turno += 1
            if st.session_state.turno >= len(st.session_state.jugadores):
                st.session_state.estado = 'jugando'
            st.rerun()

# ==========================================
# FASE 4: JUEGO Y SIGUIENTE RONDA
# ==========================================
elif st.session_state.estado == 'jugando':
    st.balloons()
    st.header("⏳ DEBATE EN CURSO")
    st.write(f"Impostores ocultos: **{len(st.session_state.impostores_actuales)}**")
    
    with st.expander("👁️ Ver Solución de esta ronda"):
        st.write(f"Palabra: **{st.session_state.palabra_actual}**")
        st.write(f"Impostores: **{', '.join(st.session_state.impostores_actuales)}**")
    
    st.markdown("---")
    st.subheader("¿Qué hacemos ahora?")
    
    palabras_restantes = len(st.session_state.banco_palabras)
    st.write(f"Quedan **{palabras_restantes}** palabras en la caja fuerte.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Añadir más palabras"):
            st.session_state.estado = 'banco'
            st.session_state.palabra_actual = "" # Limpiar ronda anterior
            st.rerun()
            
    with col2:
        if palabras_restantes > 0:
            if st.button("🔄 Siguiente Ronda (Palabra Nueva)"):
                # LÓGICA DE NUEVA RONDA SIN REPETIR SETUP
                idx_azar = random.randrange(len(st.session_state.banco_palabras))
                st.session_state.palabra_actual = st.session_state.banco_palabras.pop(idx_azar)
                
                # Nuevos impostores (mismos jugadores)
                num = min(len(st.session_state.jugadores)-1, len(st.session_state.impostores_actuales) if st.session_state.impostores_actuales else 1)
                st.session_state.impostores_actuales = random.sample(st.session_state.jugadores, num) # Mantiene cant. impostores
                
                st.session_state.estado = 'revelar'
                st.session_state.turno = 0
                st.rerun()
        else:
            st.error("¡Se acabaron las palabras! Añadid más.")

