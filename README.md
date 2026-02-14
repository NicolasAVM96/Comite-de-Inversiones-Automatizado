🤖 Comité de Inversiones Automatizado (AI Investment Committee)
Estado: 🚧 En Desarrollo (Work in Progress) | Versión: 0.1.0

Este proyecto es una implementación práctica de una arquitectura de Debate Multi-Agente (Multi-Agent Debate) aplicada al análisis financiero fundamental. El objetivo es orquestar múltiples Modelos de Lenguaje (LLMs) para simular un comité de expertos financieros, reduciendo alucinaciones y sesgos mediante un mecanismo de consenso y un "Juez" final.

📋 Tabla de Contenidos
Sobre el Proyecto

Arquitectura del Flujo

Funcionalidades Actuales

Stack Tecnológico

Roadmap (Próximos Pasos)

Instalación y Uso

💡 Sobre el Proyecto
Como desarrollador explorando el mundo de los Agentes de IA, creé este sistema para resolver un problema complejo: ¿Cómo obtener un análisis financiero confiable combinando la capacidad de cálculo de Python con la capacidad de razonamiento de las IAs?

El sistema no depende de una sola opinión. Extrae datos reales de mercado, los procesa matemáticamente y (en fases futuras) los somete a votación entre 5 modelos de IA distintos, donde un "Juez" emite el veredicto final.

🔄 Arquitectura del Flujo
El sistema sigue una pipeline lineal de datos:

Ingesta de Datos (Data Ingestion): Conexión a Yahoo Finance para obtener Balances y Estados de Resultados de los últimos 5 años.

Procesamiento (Hard Skills): Cálculo determinista de ratios financieros (Python puro). Las IAs no calculan, solo analizan.

El Comité (Multi-Agent Layer - En proceso): 5 Modelos (Gemini, GPT, DeepSeek, Llama, etc.) reciben el JSON procesado.

El Juez (Consensus Mechanism - En proceso): Sintetiza los votos y genera un informe de riesgos.

Visualización (Frontend): Interfaz de usuario construida en Flet.

✅ Funcionalidades Actuales
Lo que ya está construido y operativo en este repositorio:

Extracción Histórica Robusta: Script optimizado para obtener datos financieros de hasta 4-5 años usando yfinance.

Limpieza de Datos: Manejo de valores nulos (NaN), ceros y formatos inconsistentes de la API.

Cálculo de Ratios Financieros:

Solvencia: Razón Corriente, Test Ácido.

Estructura de Capital: Endeudamiento, Patrimonio.

Valoración: Valor Libro por Acción.

Eficiencia: Capital de Trabajo.

Exportación Estructurada: Generación automática de salidas en formato JSON limpio, diseñado específicamente para optimizar el contexto de los LLMs (Prompt Engineering).

🛠 Stack Tecnológico
Lenguaje:

Gestión de Paquetes: uv (para una gestión de dependencias ultrarrápida).

Librerías de Datos: yfinance, pandas, json.

Interfaz (Futuro): Flet (Flutter para Python).

Integración IA (Futuro): APIs de OpenAI, Google Gemini, Groq, DeepSeek.

🚀 Roadmap (Próximos Pasos)
[x] Fase 1: Script de extracción y cálculo financiero (Completado).

[ ] Fase 2: Conexión a APIs de LLMs (Gemini, OpenAI, Groq).

[ ] Fase 3: Implementación de la lógica del "Juez" (Prompt del Sistema y conteo de votos).

[ ] Fase 4: Desarrollo de la UI con Flet para visualizar gráficos y veredictos.

[ ] Fase 5: Deploy y documentación final.

💻 Instalación y Uso
Primero, clona el repositorio:

Bash
git clone https://github.com/TU_USUARIO/investment-committee-ai.git
cd investment-committee-ai
Opción A: Instalación Moderna con uv (Recomendada ⚡)
Este proyecto utiliza uv para una gestión de entorno virtual y dependencias extremadamente rápida.

Crea el entorno virtual:

Bash
uv venv
Activa el entorno e instala las dependencias:

Bash
# En Windows
.venv\Scripts\activate
uv pip install yfinance pandas flet

# En Mac/Linux
source .venv/bin/activate
uv pip install yfinance pandas flet
Opción B: Instalación Clásica con pip
Si prefieres el método estándar:

Crea un entorno virtual (opcional pero recomendado):

Bash
python -m venv venv
source venv/bin/activate  # O venv\Scripts\activate en Windows
Instala las librerías:

Bash
pip install yfinance pandas flet
Ejecutar el Script
Para ver la extracción de datos en acción:

Bash
python main.py
📊 Ejemplo de Salida (JSON)
El sistema genera un contexto limpio para las IAs como este:

JSON
{
    "2023": {
        "Empresa": "AAPL",
        "Razón Corriente": 0.99,
        "Capital de Trabajo": "$-1,500.00M",
        "Endeudamiento": 0.82
    },
    "2022": {
        "Empresa": "AAPL",
        "Razón Corriente": 0.88,
        "Endeudamiento": 0.80
    }
}

Disclaimer: Este proyecto es con fines educativos y de portafolio. No constituye asesoramiento financiero real.
