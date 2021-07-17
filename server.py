import peeweedbevolve # new; must be imported before models
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Store, Warehouse # new line
app = Flask(__name__)

@app.before_request # new line
def before_request():
   db.connect()

@app.after_request # new line
def after_request(response):
   db.close()
   return response

@app.cli.command("migrate", help="migrate database") # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
   s = Store
   return render_template('index.html', s = s)

@app.route("/store")
def new_store():
   return render_template('store.html')

@app.route("/store", methods=['POST'])
def create_store():
   store_name = request.form.get('store_name')
   if Store.create(name = store_name):
      flash("Successfully saved.")
      return redirect(url_for('index'))

@app.route("/warehouse")
def new_warehouse():
   s = Store
   return render_template('warehouse.html', s = s)

@app.route("/warehouse", methods=['POST'])
def create_warehouse():
   location = request.form.get('location')
   store_select = request.form.get('store_select')
   try:
      Warehouse.create(location = location, store = store_select)
   except:
      print("error")
   return redirect(url_for('new_warehouse', location = location, store_select = store_select))

if __name__ == '__main__':
   app.run()