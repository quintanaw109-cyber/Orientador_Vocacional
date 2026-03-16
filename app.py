import streamlit as st
import pandas as pd
import time

# ==============================================================================
# 1. CONFIGURACIÓN DE AUTORÍA Y PÁGINA
# ==============================================================================
AUTOR = "Ing. William Verdecia Quintana"  # <--- CAMBIA ESTO POR TU NOMBRE REAL
APP_NAME = "Orientador Vocacional Ecuador - TIC & Más"
VERSION = "v5.0 Final (SENESCYT Oct 2024 + Sheet)"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🇪🇨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #2c3e50; text-align: center; }
    h2, h3 { color: #27ae60; }
    .stButton>button { 
        width: 100%; 
        background-color: #27ae60; 
        color: white; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #219150; }
    .resultado-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        margin-bottom: 20px; 
        border-left: 5px solid #27ae60; 
    }
    .footer { text-align: center; margin-top: 50px; color: #7f8c8d; font-size: 0.8em; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNCIONES DE PROCESAMIENTO DE DATOS
# ==============================================================================

def normalizar_columnas(df):
    """Normaliza nombres de columnas para evitar errores KeyError."""
    df.columns = df.columns.str.lower().str.strip()
    
    mapa_nombres = {
        'nombre_carrera': 'carrera', 'nombre': 'carrera', 'carrera': 'carrera',
        'matematicas': 'mat', 'mat': 'mat',
        'logica': 'log', 'log': 'log',
        'creatividad': 'cre', 'cre': 'cre',
        'social': 'soc', 'soc': 'soc',
        'verbal': 'ver', 'ver': 'ver',
        'tecnico': 'tec', 'tec': 'tec',
        'justificacion_es': 'justificacion_es',
        'justificacion_en': 'justificacion_en',
        'justificacion_fr': 'justificacion_fr',
        'justificacion_qu': 'justificacion_qu'
    }
    
    columnas_actuales = df.columns.tolist()
    renombrar_dict = {orig: est for orig, est in mapa_nombres.items() if orig in columnas_actuales}
    
    if renombrar_dict:
        df = df.rename(columns=renombrar_dict)
    return df

@st.cache_data
def cargar_datos_desde_sheet(url):
    if not url:
        return None
    try:
        df = pd.read_csv(url)
        if df.empty:
            return None
        return normalizar_columnas(df)
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return None

def obtener_datos_maestros():
    # Intentar cargar desde URL si existe
    if URL_GOOGLE_SHEET:
        df = cargar_datos_desde_sheet(URL_GOOGLE_SHEET)
        if df is not None and not df.empty:
            if 'carrera' in df.columns and 'mat' in df.columns:
                return df
            else:
                st.warning("El Google Sheet no tiene las columnas correctas. Usando datos de respaldo del PDF SENESCYT.")
    
    # DATOS DE RESPALDO (Extraídos EXACTAMENTE del PDF subido - Carreras Únicas Consolidadas)
    data_respaldo = [
        {"carrera": "Desarrollo de Software", "mat": 5, "log": 5, "cre": 4, "soc": 2, "ver": 3, "tec": 5, 
         "justificacion_es": "Ideal para crear soluciones digitales. Requiere alta lógica matemática.",
         "justificacion_en": "Ideal for creating digital solutions. Requires high mathematical logic.",
         "justificacion_fr": "Idéal pour créer des solutions numériques. Nécessite une forte logique.",
         "justificacion_qu": "Allin solucionkunata kamariypaq. Hatun yupay logica munan."},
        
        {"carrera": "Transformación Digital de Empresas", "mat": 3, "log": 4, "cre": 3, "soc": 4, "ver": 4, "tec": 4,
         "justificacion_es": "Liderar cambios tecnológicos en organizaciones. Visión de negocio.",
         "justificacion_en": "Leading technological changes in organizations. Business vision.",
         "justificacion_fr": "Diriger les changements technologiques. Vision commerciale.",
         "justificacion_qu": "Organizacionkunapi tecnologico tikraykunata pusay."},
        
        {"carrera": "Comunicación y Gestión de Datos con Inteligencia Artificial", "mat": 5, "log": 5, "cre": 3, "soc": 2, "ver": 4, "tec": 5,
         "justificacion_es": "Híbrido tecnología/comunicación. Perfiles analíticos en IA.",
         "justificacion_en": "Tech/Communication hybrid. Analytical profiles in AI.",
         "justificacion_fr": "Hybride Technologie/Communication. Profils analytiques en IA.",
         "justificacion_qu": "Tecnologia/Rimay chaqrusqa. IA nisqawan analitico."},
        
        {"carrera": "Redes y Telecomunicaciones", "mat": 4, "log": 4, "cre": 2, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Infraestructura física y lógica de conexiones.",
         "justificacion_en": "Physical and logical infrastructure of connections.",
         "justificacion_fr": "Infrastructure physique et logique des connexions.",
         "justificacion_qu": "Tinkiykunapa fisico hinaspa logico infraestructura."},
        
        {"carrera": "Ensamblaje y Mantenimiento de Equipos de Cómputo", "mat": 3, "log": 4, "cre": 3, "soc": 3, "ver": 2, "tec": 5,
         "justificacion_es": "Perfil práctico. Trabajo con hardware y reparación.",
         "justificacion_en": "Practical profile. Working with hardware and repair.",
         "justificacion_fr": "Profil pratique. Travail avec le matériel.",
         "justificacion_qu": "Practico perfil. Hardwarewan llamk'ay."},
        
        {"carrera": "Administración de Sistemas Informáticos en Red", "mat": 3, "log": 4, "cre": 2, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Gestión de servidores y redes corporativas.",
         "justificacion_en": "Management of servers and corporate networks.",
         "justificacion_fr": "Gestion des serveurs et réseaux d'entreprise.",
         "justificacion_qu": "Servidorukuna hinaspa empresa redkuna gestion."},
        
        {"carrera": "Big Data e Inteligencia de Negocio", "mat": 5, "log": 5, "cre": 3, "soc": 2, "ver": 4, "tec": 5,
         "justificacion_es": "Matemáticas avanzadas para encontrar patrones en grandes datos.",
         "justificacion_en": "Advanced math to find patterns in big data.",
         "justificacion_fr": "Mathématiques avancées pour trouver des motifs dans les mégadonnées.",
         "justificacion_qu": "Hatun datokunapi patrones tarinapaq advanced yupay."},
        
        {"carrera": "Desarrollo de Aplicaciones Web", "mat": 4, "log": 5, "cre": 5, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Lógica de programación con creatividad visual web.",
         "justificacion_en": "Programming logic with visual creativity for web.",
         "justificacion_fr": "Logique de programmation avec créativité visuelle web.",
         "justificacion_qu": "Web paginakunapaq programacion logica hinaspa visual creatividad."},
        
        {"carrera": "Internet de las Cosas (IoT)", "mat": 4, "log": 4, "cre": 4, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Conecta objetos físicos a internet. Domótica y sensores.",
         "justificacion_en": "Connects physical objects to internet. Domotics and sensors.",
         "justificacion_fr": "Connecte les objets physiques à Internet. Domotique.",
         "justificacion_qu": "Fisico objetokunata internetman t'inkin."},
        
        {"carrera": "Gestión de Bases de Datos", "mat": 4, "log": 5, "cre": 2, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Almacenamiento y seguridad de información crítica.",
         "justificacion_en": "Storage and security of critical information.",
         "justificacion_fr": "Stockage et sécurité des informations critiques.",
         "justificacion_qu": "Empresa critica informacion waqaychay."},
        
        {"carrera": "Desarrollo de Videojuegos y Experiencias Interactivas Digitales", "mat": 4, "log": 5, "cre": 5, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Programación avanzada combinada con arte y narrativa.",
         "justificacion_en": "Advanced programming combined with art and narrative.",
         "justificacion_fr": "Programmation avancée combinée à l'art et la narration.",
         "justificacion_qu": "Avanzado programacion arte, willakuy hinaspa diseño."},
        
        {"carrera": "Desarrollo de Aplicaciones Móviles", "mat": 4, "log": 5, "cre": 5, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Creación de apps para celulares. Lógica y UX.",
         "justificacion_en": "Creation of mobile apps. Logic and UX.",
         "justificacion_fr": "Création d'applications mobiles. Logique et UX.",
         "justificacion_qu": "Celular aplicacionkunata kamariy."},
        
        {"carrera": "Inteligencia Artificial", "mat": 5, "log": 5, "cre": 4, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Vanguardia tecnológica. Matemáticas y lógica abstracta.",
         "justificacion_en": "Technological forefront. Math and abstract logic.",
         "justificacion_fr": "Avant-garde technologique. Mathématiques et logique abstraite.",
         "justificacion_qu": "Tecnologico ñawpaq kaq. Yupay, abstracto logica."},
        
        {"carrera": "Ciberseguridad", "mat": 4, "log": 5, "cre": 3, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Protección de sistemas y privacidad digital.",
         "justificacion_en": "System protection and digital privacy.",
         "justificacion_fr": "Protection des systèmes et vie privée numérique.",
         "justificacion_qu": "Sistemakunata amachay, digital privacidad."},
        
        {"carrera": "Análisis y Desarrollo Web", "mat": 4, "log": 5, "cre": 4, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Arquitectura de la información y requisitos web.",
         "justificacion_en": "Information architecture and web requirements.",
         "justificacion_fr": "Architecture de l'information et besoins web.",
         "justificacion_qu": "Informacion arquitectura hinaspa web requisitos."},
        
        {"carrera": "Seguridad Informática", "mat": 4, "log": 5, "cre": 2, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Auditoría de sistemas y prevención de delitos.",
         "justificacion_en": "System auditing and crime prevention.",
         "justificacion_fr": "Audit des systèmes et prévention de la cybercriminalité.",
         "justificacion_qu": "Sistema auditoria hinaspa delitokunata hark'ay."},
        
        {"carrera": "Infraestructura de Redes y Cyber Seguridad", "mat": 4, "log": 5, "cre": 2, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Montar redes robustas y asegurarlas contra ataques.",
         "justificacion_en": "Building robust networks and securing them.",
         "justificacion_fr": "Construire des réseaux robustes et les sécuriser.",
         "justificacion_qu": "Fuerte redkunata ruway hinaspa amachay."},
        
        {"carrera": "Sistemas y Gestión de Data", "mat": 4, "log": 4, "cre": 2, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Administración integral de información y sistemas.",
         "justificacion_en": "Comprehensive management of information systems.",
         "justificacion_fr": "Gestion complète des systèmes d'information.",
         "justificacion_qu": "Informacion hinaspa sistemakunapa administracion."},
        
        {"carrera": "Instalación y Mantenimiento de Redes", "mat": 3, "log": 3, "cre": 2, "soc": 3, "ver": 2, "tec": 5,
         "justificacion_es": "Tendido y reparación física de redes de datos.",
         "justificacion_en": "Laying and physical repair of data networks.",
         "justificacion_fr": "Pose et réparation physique des réseaux de données.",
         "justificacion_qu": "Datos redkunapa tendido hinaspa allichay."},
        
        {"carrera": "Administración de Infraestructura y Plataformas Tecnológicas", "mat": 3, "log": 4, "cre": 2, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Gestión de servidores, nube y plataformas.",
         "justificacion_en": "Management of servers, cloud, and platforms.",
         "justificacion_fr": "Gestion des serveurs, cloud et plateformes.",
         "justificacion_qu": "Servidorukuna, nube hinaspa plataformakuna gestion."},
        
        {"carrera": "Internet de las Cosas y Computación en la Nube", "mat": 4, "log": 4, "cre": 4, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Conectividad de dispositivos con servicios en la nube.",
         "justificacion_en": "Device connectivity with cloud services.",
         "justificacion_fr": "Connectivité des appareils avec services cloud.",
         "justificacion_qu": "Dispositivotinkiy nube serviciokuna gestionwan."},
        
        {"carrera": "Desarrollo de Software y Programación", "mat": 5, "log": 5, "cre": 4, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Enfoque intensivo en codificación pura.",
         "justificacion_en": "Intensive focus on pure coding.",
         "justificacion_fr": "Accent intensif sur le codage pur.",
         "justificacion_qu": "Puro codificacion hinaspa programacion."},
        
        {"carrera": "Diseño y Mantenimiento de Redes", "mat": 3, "log": 3, "cre": 2, "soc": 3, "ver": 2, "tec": 5,
         "justificacion_es": "Diseño lógico y reparación de infraestructura de red.",
         "justificacion_en": "Logical design and repair of network infrastructure.",
         "justificacion_fr": "Conception logique et réparation réseau.",
         "justificacion_qu": "Red infraestructurapa logico diseño hinaspa allichay."},
        
        {"carrera": "Sistemas de Información y Ciberseguridad", "mat": 4, "log": 5, "cre": 2, "soc": 2, "ver": 3, "tec": 5,
         "justificacion_es": "Gestión de sistemas con protocolos de seguridad.",
         "justificacion_en": "System management with security protocols.",
         "justificacion_fr": "Gestion des systèmes avec protocoles de sécurité.",
         "justificacion_qu": "Sistema gestion seguridad protocolokunawan."},
        
        {"carrera": "Gestión de Redes y Telecomunicaciones", "mat": 4, "log": 4, "cre": 2, "soc": 3, "ver": 3, "tec": 5,
         "justificacion_es": "Administración estratégica de redes de comunicación.",
         "justificacion_en": "Strategic management of communication networks.",
         "justificacion_fr": "Gestion stratégique des réseaux de communication.",
         "justificacion_qu": "Comunicacion redkunapa estrategico administracion."},
         
        # Carreras No-TIC Esenciales
        {"carrera": "Medicina", "mat": 4, "log": 5, "cre": 2, "soc": 5, "ver": 3, "tec": 4,
         "justificacion_es": "Vocación de servicio y análisis clínico.",
         "justificacion_en": "Service vocation and clinical analysis.",
         "justificacion_fr": "Vocation de service et analyse clinique.",
         "justificacion_qu": "Servicio vocacion hinaspa clinico analisis."},
        {"carrera": "Ingeniería Civil", "mat": 5, "log": 5, "cre": 3, "soc": 2, "ver": 2, "tec": 5,
         "justificacion_es": "Matemáticas aplicadas e infraestructura tangible.",
         "justificacion_en": "Applied mathematics and tangible infrastructure.",
         "justificacion_fr": "Mathématiques appliquées et infrastructures tangibles.",
         "justificacion_qu": "Aplicado yupay hinaspa tangible infraestructura."},
        {"carrera": "Derecho", "mat": 2, "log": 4, "cre": 2, "soc": 4, "ver": 5, "tec": 1,
         "justificacion_es": "Capacidad verbal y sentido de justicia.",
         "justificacion_en": "Verbal ability and sense of justice.",
         "justificacion_fr": "Capacité verbale et sens de la justice.",
         "justificacion_qu": "Verbal atiy hinaspa justicia sentido."},
        {"carrera": "Educación Intercultural Bilingüe", "mat": 2, "log": 3, "cre": 3, "soc": 5, "ver": 5, "tec": 2,
         "justificacion_es": "Valoración cultural y vocación comunitaria.",
         "justificacion_en": "Cultural appreciation and community vocation.",
         "justificacion_fr": "Appréciation culturelle et vocation communautaire.",
         "justificacion_qu": "Cultura valoracion hinaspa comunidad vocacion."}
    ]
    
    df_respaldo = pd.DataFrame(data_respaldo)
    return normalizar_columnas(df_respaldo)

# ==============================================================================
# 3. CONFIGURACIÓN DE URL (GOOGLE SHEETS)
# ==============================================================================
# 👇👇👇 PEGA TU ENLACE CSV AQUÍ ABAJO ENTRE LAS COMILLAS 👇👇👇
# Si lo dejas vacío "", usará los datos del PDF integrados arriba.
URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSLzI17_23U2iFrZceztV_APjgpJpBYelt6yVDb5m9IXYHKKT0oaGp4xf15SVt0rsJ7oByzC07N7r7P/pub?output=csv" 

# Cargar DataFrame Maestro
df_carreras = obtener_datos_maestros()

# ==============================================================================
# 4. BANCO DE PREGUNTAS MULTILINGÜE
# ==============================================================================
preguntas_data = [
    {"id": 1, "area": "mat", "es": "¿Te gusta resolver problemas complejos usando números?", "en": "Do you enjoy solving complex problems using numbers?", "fr": "Aimez-vous résoudre des problèmes complexes avec des nombres ?", "qu": "¿Kusikunkichu yupaykunawan sasachakuykunata allichinata?"},
    {"id": 2, "area": "log", "es": "¿Disfrutas analizando cómo funcionan las cosas paso a paso?", "en": "Do you enjoy analyzing how things work step-by-step?", "fr": "Aimez-vous analyser comment les choses fonctionnent étape par étape ?", "qu": "¿Kusikunkichu imakuna imayna llamk'asqanta paso a paso t'aqwiyta?"},
    {"id": 3, "area": "cre", "es": "¿Te imaginas creando diseños nuevos o aplicaciones visuales?", "en": "Can you imagine creating new designs or visual applications?", "fr": "Pouvez-vous imaginer créer de nouveaux designs ou applications visuelles ?", "qu": "¿Muspaykunchu musuq diseñokunata utaq aplicacionkunata kamariyta?"},
    {"id": 4, "area": "soc", "es": "¿Te sientes realizado ayudando a otras personas?", "en": "Do you feel fulfilled helping other people?", "fr": "Vous sentez-vous épanoui en aidant les autres ?", "qu": "¿Shuktakunata yanapaspa allillanchu sintekunki?"},
    {"id": 5, "area": "ver", "es": "¿Te gusta leer, escribir o debatir ideas?", "en": "Do you like reading, writing, or debating ideas?", "fr": "Aimez-vous lire, écrire ou débattre d'idées ?", "qu": "¿Kusikunkichu ñawinchiyta, quillqayta utaq yuyaykunata rimarinakuypi?"},
    {"id": 6, "area": "tec", "es": "¿Te interesa saber cómo funcionan las computadoras por dentro?", "en": "Are you interested in how computers work inside?", "fr": "Êtes-vous intéressé de savoir comment fonctionnent les ordinateurs ?", "qu": "¿Munankichu yachayta imaynatas computadorakuna ukupi llamk'anku?"},
    {"id": 7, "area": "log", "es": "¿Eres bueno encontrando errores en sistemas (depuración)?", "en": "Are you good at finding errors in systems (debugging)?", "fr": "Êtes-vous bon pour trouver des erreurs dans les systèmes ?", "qu": "¿Allillachu kanqa huk sistemapi pantaykunata taripay?"},
    {"id": 8, "area": "mat", "es": "¿Te facilita interpretar gráficos y estadísticas?", "en": "Is it easy for you to interpret graphs and statistics?", "fr": "Est-il facile d'interpréter des graphiques et statistiques ?", "qu": "¿Facilchu kanqa graficoskunata estadisticakunata entiendey?"},
    {"id": 9, "area": "cre", "es": "¿Prefieres inventar soluciones nuevas antes que seguir instrucciones?", "en": "Do you prefer inventing new solutions rather than following instructions?", "fr": "Préférez-vous inventer de nouvelles solutions plutôt que suivre des instructions ?", "qu": "¿Munankichu musuq solucionkunata inventarayta manataq instrucciónkunata qatipaychu?"},
    {"id": 10, "area": "tec", "es": "¿Te gustaría configurar servidores o proteger datos?", "en": "Would you like to configure servers or protect data?", "fr": "Aimeriez-vous configurer des serveurs ou protéger des données ?", "qu": "¿Munankichu servidorukunata configurayta datokunata amachayta?"}
]

# ==============================================================================
# 5. FUNCIONES LÓGICAS
# ==============================================================================

def calcular_perfil(respuestas):
    areas = ['mat', 'log', 'cre', 'soc', 'ver', 'tec']
    perfil = {a: 0 for a in areas}
    conteo = {a: 0 for a in areas}
    for r in respuestas:
        area = r['area']
        valor = r['valor']
        perfil[area] += valor
        conteo[area] += 1
    for a in areas:
        if conteo[a] > 0:
            perfil[a] /= conteo[a]
    return perfil

def recomendar(perfil, df, lang_code):
    resultados = []
    if 'carrera' not in df.columns:
        return []
    
    col_justif = f"justificacion_{lang_code}"
    if col_justif not in df.columns:
        col_justif = 'justificacion_es'
    
    areas_map = {'mat': 'mat', 'log': 'log', 'cre': 'cre', 'soc': 'soc', 'ver': 'ver', 'tec': 'tec'}
    
    for _, row in df.iterrows():
        puntaje = 0
        valido = True
        for area, col_name in areas_map.items():
            if col_name not in row:
                valido = False
                break
            try:
                val_carrera = float(row[col_name])
                diff = abs(val_carrera - perfil[area])
                puntaje += (5 - diff)
            except (ValueError, TypeError):
                valido = False
                break
        
        if not valido: continue
            
        porc = (puntaje / 30) * 100
        justificacion = row.get(col_justif, row.get('justificacion_es', 'Sin descripción.'))
        
        resultados.append({
            "carrera": str(row['carrera']),
            "score": round(porc, 1),
            "justificacion": justificacion
        })
    
    return sorted(resultados, key=lambda x: x['score'], reverse=True)

# ==============================================================================
# 6. INTERFAZ PRINCIPAL
# ==============================================================================

def main():
    with st.sidebar:
        st.image("https://share.google/WbFjvFBHxOT9WozLw", width=80)
        st.title("Configuración")
        st.markdown(f"**Autor:** {AUTOR}")
        st.markdown(f"**Versión:** {VERSION}")
        st.info("Desarrollado para Ecuador 🇪🇨\nInclusivo & Multilingüe")
        
        lang_options = {"Español": "es", "English": "en", "Français": "fr", "Kichwa": "qu"}
        idioma_sel = st.selectbox("Selecciona Idioma / Language", list(lang_options.keys()))
        lang_code = lang_options[idioma_sel]

    st.title("🎓 Orientador Vocacional Inteligente")
    st.markdown(f"### {APP_NAME}")
    st.markdown("Descubre tu carrera ideal en Ecuador basada en tus habilidades reales.")
    st.divider()

    if 'completado' not in st.session_state:
        st.session_state.completado = False
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = []

    if not st.session_state.completado:
        st.subheader("📝 Test de 10 Preguntas")
        st.markdown("Responde del 1 (Nada de acuerdo) al 5 (Muy de acuerdo).")
        
        with st.form("test_form"):
            respuestas_temp = []
            cols = st.columns(2)
            for i, q in enumerate(preguntas_data):
                texto_q = q[lang_code]
                col_idx = i % 2
                with cols[col_idx]:
                    val = st.slider(f"{q['id']}. {texto_q}", 1, 5, 3, key=f"q_{q['id']}")
                    respuestas_temp.append({"area": q['area'], "valor": val})
            
            submitted = st.form_submit_button("🚀 Calcular mi Carrera Ideal")
            if submitted:
                st.session_state.respuestas = respuestas_temp
                st.session_state.completado = True
                st.rerun()
    
    else:
        perfil = calcular_perfil(st.session_state.respuestas)
        
        if df_carreras.empty or 'carrera' not in df_carreras.columns:
            st.error("⚠️ Error crítico: No se cargaron datos válidos. Verifica tu Google Sheet o el código.")
            st.stop()
            
        recomendaciones = recomendar(perfil, df_carreras, lang_code)
        
        if not recomendaciones:
            st.error("No se pudieron generar recomendaciones. Verifica las columnas numéricas.")
            st.stop()

        st.success("✅ ¡Análisis completado!")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📊 Tu Perfil")
            df_perfil = pd.DataFrame({
                'Habilidad': ['Matemáticas', 'Lógica', 'Creatividad', 'Social', 'Verbal', 'Técnico'],
                'Nivel': [round(perfil['mat'], 1), round(perfil['log'], 1), round(perfil['cre'], 1), round(perfil['soc'], 1), round(perfil['ver'], 1), round(perfil['tec'], 1)]
            })
            st.bar_chart(df_perfil.set_index('Habilidad'), use_container_width=True)
            
            if st.button("🔄 Volver a empezar"):
                st.session_state.completado = False
                st.rerun()
        
        with col2:
            st.markdown("### 🏆 Top 3 Carreras Recomendadas")
            textos_btn = {
                "es": {"opcion": "Opción", "compat": "Compatibilidad", "porque": "💡 Por qué"},
                "en": {"opcion": "Option", "compat": "Compatibility", "porque": "💡 Why"},
                "fr": {"opcion": "Option", "compat": "Compatibilité", "porque": "💡 Pourquoi"},
                "qu": {"opcion": "Akllay", "compat": "Tupachiy", "porque": "💡 Imarayku"}
            }
            t = textos_btn[lang_code]
            
            for i, rec in enumerate(recomendaciones[:3]):
                medalla = "🥇" if i == 0 else ("🥈" if i == 1 else "🥉")
                st.markdown(f"""
                <div class="resultado-card">
                    <h3>{medalla} {t['opcion']} #{i+1}: {rec['carrera']}</h3>
                    <p><b>{t['compat']}:</b> {rec['score']}%</p>
                    <p><i>{t['porque']}: {rec['justificacion']}</i></p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div class='footer'>© 2024 {APP_NAME}. Developed by {AUTOR}. Based on SENESCYT Data (Oct 2024).</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()