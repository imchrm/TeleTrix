""" User model for database operations """

class UserModel:
    def __init__(self, db, DATABASE_URL: str):
        DATABASE_URL = DATABASE_URL
        self.db = db

    def create(self, user):
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id"
        cursor = self.db.cursor()
        cursor.execute(query, (user.name, user.email, user.password))
        user_id = cursor.fetchone()[0]
        self.db.commit()
        cursor.close()
        return user_id

    def get(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def get_all(self):
        query = "SELECT * FROM users"
        cursor = self.db.cursor()
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        return users

    def update(self, user):
        query = "UPDATE users SET name = %s, email = %s, password = %s WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (user.name, user.email, user.password, user.id))
        self.db.commit()
        cursor.close()
        return user

    def delete(self, user_id):
        query = "DELETE FROM users WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (user_id,))
        self.db.commit()
        cursor.close()
        return None
