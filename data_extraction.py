# Conexion a la API yfinance
import yfinance as yf
import json

#symbol = input(f"Ingrese el simbolo de la empresa a evaluar: ")
symbol = "MSFT"
def obtener_datos_historicos(ticket_symbol):
    stock = yf.Ticker(ticket_symbol)
    
    # Obtencion DF
    stock = yf.Ticker(ticket_symbol)
    info = stock.info
    balance = stock.balance_sheet
    financials = stock.financials
    
    # Verificacion de datos
    if balance.empty: 
        return None

    datos_historicos = {}

    # Iteramos por cada columna (año disponible)

    fechas_disponibles = balance.columns[:5] 
    
    for fecha in fechas_disponibles:
        year_str = fecha.strftime('%Y') # Convertimos la fecha a texto
        
        precio_actual = info.get('currentPrice')

        try:
            # Extraemos datos clave de ese año específico usando .loc[fila, columna]
            activo_corriente = balance.loc['Current Assets', fecha] if 'Current Assets' in balance.index else 0
            pasivo_corriente = balance.loc['Current Liabilities', fecha] if 'Current Liabilities' in balance.index else 0
            inventario = balance.loc['Inventory', fecha] if 'Inventory' in balance.index else 0
            total_pasivos = balance.loc['Total Liabilities Net Minority Interest', fecha] if 'Total Liabilities Net Minority Interest' in balance.index else 0
            total_activos = balance.loc['Total Assets', fecha]
            acciones_historicas = balance.loc['Ordinary Shares Number', fecha]
            # En el caso de que el nombre de la fila no la encuentre, ocupara la siguiente
            try:
                acciones_historicas = balance.loc['Ordinary Shares Number', fecha]
            except KeyError:
                try:
                    acciones_historicas = balance.loc['Share Issued', fecha]
                except KeyError:
                    acciones_historicas = 1

            # Cálculos
            patrimonio = total_activos - total_pasivos
            valor_libro = patrimonio / acciones_historicas
            capital_trabajo = activo_corriente - pasivo_corriente
            razon_corriente = activo_corriente / pasivo_corriente
            test_acido = (activo_corriente - inventario) / pasivo_corriente
            endeudamiento = total_pasivos / total_activos

            datos_historicos[year_str] = {
                "Empresa": ticket_symbol,
                "Precio": precio_actual,
                "Razón Corriente": round(razon_corriente, 2),
                "Test Ácido": round(test_acido, 2),
                "Endeudamiento": round(endeudamiento, 2),
                "Capital de Trabajo": f"${capital_trabajo/1_000_000_000:,.2f}B", # B de Billions,
                "Acciones (M)": f"{acciones_historicas/1_000_000:,.1f}M",
                "Patrimonio": f"${patrimonio:,.0f}",
                "Valor Libro": f"${valor_libro:.2f}"
            }
        except Exception as e:
            print(f"No se pudo extraer los datos del año {fecha}. \nError: {e}")
            continue

    return datos_historicos

# def mostrar_datos(symbol):
#     # Probamos con Apple
#     datos_historicos = obtener_datos_historicos(symbol)
#     primer_año = list(datos_historicos.keys())[0] 
#     nombre_empresa = datos_historicos[primer_año]["Empresa"]

#     texto_para_el_prompt = f"REPORTE FINANCIERO DE {nombre_empresa} (Últimos años):\n\n"
#     for año in sorted(datos_historicos.keys(), reverse=True):
#         datos = datos_historicos[año]
        
#         texto_para_el_prompt += f"--- AÑO {año} ---\n"
#         texto_para_el_prompt += f"- Razón Corriente: {datos['Razón Corriente']}\n"
#         texto_para_el_prompt += f"- Test Ácido: {datos['Test Ácido']}\n"
#         texto_para_el_prompt += f"- Endeudamiento: {datos['Endeudamiento']}\n"
#         texto_para_el_prompt += f"- Patrimonio: {datos['Patrimonio']}\n"
#         texto_para_el_prompt += f"- Capital de Trabajo: {datos['Capital de Trabajo']}\n"
#         texto_para_el_prompt += f"- Acciones (M): {datos['Acciones (M)']}\n"
#         texto_para_el_prompt += f"- Valor Libro: {datos['Valor Libro']}\n"
#         texto_para_el_prompt += "\n"
#     texto_para_el_prompt += f"- Precio Actual: {datos['Precio']}\n"

#     print(texto_para_el_prompt)

def exportar_datos_json(symbol):
    datos = obtener_datos_historicos(symbol)
    
    if not datos:
        print(f"No se encontraron datos para {symbol}")
        return

    # Transofrmar datos a JSON
    json_str = json.dumps(datos, indent=4, ensure_ascii=False)
    
    print(f"--- JSON GENERADO PARA {symbol} ---")

    # Guardar archivo formato JSON
    nombre_archivo = f"{symbol}_financiero.json"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    print(f"\n✅ Archivo guardado exitosamente: {nombre_archivo}")

exportar_datos_json(symbol)
# mostrar_datos(symbol)