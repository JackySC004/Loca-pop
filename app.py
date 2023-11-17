from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='Tuvieja'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True )
    name=db.Column(db.String(50))
    email=db.Column(db.String(70))
    password=db.Column(db.String(20))

with app.app_context():
    db.create_all()



@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        new_user=User(name=name,email=email,password=password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and password == user.password:
            return render_template('welcome.html')

    return render_template('login.html')



if __name__=='__main__':
    app.run(debug=True)