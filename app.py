from flask import Flask,render_template,redirect,request,flash
from models import Post, connect_db,User,db,Tag
from flask_debugtoolbar import DebugToolbarExtension
from res.Tools import empty_to_default

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

#USERS

@app.route('/users')
def users_page():
    all_users = User.query.all()
    print(all_users[0].first_name)
    return render_template('users.html',all_users=all_users)

@app.route('/users/new',methods=['POST','GET'])
def new_user_page():
    if request.method=='POST':
        first_name = empty_to_default(request.form['firstNameInput'],None)
        last_name = empty_to_default(request.form['lastNameInput'],None)
        try:
            User.update_table(user=User(first_name= first_name,last_name= last_name))
            return redirect('/')
        except:
            flash('Error Adding User, Please Try Again')
            return redirect('/users/new')
        
    if request.method=='GET':
        return render_template('new_user.html')  

@app.route('/users/<user_id>')
def user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html',user=user)

@app.route('/users/<user_id>/edit',methods=['POST','GET'])
def edit_user_page(user_id):
    
    user = User.query.get_or_404(user_id)
    if request.method=='POST':
        try:
            user.first_name = empty_to_default(request.form['firstNameInput'],None)
            user.last_name = empty_to_default(request.form['lastNameInput'],None)
            user.image_url = empty_to_default(request.form['imgUrl'],user.image_url)

            User.update_table(user=user)
            return redirect(f'/users/{user.id}')
        except:
            db.session.rollback()
            flash('Error Editing User, Please Try Again')
            return redirect(f'/users/{user.id}/edit')
    if request.method=='GET':
        return render_template('edit_user.html',user=user)

@app.route('/users/<user_id>/delete',methods=['POST'])
def delete_user_page(user_id):
    User.delete_at_id(user_id)
    return redirect('/')

@app.route('/users/<user_id>/posts/new',methods=['GET','POST'])
def new_post_page(user_id):
    user = User.query.get_or_404(user_id)
    if request.method=='POST':
        title = empty_to_default(request.form['titleInput'],None)
        content = empty_to_default(request.form['contentInput'],None)
        try:
            Post.update_table(Post(title=title,content=content,user_id=user.id))
            return redirect(f'/users/{user.id}')
        except:
            db.session.rollback()
            flash('Invalid Input')
            return redirect(f'/users/{user.id}/posts/new')
    if request.method=='GET':
        return render_template('new_post.html',user=user)

#POSTS

@app.route('/posts/<post_id>')
def posts_page(post_id):
    post = Post.query.get(post_id)
    return render_template('posts.html',post=post)

@app.route('/posts/<post_id>/edit',methods=['POST','GET'])
def edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    all_tags = Tag.query.all()
    if request.method=='POST':
        for tag in all_tags:
            if request.form.get(f'tag-{tag.name}'):
                if tag not in post.tags:
                    post.tags.append(tag)
                    db.session.add(post)
                    db.session.commit()
            else:
                if tag in post.tags:
                    post.tags.remove(tag)
        try:
            post.title = empty_to_default(request.form['titleInput'],None)
            post.content = empty_to_default(request.form['contentInput'],None)
            db.session.add(post)
            db.session.commit()
            return redirect(f'/users/{user_id}')
        except:
            db.session.rollback()
            flash('Invalid Input')
            return redirect(f'/users/{user_id}/posts/new')
    if request.method=='GET':
        return render_template('edit_post.html',post=post,all_tags=all_tags)

@app.route('/posts/<post_id>/delete',methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    Post.delete_at_id(post.id)
    return redirect(f'/users/{user_id}')

#TAGS

@app.route('/tags')
def tags_view():
    """list links for tags"""
    #search database for tags and display in a list#
    all_tags = Tag.query.all()
    return render_template('tags.html',all_tags=all_tags)
    
@app.route('/tags/<tag_id>')
def tag_detail_view(tag_id):
    """Show tag details"""
    #search database for tags and display in a list#
    tag = Tag.query.get(tag_id)
    
    return render_template('tag_details.html',tag=tag)

@app.route('/tags/new',methods=['GET','POST'])
def tags_new_view():
    """Shows and processes tag form"""
    #search database for tags and display in a list#
    if request.method=='POST':
        posted_tag = request.form['name_input']
        if Tag.query.filter_by(name=posted_tag).all():
            flash('Already Added')
        else:
            db.session.add(Tag(name=posted_tag))
            db.session.commit()
            print('should be added', posted_tag)
        return redirect('/tags')
    else:
        return render_template('new_tag.html')

@app.route('/tags/<tag_id>/edit',methods=['GET','POST'])
def edit_tag_view(tag_id):
    """Shows edit tag form"""
    #search database and edit tag#
    if request.method == 'POST':
        editing_tag = Tag.query.get(tag_id)
        editing_tag.name = request.form['name_input']
        db.session.add(editing_tag)
        db.session.commit()
        return redirect('/tags')
    else: 
        tag = Tag.query.get(tag_id)
        return render_template('edit_tag.html',tag=tag)

@app.route('/tags/<tag_id>/delete',methods=['POST'])
def delete_tag_view(tag_id):
    """Deletes tag"""
    #search database for tags and display in a list#
    cur_tag = Tag.query.get(tag_id)
    db.session.delete(cur_tag)
    db.session.commit()
    return redirect('/tags')

