from fpdf import FPDF
import base64

class PDFReport(FPDF):
    """
    Custom PDF class for travel reports.
    """
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Autonomous Travel Plan', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text_content):
    """
    Creates a PDF report from the given text content.
    
    Args:
        text_content (str): The text to include in the PDF.
    
    Returns:
        str: The file path of the generated PDF.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Latin-1 encoding to handle basic accents
    content = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, content)
    
    file_path = "travel_result.pdf"
    pdf.output(file_path)
    return file_path

def get_pdf_download_link(file_path):
    """
    Generates an HTML download link for the PDF file.
    
    Args:
        file_path (str): The path to the PDF file.
    
    Returns:
        str: The HTML string for the download link.
    """
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="My_Travel.pdf" style="text-decoration:none; background-color:#FF4B4B; color:white; padding:10px 20px; border-radius:5px; font-weight:bold;"> Download PDF</a>'