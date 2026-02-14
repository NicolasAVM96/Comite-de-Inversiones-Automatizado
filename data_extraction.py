# Conexion a la API yfinance
import yfinance as yf
import json
import math

#symbol = input(f"Ingrese el simbolo de la empresa a evaluar: ")
symbol = "TSLA"

def verificador_datos(val):
    return val if isinstance(val, (int, float)) and not math.isnan(val) else 0

def obtener_datos_historicos(ticket_symbol):
    stock = yf.Ticker(ticket_symbol)
    
    # Obtencion DF
    info = stock.info
    balance = stock.balance_sheet
    financials = stock.financials
    cashflow = stock.cashflow
    
    # Verificacion de datos
    if balance.empty: 
        return None

    peg_ratio = info.get('pegRatio')
    forward_pe = info.get('forwardPE')
    trailing_pe = info.get('trailingPE')
    revenue_growth = info.get('revenueGrowth')
    earnings_growth = info.get('earningsGrowth')
    
    datos_empresa = {
        "perfil general": {
            "Empresa": ticket_symbol,
            "Sector": info.get('sector'),      
            "Industria": info.get('industry'), 
            "Pais": info.get('country'),
            "Precio Actual": info.get('currentPrice'),
        },
        "metricas futuras": {
            "PEG Ratio": peg_ratio, 
            "Forward PE": forward_pe, 
            "Trailing PE": trailing_pe,
            "Beta_Riesgo": info.get('beta'), 
            "Dividend Yield": info.get('dividendYield'),
            "Recomendacion de Analistas": info.get('recommendationKey'),
            "Crecimiento de Ventas Trimestral": revenue_growth, 
            "Crecimiento de Ganancias Trimestral": earnings_growth
        },
        "historico": {}
    }

    # Iteramos por cada columna de año (yfinance solo permite los 4 ultimos años)
    fechas_disponibles = balance.columns[:4] 
   
    for fecha in fechas_disponibles:
        year_str = fecha.strftime('%Y') # Convertimos la fecha a texto
        
        try:
            # Extraccion de datos
            activo_corriente = verificador_datos(balance.loc['Current Assets', fecha] if 'Current Assets' in balance.index else 0)
            pasivo_corriente = verificador_datos(balance.loc['Current Liabilities', fecha] if 'Current Liabilities' in balance.index else 0)
            inventario = verificador_datos(balance.loc['Inventory', fecha] if 'Inventory' in balance.index else 0)
            total_pasivos = verificador_datos(balance.loc['Total Liabilities Net Minority Interest', fecha] if 'Total Liabilities Net Minority Interest' in balance.index else 0)
            total_activos = verificador_datos(balance.loc['Total Assets', fecha] if 'Total Assets' in balance.index else 0)
            ingresos = verificador_datos(financials.loc['Total Revenue', fecha] if 'Total Revenue' in financials.index else 0)
            utilidad = verificador_datos(financials.loc['Net Income', fecha] if 'Net Income' in financials.index else 0) # Free Cash Flow
            fcf = verificador_datos(cashflow.loc['Free Cash Flow', fecha]) if 'Free Cash Flow' in cashflow.index else 0
            # # En el caso de que el nombre de la fila de acciones no la encuentre, ocupara el siguiente nombre
            try:
                acciones_historicas = verificador_datos(balance.loc['Ordinary Shares Number', fecha])
            except KeyError:
                try:
                    acciones_historicas = verificador_datos(balance.loc['Share Issued', fecha])
                except KeyError:
                    acciones_historicas = 1
            eps = utilidad / acciones_historicas if acciones_historicas > 0 else 0 # Beneficio por Acción

            patrimonio = total_activos - total_pasivos 
            valor_libro = patrimonio / acciones_historicas if acciones_historicas > 0 else 0
            capital_trabajo = activo_corriente - pasivo_corriente
            razon_corriente = activo_corriente / pasivo_corriente if pasivo_corriente > 0 else 0
            test_acido = (activo_corriente - inventario) / pasivo_corriente if pasivo_corriente > 0 else 0
            endeudamiento = total_pasivos / total_activos if total_activos > 0 else 0
            margen_neto = (utilidad / ingresos) * 100 if ingresos > 0 else 0
            roe = (utilidad / patrimonio) * 100 if patrimonio > 0 else 0 # Rentabilidad sobre Patrimonio

            datos_empresa["historico"][year_str] = {
                # Solvencia
                "Razón Corriente": round(razon_corriente, 2),
                "Test Ácido": round(test_acido, 2),
                "Endeudamiento": round(endeudamiento, 2),
                "Capital de Trabajo": capital_trabajo, 
                # Rentabilidad/Eficiencia
                "Ventas Totales": ingresos,    
                "Utilidad Neta": utilidad,   
                "Free Cash Flow" : fcf,
                "REO (%)" : round(roe),            
                "Margen Neto (%)": round(margen_neto, 2), 
                # Valoracion
                "EPS (Beneficio/Acción)": round(eps, 2),
                "Acciones (M)": acciones_historicas,
                "Patrimonio": patrimonio,
                "Valor Libro": round(valor_libro, 2)
            }
        except Exception as e:
            print(f"No se pudo extraer los datos del año {fecha}. \nError: {e}")
            continue

    return datos_empresa

def exportar_datos_json(symbol):
    datos = obtener_datos_historicos(symbol)
    
    if not datos:
        print(f"No se encontraron datos para {symbol}")
        return

    # Transformar datos a JSON
    json_str = json.dumps(datos, indent=4, ensure_ascii=False)
    
    print(f"--- JSON GENERADO PARA {symbol} ---")

    # Guardar archivo formato JSON
    nombre_archivo = f"{symbol}_financiero.json"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    print(f"\n✅ Archivo guardado exitosamente: {nombre_archivo}")

exportar_datos_json(symbol)