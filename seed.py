from app import app
from models import db,User

db.drop_all()
db.create_all()

user_list = [(User(first_name="John",last_name="Ralfert")),(User(first_name="Albert",last_name="Syanasue")),(User(first_name="Rafael",last_name="Suso"))]

db.session.add_all(user_list)

db.session.commit()