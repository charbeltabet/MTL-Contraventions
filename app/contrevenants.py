from flask import Blueprint, render_template, request, Response, jsonify
from app.models.violation import Violation
from dicttoxml import dicttoxml
import csv, io

bp = Blueprint('contrevenants', __name__, url_prefix='/')

@bp.route('/doc')
def doc():
    return render_template('contrevenants/doc.html')

@bp.route('/')
def index():
    return render_template('contrevenants/index.html', establishments=Violation.all_establishments())

@bp.route('/contrevenants')
def get_contrevenants():
    if request.args.get('du') and request.args.get('au'):
        return violations_response(Violation.count_by_establishment_between_dates(
            start_date=request.args.get('du'),
            end_date=request.args.get('au'),
        ), request.content_type)
    elif not request.args.get('du') and not request.args.get('au'):
        return Violation.count_by_establishment()
    return "Bad request", 400

@bp.route('/contrevenants/search')
def search_contrevenants():
    if not request.args.get('establishment') and not request.args.get('owner') and not request.args.get('address'):
        return "Bad request", 400

    violations = Violation.search(
        establishment=request.args.get('establishment'),
        owner=request.args.get('owner'),
        address=request.args.get('address'),
    )
    if (request.content_type == 'application/json'):
        return [violation.to_dict() for violation in violations]
    return render_template('contrevenants/search_results.html', violations=violations)

def violations_response(violations, content_type):
    if content_type == 'application/json':
        return violations
    elif content_type == 'application/xml':
        xml = dicttoxml([violation.to_dict() for violation in violations])
        return Response(xml, content_type='application/xml')
    elif content_type == 'text/csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Establishment', 'Violation Count'])
        for violation in violations:
            writer.writerow([violation.establishment, violation.violation_count])
        return Response(output.getvalue(), content_type='text/csv')