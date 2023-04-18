import io, csv, requests
from app.models.violation import Violation

def perform_import_violations(app):
    ImportViolations(app).perform()

class ImportViolations():
    VIOLATIONS_URL = "https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/download/violations.csv"

    def __init__(self, app):
        self.app = app

    def perform(self):
        response = requests.get(self.VIOLATIONS_URL)
        response.raise_for_status()
        violations = csv.DictReader(io.StringIO(response.content.decode('utf-8')))
        with self.app.app_context():
            for violation_response in violations:
                Violation.insert_or_update_by_remote_id(
                    remote_id = violation_response['id_poursuite'],
                    business_id = violation_response['business_id'],
                    date = self._format_date(violation_response['date']),
                    description = violation_response['description'],
                    address = violation_response['adresse'],
                    judgement_date = self._format_date(violation_response['date_jugement']),
                    establishment = violation_response['etablissement'],
                    amount = violation_response['montant'],
                    owner = violation_response['proprietaire'],
                    city = violation_response['ville'],
                    status = violation_response['statut'],
                    status_date = self._format_date(violation_response['date_statut']),
                    category = violation_response['categorie']
                )
    
    def _format_date(self, date):
        return date[:4] + "-" + date[4:6] + "-" + date[6:]
 