from flask import Blueprint
from flask import render_template

from models import CustomReport

custom_report = Blueprint('custom_report', __name__, template_folder='templates')


@custom_report.route('/reports/')
def custom_report_index():
    reports = CustomReport.query.all()
    return render_template('reports/index.html', reports=reports)
