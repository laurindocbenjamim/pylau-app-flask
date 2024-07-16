
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO

class PdfModel(object):

    def draw_header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # Header
        header_text = "Sales Report"
        canvas.setFont('Helvetica-Bold', 18)  # Set the font size to 18
        canvas.drawString(200, 770, header_text)

        # Footer
        footer_text = "Page %s" % doc.page
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(500, 20, footer_text)

        # Release the canvas
        canvas.restoreState()

    
    def draw_header_footer_first_page(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # Header
        header_text = "Sales Report"
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(200, 770, header_text)

        # Footer for the first page
        footer_text = "First Page - %s" % doc.page
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(500, 20, footer_text)

        # Release the canvas
        canvas.restoreState()

    def draw_header_footer_later_pages(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()

        # Header
        header_text = "Sales Report - Continue"
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(200, 770, header_text)

        # Footer for the subsequent pages
        footer_text = "Subsequent Page - %s" % doc.page
        canvas.setFont('Times-Roman', 10)
        canvas.drawString(500, 20, footer_text)

        # Release the canvas
        canvas.restoreState()
