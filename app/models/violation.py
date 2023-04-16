from app.db import get_db

class Violation(object):
    def __init__(self, remote_id, business_id, date, description, address, judgement_date, establishment, amount, owner, city, status, status_date, category, id=None):
        self.id = id
        self.remote_id = remote_id
        self.business_id = business_id
        self.date = date
        self.description = description
        self.address = address
        self.judgement_date = judgement_date
        self.establishment = establishment
        self.amount = amount
        self.owner = owner
        self.city = city
        self.status = status
        self.status_date = status_date
        self.category = category
    
    def save(self):
        if self.id is None:
            return self.insert()
        else:
            return self.update()
    
    def insert(self):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO violations (
                remote_id,
                business_id,
                date,
                description,
                address,
                judgement_date,
                establishment,
                amount,
                owner,
                city,
                status,
                status_date,
                category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                self.business_id,
                self.remote_id,
                self.date,
                self.description,
                self.address,
                self.judgement_date,
                self.establishment,
                self.amount,
                self.owner,
                self.city,
                self.status,
                self.status_date,
                self.category
            )
        )
        self.id = cursor.lastrowid
        cursor.close()
        db.commit()
        return self

    def update(self):
        db = get_db()
        cursor = db.execute(
            """
            UPDATE violations SET
                remote_id = ?,
                business_id = ?,
                date = ?,
                description = ?,
                address = ?,
                judgement_date = ?,
                establishment = ?,
                amount = ?,
                owner = ?,
                city = ?,
                status = ?,
                status_date = ?,
                category = ?
            WHERE id = ?
            """,
            (
                self.business_id,
                self.remote_id,
                self.date,
                self.description,
                self.address,
                self.judgement_date,
                self.establishment,
                self.amount,
                self.owner,
                self.city,
                self.status,
                self.status_date,
                self.category,
                self.id
            )
        )
        cursor.close()
        db.commit()
        return self
    
    @classmethod
    def find_by_id(cls, id):
        db = get_db()
        cursor = db.execute(
            """
            SELECT * FROM violations
            WHERE id = ?
            """,
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        violation =  Violation(
            id = row['id'],
            remote_id=row['remote_id'],
            business_id=row['business_id'],
            date=row['date'],
            description=row['description'],
            address=row['address'],
            judgement_date=row['judgement_date'],
            establishment=row['establishment'],
            amount=row['amount'],
            owner=row['owner'],
            city=row['city'],
            status=row['status'],
            status_date=row['status_date'],
            category=row['category']
        )
        return violation
      
    @classmethod
    def all(self):
        db = get_db()
        cursor = db.execute(
            """
                SELECT * FROM violations
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return [self.from_row(row) for row in rows]

    @classmethod
    def count(self):
        db = get_db()
        cursor = db.execute(
            """
                SELECT COUNT(*) FROM violations
            """
        )
        count = cursor.fetchone()
        cursor.close()
        return count[0]

    def to_dict(self):
        return {
          'id': self.id,
          'remote_id': self.remote_id,
          'business_id': self.business_id,
          'date': self.date,
          'description': self.description,
          'address': self.address,
          'judgement_date': self.judgement_date,
          'establishment': self.establishment,
          'amount': self.amount,
          'owner': self.owner,
          'city': self.city,
          'status': self.status,
          'status_date': self.status_date,
          'category': self.category
        }
    
    @classmethod
    def from_row(cls, row):
        return cls(
            id = row['id'],
            remote_id=row['remote_id'],
            business_id=row['business_id'],
            date=row['date'],
            description=row['description'],
            address=row['address'],
            judgement_date=row['judgement_date'],
            establishment=row['establishment'],
            amount=row['amount'],
            owner=row['owner'],
            city=row['city'],
            status=row['status'],
            status_date=row['status_date'],
            category=row['category']
        )
 