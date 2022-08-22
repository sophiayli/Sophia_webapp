from flask import Flask,g, redirect, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = 'sophia_webapp.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/menu", methods =['GET', 'POST'])
def menu():
   #get items with type name Chips
   cursor = get_db().cursor()
   chips = "SELECT name, description, price FROM item WHERE type = 'Chips'"
   cursor.execute(chips)
   chips = cursor.fetchall()
   #get items with the name Fish
   cursor = get_db().cursor()
   fish = "SELECT name, description, price FROM item WHERE type = 'Fish'"
   cursor.execute(fish)
   fish = cursor.fetchall()
   #get items with type name Popular
   popular = "SELECT name, description, price FROM item WHERE type = 'Popular'"
   cursor.execute(popular)
   popular = cursor.fetchall()
   return render_template("menu.html", chips = chips, fish = fish, popular = popular,)


@app.route("/orders")
def orders():
    cursor = get_db().cursor()
    sql = "SELECT item.id, name, description, price, order_item.id FROM item INNER JOIN order_item ON item.id = order_item.item_id"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("order.html", results=results)

@app.route("/tester", methods =['GET', 'POST'])
def tester():
   cursor = get_db().cursor()
   chips = "SELECT name, description, price FROM item WHERE type = 'Chips'"
   cursor.execute(chips)
   chips = cursor.fetchall()
   cursor = get_db().cursor()
   fish = "SELECT name, description, price FROM item WHERE type = 'Fish'"
   cursor.execute(fish)
   fish = cursor.fetchall()
   popular = "SELECT name, description, price FROM item WHERE type = 'Popular'"
   cursor.execute(popular)
   popular = cursor.fetchall()
   return render_template("tester.html", chips = chips, fish = fish, popular = popular,)
    
@app.route("/faq")
def faq():
    return render_template("faq.html")   



@app.route("/add", methods=["GET","POST"])
def add():
    if request.method =="POST":
        cursor = get_db().cursor()
        button = int(request.form["item"])
        insert = "INSERT INTO order_item (item_id) VALUES (?)"
        cursor.execute(insert,(button,))
        get_db().commit()
    return redirect('/menu')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST": 
        cursor = get_db().cursor()
        object = int(request.form["id"])
        sql = "DELETE FROM order_item WHERE id=?"
        cursor.execute(sql,(object,))
        get_db().commit()
        
    return redirect ('/orders')




if __name__ == "__main__":
    app.run(debug=True)