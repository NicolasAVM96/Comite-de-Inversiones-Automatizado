from dotenv import load_dotenv
from data_extraction import obtener_datos_json
from crew import comite
from pdf_export import exportar_a_pdf

# Cargar claves del archivo .env
load_dotenv(override=True)

if __name__ == "__main__":
    symbol = input("\nIngrese el símbolo de la empresa (ej: TSLA, AAPL, NVDA): ").upper()
    
    # Obtencion de datos
    json_string = obtener_datos_json(symbol)
    
    if json_string:       
        print(f"\n🚀 Iniciando análisis de {symbol} con IA Multi-Agente...")
        
        # Se le entrega el Json al comite
        veredicto_final = comite.kickoff(inputs={'json_datos': json_string})
        
        print("\n\n################################################")
        print(f"## ⚖️ VEREDICTO FINAL PARA {symbol} ##")
        print("################################################\n")
        print(veredicto_final)
    else:
        print("❌ Error: No se encontraron datos. Verifica el ticker.")

    lista_reportes = []
    
    # Mapeo manual para que se vea bonito en el PDF
    nombres_agentes = [
        "Analista Quant (Ratios)", 
        "Visionario (Estrategia)", 
        "Trader (Timing)", 
        "Auditor (Riesgos)", 
        "Secretario (Resumen)", 
        "Juez CIO (Veredicto)"
    ]

    for i, tarea in enumerate(comite.tasks):
        # Evitamos índice fuera de rango si hay más tareas que nombres
        nombre = nombres_agentes[i] if i < len(nombres_agentes) else f"Agente {i+1}"
        
        # Extraemos el output de la tarea
        contenido = tarea.output 
        lista_reportes.append((nombre, contenido))

    # Llamamos a la función del PDF
    exportar_a_pdf(symbol, lista_reportes, veredicto_final, json_string)

