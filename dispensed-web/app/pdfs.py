from xhtml2pdf import pisa
from io import StringIO

def create_pdf(pdf_data):
    pisa.CreatePDF(StringIO(pdf_data), pdf)
    return pdf
