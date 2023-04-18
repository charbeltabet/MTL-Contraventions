from app.db import get_db
from datetime import datetime

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
                self.remote_id,
                self.business_id,
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

    @classmethod
    def find_by_remote_id(cls, remote_id):
        db = get_db()
        cursor = db.execute(
            """
            SELECT * FROM violations
            WHERE remote_id = ?
            """,
            (remote_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        return cls.from_row(row)

    @classmethod
    def update_by_remote_id(cls, **kwargs):
        db = get_db()
        cursor = db.execute(
            """
            UPDATE violations SET
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
            WHERE remote_id = ?
            RETURNING *
            """,
            (
                kwargs['business_id'],
                kwargs['date'],
                kwargs['description'],
                kwargs['address'],
                kwargs['judgement_date'],
                kwargs['establishment'],
                kwargs['amount'],
                kwargs['owner'],
                kwargs['city'],
                kwargs['status'],
                kwargs['status_date'],
                kwargs['category'],
                kwargs['remote_id'],
            )
        )
        row = cursor.fetchone()
        cursor.close()
        db.commit()
        return cls.from_row(row)
    
    @classmethod
    def insert_or_update_by_remote_id(cls, **kwargs):
        violation = cls.find_by_remote_id(kwargs['remote_id'])
        if violation is None:
            return cls(**kwargs).insert()

        if (
            violation.business_id != kwargs['business_id'] or
            violation.date != kwargs['date'] or
            violation.description != kwargs['description'] or
            violation.address != kwargs['address'] or
            violation.judgement_date != kwargs['judgement_date'] or
            violation.establishment != kwargs['establishment'] or
            violation.amount != kwargs['amount'] or
            violation.owner != kwargs['owner'] or
            violation.city != kwargs['city'] or
            violation.status != kwargs['status'] or
            violation.status_date != kwargs['status_date'] or
            violation.category != kwargs['category']
        ):
            return cls.update_by_remote_id(**kwargs)

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
    def all_establishments(cls):
        db = get_db()
        cursor = db.execute(
            """
                SELECT distinct(establishment) FROM violations
                ORDER BY establishment
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        return [row[0] for row in rows]

    @classmethod
    def search(cls, **kwargs):
        stripped_kwargs = {k: str(v).strip() for k, v in kwargs.items() if v and str(v).strip()}
        if not stripped_kwargs:
            return []

        db = get_db()
        cursor = db.execute(
            "SELECT * FROM violations WHERE " + " OR ".join([f"{k} LIKE ?" for k in stripped_kwargs.keys()]),
            tuple(f"%{v}%" for v in stripped_kwargs.values())
        )
        results = cursor.fetchall()
        cursor.close()
        return [cls.from_row(row) for row in results]

    @classmethod
    def count_by_establishment_between_dates(cls, start_date, end_date):
        if start_date > end_date:
            return []
        db = get_db()
        cursor = db.execute(
            """
                SELECT establishment, count(*) AS violations_count FROM violations
                WHERE date BETWEEN ? AND ?
                GROUP BY establishment
                ORDER BY count(*) DESC
            """,
            (start_date, end_date)
        )
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return results
    
    @classmethod
    def count_by_establishment(cls):
        db = get_db()
        cursor = db.execute(
            """
                SELECT establishment, count(*) AS violations_count FROM violations
                GROUP BY establishment
                ORDER BY count(*) DESC
            """
        )
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return results

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
            date=row['date'].strftime("%d-%m-%Y"),
            description=row['description'],
            address=row['address'],
            judgement_date=row['judgement_date'].strftime("%d-%m-%Y"),
            establishment=row['establishment'],
            amount=row['amount'],
            owner=row['owner'],
            city=row['city'],
            status=row['status'],
            status_date=row['status_date'].strftime("%d-%m-%Y"),
            category=row['category']
        )
 