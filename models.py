from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    def __repr__(self):
        return self.first_name

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
        return self.title

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.String(30),nullable=False)

    content = db.Column(db.Text,nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def update_table(user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_at_id(cls,d_id):
        cls.query.filter_by(id=d_id).delete()
        db.session.commit()

class PostTag(db.Model):
    __tablename__ = "posttag"

    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'),primary_key=True,nullable=False)
    
    tag_id = db.Column(db.Integer,db.ForeignKey('tags.id'),primary_key=True,nullable =False)

class Tag(db.Model):
    def __repr__(self):
        return self.name

    __tablename__='tags'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    name = db.Column(db.String(50),unique=True)

    posts = db.relationship('Post',secondary="posttag",backref=('tags'))

