from flask import Flask,render_template,redirect,request,flash
from models import connect_db,User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testing_users'
app.config['SECRET_KEY'] = "secret1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def users_page():
    all_users = User.query.all()

    return render_template('users.html',all_users=all_users)

@app.route('/users/new',methods=['POST','GET'])
def new_user_page():
    if request.method=='POST':
        first_name = request.form['firstNameInput'] if request.form['firstNameInput'] != "" else None
        last_name = request.form['lastNameInput'] if request.form['lastNameInput'] != "" else None
        try:
            User.update_table(user=User(first_name= first_name,last_name= last_name))
        except:
            flash('Error Adding User, Please Try Again')
        return redirect('/')
    if request.method=='GET':
        return render_template('new_user.html')  

@app.route('/users/<user_id>')
def user_page(user_id):
    user = User.query.get(user_id)
    return render_template('user_detail.html',user=user)

@app.route('/users/<user_id>/edit',methods=['POST','GET'])
def edit_user_page(user_id):
    
    user = User.query.get(user_id)
    if request.method=='POST':
        first_name = request.form['firstNameInput'] if request.form['firstNameInput'] != "" else None
        last_name = request.form['lastNameInput'] if request.form['lastNameInput'] != "" else None
        image_url = request.form['imgUrl'] if request.form['imgUrl'] != "" else user.image_url

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.image_url = image_url
            User.update_table(user=user)
        except:
            flash('Error Editing User, Please Try Again')
        return redirect(f'/users/{user_id}')
    if request.method=='GET':
        return render_template('edit_user.html',user=user)

@app.route('/users/<user_id>/delete',methods=['POST'])
def delete_user_page(user_id):
    User.delete_at_id(user_id)
    return redirect('/')
