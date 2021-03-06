from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from database import db_session
from models import CustomReport
from reports.forms import CustomReportForm
import utils

custom_report = Blueprint('custom_report', __name__,
                          template_folder='templates')


@custom_report.route('/reports/')
def custom_report_index():
    reports = CustomReport.query.all()
    return render_template('reports/index.html', reports=reports)


@custom_report.route('/reports/show/<int:report_id>', methods=['GET', 'POST'])
def show_report(report_id):
    custom_report = CustomReport.query.get(report_id)

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    username = session.get('username', None)
    password = session.get('password', None)

    if username and password:
        csv_document = utils.get_csv_from_url(custom_report.url,
                                              username=username,
                                              password=password)

        if '<!DOCTYPE html PUBLIC' in csv_document:
            session['username'] = None
            session['password'] = None
            return render_template('reports/report.html', require_auth=True,
                                   failure=True)

        reports = utils.parse_csv(csv_document)
        return render_template('reports/report.html', reports=reports)
    else:
        return render_template('reports/report.html', require_auth=True)


@custom_report.route('/reports/create/', methods=['GET', 'POST'])
def create_report():
    form = CustomReportForm(request.form)
    if request.method == 'POST' and form.validate():
        custom_report = CustomReport()
        custom_report.name = form.name.data
        custom_report.url = utils.parse_url(form.url.data)
        custom_report.description = form.description.data

        db_session.add(custom_report)
        db_session.commit()
        return redirect(url_for('custom_report.custom_report_index'))

    return render_template('reports/create_report.html', form=form)
