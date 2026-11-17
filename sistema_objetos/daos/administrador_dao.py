from models import db, Administrador


class AdministradorDAO:

    # Cadastrar um administrador
    @staticmethod
    def inserir(usuario, senha):
        administrador = Administrador(usuario=usuario)
        administrador.definir_senha(senha)

        db.session.add(administrador)
        db.session.commit()

        return administrador

    # Listar todos os administradores
    @staticmethod
    def listar():
        return Administrador.query.all()

    # Buscar administrador pelo ID
    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Administrador, id)

    # Atualizar administrador
    @staticmethod
    def atualizar(id, usuario, senha=None):
        administrador = AdministradorDAO.buscar_por_id(id)

        if administrador:
            administrador.usuario = usuario

            if senha:
                administrador.definir_senha(senha)

            db.session.commit()
            return administrador

        return None

    # Excluir administrador
    @staticmethod
    def excluir(id):
        administrador = AdministradorDAO.buscar_por_id(id)

        if administrador:
            db.session.delete(administrador)
            db.session.commit()
            return True

        return False

    # Autenticar administrador
    @staticmethod
    def autenticar(usuario, senha):
        administrador = Administrador.query.filter_by(
            usuario=usuario
        ).first()

        if administrador and administrador.verificar_senha(senha):
            return administrador

        return None
