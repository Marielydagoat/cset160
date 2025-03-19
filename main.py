from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
app = Flask(__name__)


conn_str = "mysql://root:cset155@localhost/boatdb" #the connection
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')#create route
def hello():
    return render_template('index.html')

# @app.route('/<name>')#create route
# def welcome(name): 
#     return render_template('user.html', name = name)

@app.route('/boats')
def boats():
   boats = conn.execute(text('SELECT * FROM boats')).all()
   return render_template('boats.html', boats = boats[:10])

@app.route('/boatCreate', methods = ['GET'])
def getBoat():
    return render_template('boat_create.html')

@app.route('/boatCreate', methods = ['POST'])
def createBoat():
    try:
        conn.execute(text('insert into boats values(:id, :name, :type, :owner_id, :rental_price)'), request.form)
    # conn.commit()
        return render_template('boat_create.html', error = None, success = 'successful')
    except:
        return render_template('boat_create.html', error = "fail", success = None)

# @app.route('/hello')
# def hello():
#     return f'hello'

# @app.route('/hello/<int:name>')
# def serving_cofee(name):
#     return f'the next number is {name +1}'


# @app.route('/donut')
# def donuts():
#     return 'here is your donut'


if __name__ == '__main__':
    app.run(debug=True)#last line