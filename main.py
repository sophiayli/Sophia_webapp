from flask import Flask,g, redirect, render_template, request, redirect
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
    sql = "SELECT * FROM order_item"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("order.html", results=results)
   

@app.route("/add", methods=["GET","POST"])
def add():
    cursor = get_db().cursor()
    new_name= request.form["item_name"]
    new_description = request.form["item_description"]
    new_price = int(request.form["item_price"])
    sql = "INSERT INTO order_items(item_name, item_descriptioh, item_price) VALUES (?,?,?)"
    cursor.execute(sql,(new_name, new_description))
    get_db().commit()

    return redirect('/menu')

@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        # getting the item then deleting it 
        cursor = get_db().cursor()
        object = int(request.form[item_name])
        sql = "DELETE FROM order_item WHERE item_id=?"
        cursor.execute(sql,(object))
        get_db().commit()
    return redirect ('/orders')



if __name__ == "__main__":
    app.run(debug=True)