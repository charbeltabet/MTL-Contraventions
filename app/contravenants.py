from flask import Blueprint, render_template, request, jsonify
from app.models.violation import Violation

bp = Blueprint('contravenants', __name__, url_prefix='/contravenants')

@bp.route('/')
def get_contravenants():
    if (request.args.get('establishment') or
        (request.args.get('owner')) or
        (request.args.get('address'))):
        violations = Violation.search(
            establishment=request.args.get('establishment'),
            owner=request.args.get('owner'),
            address=request.args.get('address'),
        )
        if (request.content_type == 'application/json'):
            return [violation.to_dict() for violation in violations]
        return render_template('contravenants/search_results.html', violations=violations)
    elif (request.args.get('du') and
          (request.args.get('au'))):
        return Violation.search_between_dates(
            start_date=request.args.get('du'),
            end_date=request.args.get('au'),
        )
    else:
        return render_template('contravenants/index.html', establishments=Violation.all_establishments())
