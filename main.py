from flask import Flask,g, redirect, render_template 
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

@app.route("/menu")
def menu():
   cursor = get_db().cursor()
   sql = "SELECT * FROM item"
   cursor.execute(sql)
   results = cursor.fetchall()
   return render_template("menu.html", results=results) 

def add():
    if request.method == "POST":
        cursor = get_db().cursor()
        id = int(request.form["item_id"])
        sql = "INSERT INTO order_item(item_name,item_description,item_price) VALUES (?,?,?)"
        cursor.execute(sql,(id,))
        results = cursor.fetchall()
    return redirect('/menu')
    

@app.route("/orders")
def orders():
    cursor = get_db().cursor()
    sql = "SELECT * FROM order_item"
    cursor.execute(sql)
    return render_template("order.html",)
   
''''
@app.route("/add", methods=["GET", "POST"])
def add():
    cursor = get_db().cursor()
    sql = "INSERT INTO order_items(name, descriptioh, price) VALUES (?,?,?)"
    cursor.execute(sql,)

    return render_template("menu.html", results=results) 
'''



if __name__ == "__main__":

   app.run(debug=True)