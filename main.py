from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alby.db'
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    recipe = db.relationship('Recipe', backref='user')

    def __init__(self,username):
        self.username = username

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    ingredients = db.Column(db.String(10000))
    steps = db.Column(db.String(10000))

    def __init__(self, user_id, name, ingredients, steps):
        self.user_id = user_id
        self.name = name
        self.ingredients = ingredients
        self.steps = steps

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/myRecipes")
def myRecipes():
    return render_template('myRecipes.html', values=Recipe.query.all())

@app.route("/newRecipe", methods=['GET','POST'])
def newRecipe():
    if request.method == 'POST':
        name = request.form['recipeName']
        ingredients = request.form['recipeIngredients']
        steps = request.form['recipeSteps']
 
    
        new_recipe = Recipe(session['user'],name,ingredients,steps)
        db.session.add(new_recipe)
        db.session.commit()

        flash("Recipe created successfully.")
        return redirect(url_for('myRecipes'))

    return render_template('newRecipe.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']

        found_user = User.query.filter_by(username=user).first()
        if found_user:
            session.permanent=True
            session['user'] = user
            return redirect(url_for('home'))
        else:
            flash(f"User does not exist. Please try again or register.")
            return redirect('/login')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    if "user" in session:
        user = session['user']
        flash(f"You have been logged out, {user}", 'info')
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        try:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
        except:
            flash(f"That username already exists. Please try a different username.")
            return redirect('/register')
        flash(f"Registration successful!")
        return redirect('/login')
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)