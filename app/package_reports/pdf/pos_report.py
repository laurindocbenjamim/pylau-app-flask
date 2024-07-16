from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pos_report(report_name, content):
    # Create a PDF file in the 'reports' folder
    output_folder = 'reports'
    os.makedirs(output_folder, exist_ok=True)
    pdf_path = os.path.join(output_folder, f"{report_name}.pdf")

    # Generate the report content
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, "POS Report")
    c.drawString(100, 680, content)
    c.showPage()
    c.save()

    print(f"Report saved as {pdf_path}")

# Example usage
report_content = "Sales: $1000\nItems sold: 50"
generate_pos_report("daily_sales", report_content)