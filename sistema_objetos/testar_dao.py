from main import app
from models import db
from daos.objeto_dao import ObjetoDAO
from daos.administrador_dao import AdministradorDAO


with app.app_context():

    print("\n--- TESTE DO DAO DE OBJETOS ---")

    # Inserir objeto
    objeto = ObjetoDAO.inserir(
        "Notebook",
        "Notebook para teste"
    )
    print("Objeto cadastrado:", objeto.nome)

    # Listar objetos
    objetos = ObjetoDAO.listar()
    print("Quantidade de objetos:", len(objetos))

    # Buscar objeto
    encontrado = ObjetoDAO.buscar_por_id(objeto.id)
    print("Objeto encontrado:", encontrado.nome)

    # Atualizar objeto
    ObjetoDAO.atualizar(
        objeto.id,
        "Notebook atualizado",
        "Descrição atualizada"
    )
    print("Objeto atualizado:", ObjetoDAO.buscar_por_id(objeto.id).nome)

    # Excluir objeto
    ObjetoDAO.excluir(objeto.id)
    print("Objeto excluído:", ObjetoDAO.buscar_por_id(objeto.id))


    print("\n--- TESTE DO DAO DE ADMINISTRADORES ---")

    # Inserir administrador
    administrador = AdministradorDAO.inserir(
        "admin_teste",
        "senha123"
    )
    print("Administrador cadastrado:", administrador.usuario)

    # Listar administradores
    administradores = AdministradorDAO.listar()
    print("Quantidade de administradores:", len(administradores))

    # Buscar administrador
    encontrado = AdministradorDAO.buscar_por_id(administrador.id)
    print("Administrador encontrado:", encontrado.usuario)

    # Autenticar administrador
    login = AdministradorDAO.autenticar(
        "admin_teste",
        "senha123"
    )
    print("Autenticação correta:", login is not None)

    # Atualizar administrador
    AdministradorDAO.atualizar(
        administrador.id,
        "admin_atualizado"
    )
    print("Administrador atualizado:", AdministradorDAO.buscar_por_id(administrador.id).usuario)

    # Excluir administrador
    AdministradorDAO.excluir(administrador.id)
    print("Administrador excluído:", AdministradorDAO.buscar_por_id(administrador.id))
