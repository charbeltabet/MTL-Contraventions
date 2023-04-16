from app.models.violation import Violation

def test_insert(app):
    with app.app_context():
        violation = Violation(
            remote_id=2,
            business_id=1,
            date='2019-01-01',
            description='description',
            address='address',
            judgement_date='2019-01-01',
            establishment='establishment',
            amount=1.0,
            owner='owner',
            city='city',
            status='status',
            status_date='2019-01-01',
            category='category'
        )
        violation.insert()
        assert violation.id is not None
        assert Violation.find_by_id(violation.id).to_dict() is not None
        assert violation.remote_id == 2
        assert violation.business_id == 1
        assert violation.date == '2019-01-01'
        assert violation.description == 'description'
        assert violation.address == 'address'
        assert violation.judgement_date == '2019-01-01'
        assert violation.establishment == 'establishment'
        assert violation.amount == 1.0
        assert violation.owner == 'owner'
        assert violation.city == 'city'
        assert violation.status == 'status'
        assert violation.status_date == '2019-01-01'
        assert violation.category == 'category'

def test_find_by_id(app):
    with app.app_context():
        violation = Violation(
            remote_id=2,
            business_id=1,
            date='2019-01-01',
            description='description',
            address='address',
            judgement_date='2019-01-01',
            establishment='establishment',
            amount=1.0,
            owner='owner',
            city='city',
            status='status',
            status_date='2019-01-01',
            category='category'
        )
        violation.insert()
        assert Violation.find_by_id(violation.id) is not None
