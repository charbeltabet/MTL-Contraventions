from app.db import get_db
from flask_login import UserMixin
import bcrypt

class User(UserMixin):
  def __init__(self, full_name, email, salt=None, hashed_password=None, id=None):
    self.id = id
    self.full_name = full_name
    self.email = email
    self.salt = salt
    self.hashed_password = hashed_password
  
  def insert(self):
    db = get_db()
    cursor = db.execute(
      """
      INSERT INTO users (
        full_name,
        email,
        salt,
        hashed_password
      ) VALUES (?, ?, ?, ?)
      RETURNING *
      """,
      (
        self.full_name,
        self.email,
        self.salt,
        self.hashed_password
      )
    )
    self.id = cursor.lastrowid
    cursor.close()
    db.commit()
    return self
  
  def register(self, password):
    self.set_password(password)
    return self.insert()
  
  def set_password(self, password):
    self.salt = bcrypt.gensalt()
    self.hashed_password = bcrypt.hashpw(password.encode(), self.salt)

  def verify_password(self, password):
    return bcrypt.hashpw(password.encode(), self.salt) == self.hashed_password
  
  @classmethod
  def get_by_email_and_password(cls, email, password):
    db = get_db()
    cursor = db.execute(
      """
      SELECT * FROM users WHERE email = ?
      """,
      (email,)
    )
    user = cursor.fetchone()
    cursor.close()
    if user:
      user = cls(**user)
      if user.verify_password(password):
        return user
    return None
  
  @classmethod
  def find_by_id(cls, id):
    db = get_db()
    cursor = db.execute(
      """
      SELECT * FROM users WHERE id = ?
      """,
      (id,)
    )
    user = cursor.fetchone()
    cursor.close()
    if user:
      return cls(**user)
    return None
  
  def to_dict(self):
    return {
      'full_name': self.full_name,
      'email': self.email
    }
