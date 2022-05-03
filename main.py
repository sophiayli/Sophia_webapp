from flask import Flask,g, render_template 
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
   



if __name__ == "__main__":

   app.run(debug=True)