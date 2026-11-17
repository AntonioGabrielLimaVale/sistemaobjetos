import os
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session
)
from dotenv import load_dotenv
from sqlalchemy.engine import URL

from models import db, Administrador
from daos.objeto_dao import ObjetoDAO
from daos.administrador_dao import AdministradorDAO

load_dotenv(override=True)
print("Usuário:", os.getenv("DB_USER"))
print("Senha:", repr(os.getenv("DB_PASSWORD")))
print("Banco:", os.getenv("DB_NAME"))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

conexao = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME")
)

app.config["SQLALCHEMY_DATABASE_URI"] = conexao
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Verificar se o administrador está autenticado
def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar(*args, **kwargs):
        if "administrador_id" not in session:
            flash("Faça login para acessar esta página.", "error")
            return redirect(url_for("login"))

        return funcao(*args, **kwargs)

    return verificar


@app.route("/")
def index():
    return render_template("index.html")


# GERENCIAMENTO DE OBJETOS

@app.route("/objetos", methods=["GET", "POST"])
def objetos():
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")

        if nome:
            ObjetoDAO.inserir(nome, descricao)
            flash("Objeto cadastrado com sucesso!", "success")
        else:
            flash("Informe o nome do objeto.", "error")

        return redirect(url_for("objetos"))

    lista_objetos = ObjetoDAO.listar()
    return render_template("objetos.html", objetos=lista_objetos)


@app.route("/objetos/editar/<int:id>", methods=["POST"])
def editar_objeto(id):
    nome = request.form.get("nome")
    descricao = request.form.get("descricao")

    if nome:
        ObjetoDAO.atualizar(id, nome, descricao)
        flash("Objeto atualizado!", "success")

    return redirect(url_for("objetos"))


@app.route("/objetos/excluir/<int:id>", methods=["POST"])
def excluir_objeto(id):
    ObjetoDAO.excluir(id)
    flash("Objeto excluído!", "success")

    return redirect(url_for("objetos"))


# LOGIN DO ADMINISTRADOR

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        administrador = AdministradorDAO.autenticar(usuario, senha)

        if administrador:
            session["administrador_id"] = administrador.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("administradores"))

        flash("Usuário ou senha incorretos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("administrador_id", None)
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("index"))


# GERENCIAMENTO DE ADMINISTRADORES

@app.route("/administradores", methods=["GET", "POST"])
@login_obrigatorio
def administradores():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario and senha:
            try:
                AdministradorDAO.inserir(usuario, senha)
                flash("Administrador cadastrado!", "success")
            except Exception:
                db.session.rollback()
                flash("Não foi possível cadastrar. Verifique se o usuário já existe.", "error")
        else:
            flash("Preencha o usuário e a senha.", "error")

        return redirect(url_for("administradores"))

    lista_administradores = AdministradorDAO.listar()

    return render_template(
        "administradores.html",
        administradores=lista_administradores
    )


@app.route("/administradores/editar/<int:id>", methods=["POST"])
@login_obrigatorio
def editar_administrador(id):
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    if usuario:
        try:
            AdministradorDAO.atualizar(id, usuario, senha or None)
            flash("Administrador atualizado!", "success")
        except Exception:
            db.session.rollback()
            flash("Não foi possível atualizar. Verifique se o usuário já existe.", "error")

    return redirect(url_for("administradores"))


@app.route("/administradores/excluir/<int:id>", methods=["POST"])
@login_obrigatorio
def excluir_administrador(id):
    if session.get("administrador_id") == id:
        flash("Você não pode excluir o administrador que está usando.", "error")
    else:
        AdministradorDAO.excluir(id)
        flash("Administrador excluído!", "success")

    return redirect(url_for("administradores"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

