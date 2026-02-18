import os
from crewai import Agent, Task, Crew, Process, LLM
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv(override=True)

# IMportacion de JSON
with open('TSLA_financiero.json', 'r', encoding='utf-8') as archivo:
    json_datos = json.load(archivo)
    

# --- DEFINICIÓN DE MODELOS ---

# --- ANALISTAS ---
# GROQ (Llama 3): Analizará el Momento y Sentimiento
llm_trader = LLM(
    model="groq/llama-3.3-70b-versatile", 
    api_key=os.getenv('GROQ_API_KEY'),
)


# DEEPSEEK: Encargado de analisis de ratios.  #### DESABILITADO - SE CAMBIA POR GROQ ####
# llm_quant = ChatOpenAI(
#     model="deepseek-chat", 
#     api_key=os.getenv('DEEPSEEK_API_KEY'),
#     base_url="https://api.deepseek.com"
# )
llm_quant = LLM(
    model="groq/llama-3.3-70b-versatile", 
    api_key=os.getenv('GROQ_API_KEY'),
)

# GEMINI: Analizará el Sector y la Competencia.
llm_visionario = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv('GEMINI_API_KEY'),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# OLLAMA (llama3.1 Local): Auditor de Riesgos.
llm_auditor = LLM(
    model="ollama/llama3.1",
    api_key="ollama",
    base_url="http://localhost:11434"
)

# --- SECRETARIO JUDICIAL ---
# OPENAI (GPT-4o-mini): Redacta un resumen ejecutivo de las respuestas de los analistas.
llm_secretario = LLM(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- JUEZ ---
# OPENAI (GPT-4o): Encargado del veredicto final.
llm_juez = LLM(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

# --- CREACIÓN DE LOS AGENTES ---

# Agente 1: El Quant (DeepSeek)
agente_quant = Agent(
    role='Analista Cuantitativo Senior',
    goal='Analizar la salud financiera basándose ESTRICTAMENTE en los números y ratios.',
    backstory='Eres un matemático frío. No te importan las noticias ni las promesas del CEO. Solo confías en el ROE, PEG Ratio y el Margen Neto. Si los números no cuadran, es venta.',
    llm=llm_quant,
    verbose=True
)

tarea_quant = Task(
    description=f"""
    Analiza los datos financieros en el JSON: {{json_datos}}
    
    Tu trabajo es auditar la coherencia matemática entre PRECIO y VALOR.
    
    1. **Valuación (PEG y PE):** - Busca el "PEG Ratio". Si es 'null', negativo o mayor a 2.0, considéralo una SOBREVALORACIÓN o falta de ganancias.
       - Compara el "Forward PE" con el "Trailing PE". Si el Forward es menor, el mercado espera crecimiento. Si es mayor, espera contracción.
       
    2. **Rentabilidad (ROE y Márgenes):**
       - Analiza la tendencia del "ROE (%)" y "Margen Neto (%)" en la sección histórica. 
       - ¿Están subiendo (mejora de eficiencia) o bajando (pérdida de competitividad)?
       - Si el ROE es menor al 10%, critícalo severamente.
       
    3. **Solvencia:**
       - Revisa el nivel de endeudamiento. Si supera 0.6 o 0.7, levanta una alerta.
    
    Salida: Informe técnico. ¿Los números justifican el precio actual o es pura especulación?
    """,
    expected_output="Informe Quant. Análisis de tendencias de márgenes, retorno y valuación relativa.",
    agent=agente_quant
)

# Agente 2: El Visionario (Gemini)
agente_visionario = Agent(
    role='Analista de Estrategia y Mercado',
    goal='Analizar el sector, la competencia y el potencial de crecimiento a largo plazo.',
    backstory='Eres un inversor de Venture Capital. Buscas la próxima gran cosa. Te enfocas en la innovación, el "Moat" (ventaja competitiva) y si la industria está en expansión.',
    llm=llm_visionario,
    verbose=True
)
tarea_visionario = Task(
    description=f"""
    Analiza el "Sector", "Industria" y métricas de crecimiento en: {{json_datos}}
    
    Tu trabajo es evaluar la CALIDAD del negocio y su FUTURO.
    
    1. **Contexto Sectorial:** Basado en el campo "Industria", ¿es un sector en auge (ej: IA, Salud) o estancado (ej: Tabaco, Diarios)?
    2. **Crecimiento:** Mira "Crecimiento de Ventas" y "Crecimiento de Ganancias". 
       - Si son positivos: ¿Justifican una prima en el precio?
       - Si son negativos: ¿Es un bache temporal o la empresa está muriendo?
    3. **Ventaja Competitiva (Moat):** Basado en los márgenes históricos, ¿crees que la empresa tiene poder de fijación de precios?
    
    Salida: ¿Es un negocio maravilloso a un precio justo, o un negocio mediocre?
    """,
    expected_output="Informe Estratégico. Evaluación del modelo de negocio y su sostenibilidad a 5 años.",
    agent=agente_visionario
)

# Agente 3: El Trader (Groq)
agente_trader = Agent(
    role='Trader de Momentum y Sentimiento',
    goal='Analizar si es un buen momento para entrar basado en el precio actual y el sentimiento.',
    backstory='Eres un trader de Wall Street impaciente. Te preocupa si la acción está sobrecomprada (cara hoy) o si hay pánico en el mercado. Buscas oportunidades de entrada.',
    llm=llm_trader,
    verbose=True
)
tarea_trader = Task(
    description=f"""
    Analiza el "Precio Actual", "Beta_Riesgo" y "Valor Libro" en: {{json_datos}}
    
    Tu trabajo es evaluar el RIESGO DE PRECIO (Timing).
    
    1. **Volatilidad:** Mira el Beta. 
       - Si es > 1.5, es muy volátil (peligroso en recesiones).
       - Si es < 0.8, es defensiva.
       - Adecúa tu consejo al tipo de acción.
    2. **Precio vs Realidad:** Compara Precio Actual vs Valor Libro. Si la diferencia es astronómica (ej: 10x o más), ¿hay euforia irracional?
    3. **Sentimiento:** Interpreta la "Recomendación de Analistas" y el momento técnico implícito.
    
    Salida: ¿La acción está "En Oferta", "En Precio Justo" o "En Burbuja"?
    """,
    expected_output="Informe de Timing. Sugerencia sobre si es buen momento para entrar.",
    agent=agente_trader
)

# Agente 4: El Auditor (Ollama)
agente_auditor = Agent(
    role='Auditor de Riesgos (Bear)',
    goal='Encontrar Banderas Rojas (Red Flags) y razones para NO invertir.',
    backstory='Eres un contador forense paranoico. Crees que todas las empresas maquillan sus balances. Tu trabajo es proteger el capital encontrando deuda oculta o flujo de caja negativo.',
    llm=llm_auditor,
    verbose=True
)
tarea_auditor = Task(
    description=f"""
    Actúa como auditor forense. Revisa la sección "historico" del JSON: {{json_datos}}
    
    Busca patrones de DETERIORO FINANCIERO (No importa el nombre de la empresa):
    1. **La Prueba del Flujo de Caja:** ¿Es el "Free Cash Flow" consistentemente positivo? Si una empresa reporta "Utilidad Neta" positiva pero FCF negativo, es una ALERTA DE FRAUDE o mala gestión.
    2. **La Trampa de la Deuda:** Revisa si los "Total Liabilities" (Pasivos) crecen más rápido que los Activos año tras año.
    3. **Dilución:** Revisa si la cantidad de "Acciones (M)" aumenta cada año (diluyendo al accionista).
    
    Salida: Lista de Banderas Rojas. Si todo está perfecto, dilo, pero sé escéptico.
    """,
    expected_output="Informe de Riesgos. Lista de puntos débiles en el balance o flujo de caja.",
    agent=agente_auditor
)

# Agente 5: El Secretario (GPT-4o-mini)
agente_secretario = Agent(
    role='Secretario Judicial del Comité',
    goal='Sintetizar los 4 reportes de los analistas en un Memo Ejecutivo limpio y detectar contradicciones.',
    backstory='Eres la mano derecha del CIO. Tu trabajo es leer los informes técnicos y resumirlos en 1 página clara. Identificas dónde están de acuerdo y dónde se pelean los analistas.',
    llm=llm_secretario,
    verbose=True
)
tarea_secretario = Task(
    description="""
    Lee los 4 informes de los analistas.
    
    Tu misión es cruzar la información para encontrar la VERDAD:
    1. **Consensos:** ¿En qué métricas coinciden el Quant y el Auditor? (Ej: "Ambos ven deterioro en márgenes").
    2. **Conflictos:** ¿El Visionario ve futuro pero el Quant dice que los números no dan? Resalta esta discrepancia.
    3. **Datos Clave:** Extrae los 3 ratios más preocupantes o prometedores mencionados.
    
    Genera un Memo Ejecutivo imparcial. No des tu opinión, solo presenta los hechos de los analistas.
    """,
    expected_output="Memo Ejecutivo. Resumen estructurado de fortalezas, debilidades y conflictos entre analistas.",
    agent=agente_secretario,
    context=[tarea_quant, tarea_visionario, tarea_trader, tarea_auditor]
)

# Agente 6: El Juez (GPT-4o)
agente_juez = Agent(
    role='Chief Investment Officer (CIO)',
    goal='Tomar la decisión FINAL de inversión: COMPRAR, VENDER o SEGUIMIENTO).',
    backstory="""Tienes 30 años de experiencia gestionando fondos. Lees el resumen de tu secretario y tomas la decisión final. Eres responsable ante los accionistas.
    Eres decisivo. Odias la indecisión. Si la empresa es buena pero cara, la pones en SEGUIMIENTO. Si es mala, VENDER. Si es una joya, COMPRAR.""",
    llm=llm_juez,
    verbose=True
)
tarea_juez = Task(
    description="""
    Actúa como CIO. Lee el Memo del Secretario y emite un veredicto.
    
    Usa esta MATRIZ DE DECISIÓN para cualquier empresa:
    
    A) **COMPRAR (BUY):**
       - Fundamentos Crecientes (Ventas/Utilidades subiendo).
       - Precio Razonable (Quant y Trader no ven burbuja).
       - Auditoría Limpia (Sin banderas rojas graves).
    
    B) **VENDER (SELL):**
       - Fundamentos en Deterioro (Márgenes cayendo, Deuda subiendo).
       - Valuación Absurda sin crecimiento que la respalde.
       - Riesgo de Quiebra o Fraude (Alertas del Auditor).
    
    C) **SEGUIMIENTO (WATCHLIST) - Caso Especial:**
       - Empresa de Calidad (Visionario/Quant dan visto bueno al negocio).
       - PERO: El Precio es excesivo (Trader alerta sobrecompra) O el Mercado está incierto.
       - **Obligatorio:** Si eliges esto, define un "Precio de Entrada" (ej: "Esperar corrección del 10%").
    
    Justifica tu decisión basándote en el equilibrio Riesgo/Beneficio presentado.
    """,
    expected_output="Veredicto Final [COMPRAR | VENDER | SEGUIMIENTO]. Justificación y Precio Objetivo/Gatillo.",
    agent=agente_juez,
    context=[tarea_secretario]
)

comite = Crew(
    agents=[agente_quant, agente_visionario, agente_trader, agente_auditor, agente_secretario, agente_juez],
    tasks=[tarea_quant, tarea_visionario, tarea_trader, tarea_auditor, tarea_secretario, tarea_juez],
    process=Process.sequential,
    verbose=True
)