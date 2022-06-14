from cgitb import text
from ntpath import join
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

@app.route("/menu",)
def menu():
   cursor = get_db().cursor()
   sql = "SELECT * FROM item"
   cursor.execute(sql)
   results = cursor.fetchall()
   return render_template("menu.html", results=results) 


@app.route("/orders")
def orders():
    cursor = get_db().cursor()
    sql = "SELECT id, name, description, price FROM item INNER JOIN order_item ON item.id = order_item.item_id"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("order.html", results=results)
   

@app.route("/add", methods=["GET","POST"])
def add():
    cursor = get_db().cursor()
    button = str(request.form["id"])
    insert = "INSERT INTO order_items(item_id)VALUES (?)"
    cursor.execute(insert,(button))
    get_db().commit()
    return redirect('/orders')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST": 
        cursor = get_db().cursor()
        print(request.form["item_id"])
        object = str(request.form["item_id"])
        sql = "DELETE FROM order_item WHERE item_id=?"
        cursor.execute(sql,(object,))
        get_db().commit()
        
    return redirect ('/orders')



if __name__ == "__main__":
    app.run(debug=True)