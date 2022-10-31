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

@app.route("/",)
def home():
    return render_template("index.html")

#displaying items from item table, and separate them
@app.route("/menu", methods =['GET', 'POST'])
def menu():
   cursor = get_db().cursor()
   chips = "SELECT id, name, description, price FROM item WHERE type = 'Chips'"
   cursor.execute(chips)
   chips = cursor.fetchall()

   cursor = get_db().cursor()
   fish = "SELECT id, name, description, price FROM item WHERE type = 'Fish'"
   cursor.execute(fish)
   fish = cursor.fetchall()
   popular = "SELECT id, name, description, price FROM item WHERE type = 'Popular'"
   cursor.execute(popular)
   popular = cursor.fetchall()

   cursor = get_db().cursor()
   distinct = "select item_id, name, description, price, count(*) as ct from item INNER JOIN order_item ON item.id = order_item.item_id group by item_id order by item_id"
   cursor.execute(distinct)
   distinct = cursor.fetchall()
   
   return render_template("menu.html", chips = chips, fish = fish, popular = popular, distinct =distinct,)

@app.route("/orders", methods =['GET', 'POST'])
def orders():
    cursor = get_db().cursor()
    sql = "SELECT item_id, name, description, price, order_item.item_id FROM item INNER JOIN order_item ON item.id = order_item.item_id"
    cursor.execute(sql)
    sql = cursor.fetchall()


    cursor = get_db().cursor()
    distinct = "select name, description, price, count(*) as ct from item INNER JOIN order_item ON item.id = order_item.item_id group by item_id order by item_id"
    cursor.execute(distinct)
    distinct = cursor.fetchall()

    '''
    cursor = get_db().cursor()
    distinct = "SELECT DISTINCT item_id, FROM order_item order_item.item_id FROM item INNER JOIN order_item ON item.id = order_item.item_id GROUP BY item_id ORDER BY item_id"
    cursor.execute(distinct)
    count = cursor.fetchall()'''

    return render_template("order.html", sql = sql, distinct= distinct, )

@app.route("/tester", methods =['GET', 'POST'])
def tester():
    cursor = get_db().cursor()
    distinct = "select item_id, name, description, price, count(*) as ct from item INNER JOIN order_item ON item.id = order_item.item_id group by item_id order by item_id"
    cursor.execute(distinct)
    distinct = cursor.fetchall()
    return render_template("tester.html", distinct = distinct)
    
@app.route("/faq")
def faq():
    return render_template("faq.html")   


#adding items to an order
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method =="POST":
        cursor = get_db().cursor()
        button = int(request.form["item"])
        insert = "INSERT INTO order_item (item_id) VALUES (?)"
        cursor.execute(insert,(button,))
        get_db().commit()
    return redirect('/menu')

#deleting items from an order
@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST": 
        cursor = get_db().cursor()
        object = int(request.form["id"])
        sql = "DELETE FROM order_item WHERE item_id=?"
        cursor.execute(sql,(object,))
        get_db().commit()
        
    return redirect ('/menu')




if __name__ == "__main__":
    app.run(debug=True)