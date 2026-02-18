from fpdf import FPDF
import re

class PDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.cell(0, 10, 'Comite de Inversiones - Informe Confidencial', border=False, ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def limpiar_texto(texto):
    """
    Limpia el texto de Markdown y formatea para lectura humana (quita espacios extra).
    """
    if not isinstance(texto, str):
        return str(texto)

    # Encoding
    texto = texto.encode('latin-1', 'ignore').decode('latin-1')

    # Markdown cleaning
    texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto) 
    texto = re.sub(r'#+\s*', '', texto) 
    texto = re.sub(r'[-_]{3,}', '---', texto)
    
    # Quitar indentación para texto normal 
    lineas = texto.split('\n')
    lineas_limpias = [line.strip() for line in lineas if line.strip() != ""]
    return '\n'.join(lineas_limpias)

# --- Agregamos el parámetro json_str ---
def exportar_a_pdf(simbolo, reporte_completo, veredicto_final, json_str):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    ancho_util = pdf.epw 

    # --- Título ---
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(ancho_util, 10, f"Analisis Financiero: {simbolo}", ln=True, align='L')
    pdf.ln(5)

    # --- Veredicto ---
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(230, 230, 230) 
    pdf.cell(ancho_util, 10, "VEREDICTO EJECUTIVO (CIO):", ln=True, fill=True, align='L')
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_x(pdf.l_margin) 
    veredicto_limpio = limpiar_texto(str(veredicto_final))
    pdf.multi_cell(ancho_util, 6, veredicto_limpio, align='L') 
    pdf.ln(10)

    # --- Detalles Agentes ---
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_x(pdf.l_margin)
    pdf.cell(ancho_util, 10, "Detalle de los Analistas:", ln=True)
    pdf.ln(2)

    pdf.set_font("Courier", "", 10) 
    for agente, analisis in reporte_completo:
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Courier", "B", 11)
        
        pdf.set_x(pdf.l_margin)
        pdf.cell(ancho_util, 8, f" >> Reporte: {agente}", ln=True, fill=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Courier", "", 10)
        
        texto_limpio = limpiar_texto(str(analisis))
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(ancho_util, 5, texto_limpio, align='L')
        pdf.ln(5)

    # --- ANEXO JSON ---
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(ancho_util, 10, "ANEXO: Datos Financieros Crudos (JSON)", ln=True)
    pdf.ln(5)
    
    # Configuramos fuente pequeña tipo código
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(80, 80, 80)
    
    # Tratamiento especial para el JSON:
    json_seguro = str(json_str).encode('latin-1', 'replace').decode('latin-1')
    
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(ancho_util, 4, json_seguro, align='L')

    # Guardar
    nombre_archivo = f"Reporte_{simbolo}.pdf"
    try:
        pdf.output(nombre_archivo)
        print(f"\n✅ PDF Generado exitosamente: {nombre_archivo}")
    except Exception as e:
        print(f"\n❌ Error al guardar el PDF: {e}")