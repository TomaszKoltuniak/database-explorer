from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, privileges):
        self.id = id_
        self.name = name
        self.email = email
        self.privileges = privileges

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], privileges=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, privileges):
        db = get_db()
        db.execute(
            "INSERT INTO users (id, name, email, privileges) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, privileges),
        )
        db.commit()