import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Juego del Impostor", page_icon="🕵️")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
    }
    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🕵️ ¿Quién es el Impostor?")

# --- 1. BASE DE DATOS DE PALABRAS ---
# ¡Aquí es donde tú editas las palabras!
BANCO_DE_PALABRAS = {
    "Objetos": ["Silla", "Microondas", "Cepillo de dientes", "Espejo", "Reloj", "Paraguas"],
    "Lugares": ["Hospital", "Cementerio", "Escuela", "Playa", "Cine", "Cárcel", "Supermercado"],
    "Comida": ["Pizza", "Sushi", "Paella", "Helado", "Brocoli", "Hamburguesa"],
    "Animales": ["Jirafa", "Pingüino", "León", "Mosquito", "Dinosaurio", "Perro"],
    "Profesiones": ["Bombero", "Astronauta", "Profesor", "Futbolista", "Payaso"]
}

# --- INICIALIZACIÓN DE ESTADO ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'setup' # setup, revealing, playing
if 'players' not in st.session_state:
    st.session_state.players = []
if 'impostors' not in st.session_state:
    st.session_state.impostors = []
if 'secret_word' not in st.session_state:
    st.session_state.secret_word = ""
if 'category_played' not in st.session_state:
    st.session_state.category_played = ""
if 'current_player_idx' not in st.session_state:
    st.session_state.current_player_idx = 0
if 'role_visible' not in st.session_state:
    st.session_state.role_visible = False

# --- FASE 1: CONFIGURACIÓN ---
if st.session_state.game_state == 'setup':
    st.header("Configuración de la Partida")

    # 1. Input de Jugadores
    players_input = st.text_area("Participantes (un nombre por línea)", height=150, placeholder="Ana\nBeto\nCarla\nDaniel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 2. Selección de Categoría
        opciones_cat = ["Aleatorio (Todas)"] + list(BANCO_DE_PALABRAS.keys())
        categoria_elegida = st.selectbox("Categoría de palabras", opciones_cat)
    
    with col2:
        # 3. Cantidad de Impostores
        num_impostores = st.number_input("Número de Impostores", min_value=1, max_value=5, value=1)

    if st.button("¡GENERAR PARTIDA!"):
        # Limpieza de nombres
        player_list = [p.strip() for p in players_input.split('\n') if p.strip()]
        
        # Validaciones
        if len(player_list) < 3:
            st.error("⚠️ Se necesitan al menos 3 jugadores.")
        elif num_impostores >= len(player_list):
            st.error("⚠️ No puede haber más (o iguales) impostores que jugadores.")
        else:
            # LÓGICA DE SELECCIÓN
            
            # A. Elegir palabra
            if categoria_elegida == "Aleatorio (Todas)":
                todas_las_listas = list(BANCO_DE_PALABRAS.values())
                # Aplanamos la lista de listas en una sola lista grande
                lista_plana = [item for sublist in todas_las_listas for item in sublist]
                palabra_secreta = random.choice(lista_plana)
                cat_actual = "Mix Aleatorio"
            else:
                palabra_secreta = random.choice(BANCO_DE_PALABRAS[categoria_elegida])
                cat_actual = categoria_elegida

            # B. Elegir Impostores (random.sample asegura que no se repitan)
            impostores_elegidos = random.sample(player_list, num_impostores)

            # Guardar en memoria
            st.session_state.players = player_list
            st.session_state.secret_word = palabra_secreta
            st.session_state.category_played = cat_actual
            st.session_state.impostors = impostores_elegidos
            st.session_state.game_state = 'revealing'
            st.session_state.current_player_idx = 0
            st.rerun()

# --- FASE 2: REVELAR ROLES (PASA EL MÓVIL) ---
elif st.session_state.game_state == 'revealing':
    current_player = st.session_state.players[st.session_state.current_player_idx]
    
    st.subheader(f"Turno de: {current_player}")
    st.info("Pasa el móvil a este jugador. ¡Que nadie mire!")
    
    if not st.session_state.role_visible:
        if st.button(f"Soy {current_player}, ver mi carta"):
            st.session_state.role_visible = True
            st.rerun()
    else:
        # Mostrar Rol
        st.markdown("---")
        
        if current_player in st.session_state.impostors:
            st.markdown("<p class='big-font' style='color:red;'>😈 ERES IMPOSTOR</p>", unsafe_allow_html=True)
            st.write(f"Categoría: {st.session_state.category_played}")
            st.write("Tu misión: Engañar a todos y descubrir la palabra.")
        else:
            st.markdown("<p class='big-font' style='color:green;'>😇 ERES CIVIL</p>", unsafe_allow_html=True)
            st.write(f"La palabra secreta es:")
            st.markdown(f"<p class='big-font'>{st.session_state.secret_word}</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botón siguiente
        texto_boton = "Ocultar y pasar al siguiente"
        if st.session_state.current_player_idx == len(st.session_state.players) - 1:
            texto_boton = "Ocultar y EMPEZAR JUEGO"
            
        if st.button(texto_boton):
            st.session_state.role_visible = False
            st.session_state.current_player_idx += 1
            
            if st.session_state.current_player_idx >= len(st.session_state.players):
                st.session_state.game_state = 'playing'
            
            st.rerun()

# --- FASE 3: JUEGO Y RESULTADOS ---
elif st.session_state.game_state == 'playing':
    st.header("¡A JUGAR!")
    if len(st.session_state.impostors) > 1:
        st.warning(f"⚠️ Cuidado: Hay {len(st.session_state.impostors)} impostores entre nosotros.")
    else:
        st.warning("⚠️ Hay 1 impostor entre nosotros.")
    
    st.info(f"Temática: {st.session_state.category_played}")
    
    st.write("Cuando terminen de debatir y votar, pulsad el botón.")
    
    with st.expander("Ver Resultado Final (Solo al terminar)"):
        st.success(f"La palabra era: **{st.session_state.secret_word}**")
        st.error(f"Los impostores eran: **{', '.join(st.session_state.impostors)}**")
        
        # Botón de Reset
        if st.button("🔄 Jugar otra partida (Reset)"):
            st.session_state.game_state = 'setup'
            st.session_state.impostors = []
            st.session_state.secret_word = ""
            st.session_state.current_player_idx = 0
            st.rerun()
