import streamlit as st
import random
import time

# Configuración de la página
st.set_page_config(page_title="Juego del Impostor", page_icon="🕵️")

# Estilos CSS simples para ocultar elementos innecesarios y centrar
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ ¿Quién es el Impostor?")

# --- Inicialización del Estado (Memoria de la App) ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup' # setup, revealing, playing
if 'players' not in st.session_state:
    st.session_state.players = []
if 'impostor' not in st.session_state:
    st.session_state.impostor = ""
if 'secret_word' not in st.session_state:
    st.session_state.secret_word = ""
if 'current_player_idx' not in st.session_state:
    st.session_state.current_player_idx = 0
if 'role_visible' not in st.session_state:
    st.session_state.role_visible = False

# --- FASE 1: CONFIGURACIÓN ---
if st.session_state.game_state == 'setup':
    st.header("Configuración de la Partida")
    
    # Input para la palabra secreta (oculta con type="password" para que nadie la lea de reojo)
    secret_word = st.text_input("Escribe la palabra secreta (Ej: Pizza, Playa, Elon Musk)", type="password")
    
    # Input para los jugadores
    players_input = st.text_area("Nombres de los jugadores (uno por línea)", "Juan\nMaria\nPedro\nLucia")
    
    if st.button("¡Comenzar Juego!"):
        if secret_word and players_input:
            # Procesar jugadores
            player_list = [p.strip() for p in players_input.split('\n') if p.strip()]
            
            if len(player_list) < 3:
                st.error("Necesitas al menos 3 jugadores.")
            else:
                # Guardar en estado
                st.session_state.players = player_list
                st.session_state.secret_word = secret_word
                st.session_state.impostor = random.choice(player_list)
                st.session_state.game_state = 'revealing'
                st.session_state.current_player_idx = 0
                st.rerun()
        else:
            st.warning("Por favor rellena la palabra y los nombres.")

# --- FASE 2: REVELAR ROLES (PASA EL MÓVIL) ---
elif st.session_state.game_state == 'revealing':
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    st.subheader(f"Turno de: {current_player}")
    st.info("Pasa el móvil a este jugador. Nadie más debe mirar.")
    
    if not st.session_state.role_visible:
        if st.button(f"Soy {current_player}, mostrar mi rol"):
            st.session_state.role_visible = True
            st.rerun()
    else:
        # Mostrar el rol
        st.markdown("---")
        if current_player == st.session_state.impostor:
            st.error("😈 TÚ ERES EL IMPOSTOR")
            st.write("Tu objetivo: Engañar a los demás y adivinar la palabra.")
        else:
            st.success(f"😇 ERES CIVIL. La palabra es: **{st.session_state.secret_word}**")
        st.markdown("---")
        
        # Botón para continuar
        if st.button("Ocultar y pasar al siguiente"):
            st.session_state.role_visible = False
            st.session_state.current_player_idx += 1
            
            # Si ya pasaron todos, vamos a la fase final
            if st.session_state.current_player_idx >= len(st.session_state.players):
                st.session_state.game_state = 'playing'
            
            st.rerun()

# --- FASE 3: JUEGO EN CURSO ---
elif st.session_state.game_state == 'playing':
    st.balloons()
    st.header("¡A DEBATIR!")
    st.write("Todos han visto su rol. Empiecen las preguntas.")
    
    st.warning("⚠️ Cuando terminen la votación, pulsa abajo para ver quién era.")
    
    if st.button("Revelar al Impostor"):
        st.success(f"El impostor era... **{st.session_state.impostor}**")
        st.info(f"La palabra secreta era: {st.session_state.secret_word}")
        
        if st.button("Jugar otra vez"):
            # Resetear todo
            st.session_state.game_state = 'setup'
            st.session_state.impostor = ""
            st.session_state.secret_word = ""
            st.session_state.current_player_idx = 0
            st.rerun()
