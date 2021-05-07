from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import backref
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    def __repr__(self):
        return f"{self.first_name}"

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

    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    def __repr__(self):
        return f"{self.title}"

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.String(30),nullable=False)

    content = db.Column(db.Text,nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

