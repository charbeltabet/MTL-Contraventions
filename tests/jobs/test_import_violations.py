from app.jobs.import_violations import ImportViolations
from app.models.violation import Violation

def test_import_violations(app):
    with app.app_context():
        initial_count = Violation.count() 
        ImportViolations().perform()
        count_after_import = Violation.count()
        assert count_after_import > initial_count
