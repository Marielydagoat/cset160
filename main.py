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
@app.route('/home')
def Home():
    return render_template('base.html')

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
        conn.execute(text('INSERT INTO boats VALUES (:id, :name, :type, :owner_id, :rental_price)'), request.form)
        conn.commit
        return render_template('boat_create.html', error=None, success='successful')
    
    except:
        return render_template('boat_create.html', error = "fail", success = None)
    
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        boats = get_boats_from_db(query) 
        return render_template('search.html', boats = boats)
    return render_template('search.html', boats=[])

def get_boats_from_db(query):
    query = f"%{query}%"
    result = conn.execute(text("SELECT * FROM boats WHERE name LIKE :query OR type LIKE :query"), {"query": query}).fetchall()
    return result

@app.route('/boatDelete/<int:boat_id>', methods=['POST'])
def delete_boat(boat_id):
    try:
        conn.execute(
            text('DELETE FROM boats WHERE id = :boat_id'),
            {'boat_id': boat_id}
        )
        conn.commit()
        boats = conn.execute(text('SELECT * FROM boats')).all()
        return render_template('boats.html', boats=boats[:10], success='Boat deleted successfully', error=None)
    
    except Exception as e:
        conn.rollback()
        print(f"Error occurred while deleting boat: {e}")
        boats = conn.execute(text('SELECT * FROM boats')).all()
        return render_template('boats.html', boats=boats[:10], success=None, error="Failed to delete boat")
    
@app.route('/boatUpdate/<int:boat_id>', methods=['GET', 'POST'])
def update_boat(boat_id):
    print(f"Attempting to fetch boat with ID: {boat_id}")  # Debugging line
    if request.method == 'GET':
        boat = conn.execute(
            text("SELECT * FROM boats WHERE id = :boat_id"), {"boat_id": boat_id}).fetchone()
        print(f"Boat found: {boat}")
        if boat:
            return render_template('boat_update.html', boat=boat)
        else:
            return "Boat not found", 404

    if request.method == 'POST':
        name = request.form['name']
        boat_type = request.form['boat_type']
        owner_id = request.form['owner_id']
        rental_price = request.form['rental_price']
        try:
            conn.execute(
                text('UPDATE boats SET name = :name, type = :boat_type, owner_id = :owner_id, rental_price = :rental_price WHERE id = :boat_id'),
                {'name': name, 'boat_type': boat_type, 'owner_id': owner_id, 'rental_price': rental_price, 'boat_id': boat_id}
            )
            conn.commit()
            return render_template('boat_update.html', boat=None, success="Boat updated successfully")
        except Exception as e:
            print(f"Error occurred while updating boat: {e}")
            return render_template('boat_update.html', boat=None, error="Failed to update boat")


if __name__ == '__main__':
    app.run(debug=True)#last line