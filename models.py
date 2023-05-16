from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    "Initiates the connection to the database"
    db.app = app
    db.init_app(app)

class User(db.Model):
    "Information for each user"

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)
    
    image_url = db.Column(db.String(50),
                          nullable=False,
                          default='https://tinyurl.com/default-pfp')

    def get_full_name(self):
        """Combines first name and last name into a single string and returns it"""

        first_name = self.first_name
        last_name = self.last_name

        return f'{first_name} {last_name}'