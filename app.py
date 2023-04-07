from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///booking.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key="secret@1234"


db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    fName = db.Column(db.String, nullable=False)
    lName = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    cnfPassword = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.fName

class Blog(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    poster = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Blogs %r>' % self.title

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    blog=Blog.query.all()
    return render_template('index.html',blog=blog)


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).scalar()
        if user and password==user.password:
            login_user(user)
            return redirect('/')
        else:
            flash('Please check your email and password','warning')
            return redirect('/login')

    return render_template('login.html')


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        mobile=request.form.get('mobile')
        fName=request.form.get('fName')
        lName=request.form.get('lName')
        password=request.form.get('password')
        cnfPassword=request.form.get('cnfPassword')
        user=User(email=email,mobile=mobile,fName=fName,lName=lName,password=password,cnfPassword=cnfPassword)
        db.session.add(user)
        db.session.commit()
        flash('Sign-Up Succesful!','success')
        return redirect('/login')

    return render_template("signup.html")

    

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')



@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/createpage',methods=['GET','POST'])
def createpage():
    if request.method=='POST':
        title=request.form.get('title')
        author=request.form.get('author')
        description=request.form.get('description')    
        poster=request.form.get('poster')
        blog=Blog(title=title,author=author,description=description,poster=poster)
        db.session.add(blog)
        db.session.commit()
        flash("Post Uploaded",'success')
        return redirect('/')
    return render_template('createpage.html')

@app.route('/blogdetails/<int:id>')
def blogdetails(id):
    blog=Blog.query.get(id)
    return render_template('blogdetails.html',blog=blog)

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    blog=Blog.query.get(id)
    if request.method=='POST':
        blog.title=request.form.get('title')
        blog.author=request.form.get('author')
        blog.description=request.form.get('description')
        blog.poster=request.form.get('poster')
        db.session.commit()
        flash("Post Updated!",'success')
        return redirect('/')
    return render_template('editblog.html', blog=blog)

@app.route('/delete/<int:id>')
def delete(id):
    blog=Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog deleted!','success')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)