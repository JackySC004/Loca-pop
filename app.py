from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import qrcode

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='Tuvieja'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True )
    name=db.Column(db.String(50))
    email=db.Column(db.String(70))
    password=db.Column(db.String(20))

class Tickets(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    party_name=db.Column(db.String(160))
    amount_of_tickets=db.Column(db.Integer)
    is_used=db.Column(db.Boolean, default=False)

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
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        user=User.query.filter_by(email=email).first()
        if user and password == user.password:
            return redirect('/welcome')

    return render_template('login.html')


@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    
    if request.method == 'POST':
        amount_of_tickets=request.form['amount-of-tickets']
        party_name=request.form['party-name']
        # Se genera el Qr
        qr=qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data('www.youtube.com')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'{party_name}_1.png')
        # Se convierte el tipo dato que almacena "amount_qr" que es un tipo de dato str a int
        amount_of_tickets_int=int(amount_of_tickets) 
        #Se crea la tabla en la base de datos y Se generan el resto de QR
        for indice in range(1,amount_of_tickets_int):
            img.save(f'{party_name}_{indice + 1}.png')
            new_ticket=Tickets(party_name=party_name, amount_of_tickets=amount_of_tickets)
            print(new_ticket)
            db.session.add(new_ticket)
            
        db.session.commit()
        return render_template('generate_qr.html')
    return render_template('generate_qr.html') 

@app.route('/update/<string:ticket_id>', methods=['POST','GET'])
def update_ticket(ticket_id):
    ticket=Tickets.query.filter_by(id=ticket_id).first()

    ticket.is_used=True
    db.session.commit()
    if ticket:
        if ticket.is_used == False:
            return 'verde'
        elif ticket.is_used == True:
            return 'rojo'
        else:
            return 'rojo'
    else:
        return 'rojo'
        



if __name__=='__main__':
    app.run(debug=True)