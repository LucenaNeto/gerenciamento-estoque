from flask import Flask, request, render_template, redirect, url_for
import json
from cliente import clientes_blueprint
import database as db

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
  return render_template("dashboard.html")

@app.route("/logout")
def logout():
  return render_template("login.html")

app.register_blueprint(clientes_blueprint)

@app.route("/produtos")
def produtos():
  return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html")

@app.route("/usuarios")
def usuarios():
  return render_template("dashboard.html")

@app.route("/fornecedores")
def fornecedores():
  return render_template("dashboard.html")

@app.route("/lojas")
def lojas():
  return render_template("dashboard.html")

@app.route("/categorias")
def categorias():
  bd = db.SQLiteConnection('estoque.db')
  bd.connect()
  categorias = bd.execute_query("select * from categorias;")
  print(categorias)
  return render_template("categorias.html", dados=categorias, categoria=(0,0))

@app.route("/categoria/save", methods=["POST"])
def categoriaSave():
  nome = request.form['nomeCategoria']
  id = request.form['id']
  bd = db.SQLiteConnection('estoque.db')
  bd.connect()
  if id:
    query = f"UPDATE categorias SET nome ='{nome}' WHERE id = {id}"
  else:
    query = f"INSERT INTO categorias (nome) VALUES ('{nome}')"
  print(query)
  bd.execute_query(query)
  return redirect(url_for('categorias'))
  
@app.route("/categoria/delete/<id>")
def categoriaDelete(id):
  bd = db.SQLiteConnection('estoque.db')
  bd.connect()
  bd.execute_query(f"DELETE FROM categorias WHERE id = {id}")
  return redirect(url_for('categorias'))

@app.route("/categoria/edit/<id>")
def categoriaEdit(id):
  bd = db.SQLiteConnection('estoque.db')
  bd.connect()
  query = f"select id, nome from categorias where id = {id};"
  nome = bd.execute_query(query)
  return render_template("categorias.html", categoria=nome)

@app.route("/setup")
def setup():
  bd = db.SQLiteConnection('estoque.db')
  bd.connect()
  bd.create_database()
  bd.execute_query("TRUNCATE TABLE categorias;")
  bd.execute_query("INSERT INTO categorias VALUES (1, 'Carnes');")
  bd.execute_query("INSERT INTO categorias VALUES (2, 'Gelados');")
  return "Instalado com sucesso!"

if __name__ == "__main__":
  app.run(debug=True)