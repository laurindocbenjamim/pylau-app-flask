

from flask import Blueprint

bp_reports = Blueprint("reports", __name__, url_prefix="/reports")

from .pdf.first_test import bp_pdf_reports
bp_reports.register_blueprint(bp_pdf_reports)