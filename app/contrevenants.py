from flask import Blueprint, render_template, request, Response
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
    if not request.args.get('du') and not request.args.get('au'):
        return api_response(Violation.count_by_establishment(), request.content_type)

    if not request.args.get('du') or not request.args.get('au'):
        return "Bad request", 400
    
    counts_by_establishment = Violation.count_by_establishment_between_dates(
        start_date=request.args.get('du'),
        end_date=request.args.get('au'),
    )

    content_type = request.content_type
    if content_type == 'text/html':
        return render_template('contrevenants/index.html', establishments=counts_by_establishment)
    
    return api_response(counts_by_establishment, content_type)


@bp.route('/contrevenants/search')
def search_contrevenants():
    if not request.args.get('establishment') and not request.args.get('owner') and not request.args.get('address'):
        return "Bad request", 400

    violations = Violation.search(
        establishment=request.args.get('establishment'),
        owner=request.args.get('owner'),
        address=request.args.get('address'),
    )

    content_type = request.content_type
    if content_type == 'text/html':
        return render_template('contrevenants/search_results.html', violations=violations)

    violations_dicts_list = [violation.to_dict() for violation in violations]
    return api_response(violations_dicts_list, content_type)

def api_response(violations, content_type):
    if content_type == 'application/json':
        return violations
    elif content_type == 'application/xml':
        xml = dicttoxml(violations)
        return Response(xml, content_type=content_type)
    elif content_type == 'text/csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(violations[0].keys())
        for violation in violations:
            writer.writerow([value for value in violation.values()])
        return Response(output.getvalue(), content_type=content_type)
