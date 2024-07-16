

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO

from flask import Blueprint, send_file

bp_pdf_reports = Blueprint("pdf", __name__, url_prefix="/pdf")

from .pdf_model import PdfModel
from datetime import datetime



@bp_pdf_reports.route('/gen-prod-pdf')
def products_rep():
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    data = [
        ['Product', 'Sales','Product', 'Sales'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
        ['Product 1', '1000'],
        ['Product 2', '2000'],
        ['Product 3', '1500'],
    ]

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.green),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ])
    table.setStyle(style)

    elements = [table, PageBreak()]

    """
    Approach - customize footer and header for different pages
        doc.build(elements, onFirstPage=PdfModel.draw_header_footer, onLaterPages=PdfModel.draw_header_footer)

    New code:
        doc.build(elements, onFirstPage=draw_header_footer_first_page, onLaterPages=draw_header_footer_later_pages)
    """
    doc.build(elements, onFirstPage=PdfModel.draw_header_footer_first_page, onLaterPages=PdfModel.draw_header_footer_later_pages)

    buffer.seek(0)

    """
    Approach - Solve issue
        error: send_file() got an unexpected keyword argument 'attachment_filename'
    
        return send_file(buffer, attachment_filename='report.pdf', mimetype='application/pdf')
        Updated to:
        return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')
    """

    """
    Approach - New change
     With this code just download the file asking to select the path
        return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')
    With this code the file  is opened into the browser
        return send_file(buffer, download_name='report.pdf', mimetype='application/pdf')
    """
    return send_file(buffer, download_name='report.pdf', mimetype='application/pdf')



#
def get_products():
    data = []
    data2 = []
    for i in range(50):
        data2.append({  
                'barcode': f"00{i}",
                'description': f"Arroz Agulha {i}",
                'category': "Vegetal",
                'type': "Delicados" ,   
                'detail':"product do campo",
                'brand': "",
                'measure_unit': "unit",
                'fixed_margin': "10",
                'status': True,
                'retention_font': "",
                'date_added': datetime.now().date(),
                'year_added': datetime.now().strftime('%Y'),
                'month_added': datetime.now().strftime('%m'),
                'datetime_added': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'date_updated': "",
            })
        data.append([  
                'barcode', f"00{i}",
                'description', f"Arroz Agulha {i}",
                'category', "Vegetal",
                'type', "Delicados" ,   
                'detail',"product do campo",
                'brand', "",
                'measure_unit', "unit",
                'fixed_margin', "10",
                'status', True,
                'retention_font', "",
                'date_added', datetime.now().date(),
                'year_added', datetime.now().strftime('%Y'),
                'month_added', datetime.now().strftime('%m'),
                'datetime_added', datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'date_updated', "",
            ])
    return data