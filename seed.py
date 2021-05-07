from app import app
from models import Post, db,User

db.drop_all()
db.create_all()

user_list = [(User(first_name="John",last_name="Ralfert")),(User(first_name="Albert",last_name="Syanasue")),(User(first_name="Rafael",last_name="Suso"))]
post_list = [Post(title="first post",content="This is my first post",user_id=1),Post(title="second post",content="This is my second post",user_id=1),Post(title="chicken post",content="chicken is great",user_id=2)]
db.session.add_all(user_list)
db.session.add_all(post_list)
db.session.commit()