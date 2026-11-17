from main import app
from models import db, Administrador
from daos.administrador_dao import AdministradorDAO

with app.app_context():

    administrador = Administrador.query.filter_by(
        usuario="admin"
    ).first()

    if administrador is None:
        administrador = Administrador(usuario="admin")
        db.session.add(administrador)

    # Define novamente a senha
    administrador.definir_senha("admin123")

    db.session.commit()

    print("Administrador configurado!")

    # Testa a autenticação
    resultado = AdministradorDAO.autenticar(
        "admin",
        "admin123"
    )

    print("Autenticação funcionando:", resultado is not None)
