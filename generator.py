from fpdf import FPDF

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for section, content in data.items():
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(200, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=12)
        for key, value in content.items():
            pdf.multi_cell(0, 10, f"{key}: {value}")
        pdf.ln(5)
    
    return pdf.output(dest='S').encode('latin1')
