from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    def __repr__(self):
        return "self.user"

    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    first_name = db.Column(db.String(20),nullable=False)

    last_name = db.Column(db.String(20),nullable=False)

    image_url = db.Column(db.Text,nullable=False,default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/300px-No_image_available.svg.png")
    
    def update_table(user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_at_id(cls,d_id):
        cls.query.filter_by(id=d_id).delete()
        db.session.commit()
