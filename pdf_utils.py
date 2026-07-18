import re
from fpdf import FPDF

def generate_pdf_bytes(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    
    # Header styling
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(180, 10, "DoDo Business System Blueprint", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(180, 5, "Personalized Workflow, Tools, and Execution Roadmap", ln=True, align='C')
    pdf.ln(8)
    
    # Body styling
    pdf.set_font("Arial", size=10)
    
    # Filter out the raw checklist data from showing up in the clean PDF print
    blueprint_text = text.split("--- CHECKLIST_START ---")[0].strip()
    
    lines = blueprint_text.split('\n')
    for line in lines:
        clean_line = re.sub(r'\*\*', '', line).strip()
        
        if clean_line in ["---", "___"]:
            pdf.ln(2)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(4)
        elif len(clean_line) == 0:
            pdf.ln(3)
        else:
            if clean_line.startswith('#'):
                pdf.set_font("Arial", 'B', 12)
                clean_line = clean_line.lstrip('#').strip()
                pdf.multi_cell(180, 6, txt=clean_line, align='L')
                pdf.set_font("Arial", size=10)
            else:
                pdf.multi_cell(180, 5.5, txt=clean_line, align='L')
                
    return pdf.output(dest='S').encode('latin-1')