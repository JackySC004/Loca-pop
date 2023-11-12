from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        print (email)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)