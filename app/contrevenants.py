from flask import Blueprint, render_template, request, jsonify
from app.models.violation import Violation

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
        return Violation.count_by_establishment_between_dates(
            start_date=request.args.get('du'),
            end_date=request.args.get('au'),
        )
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
