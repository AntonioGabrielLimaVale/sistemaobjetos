from models import db, Objeto


class ObjetoDAO:

    # Cadastrar um objeto
    @staticmethod
    def inserir(nome, descricao):
        objeto = Objeto(nome=nome, descricao=descricao)

        db.session.add(objeto)
        db.session.commit()

        return objeto

    # Listar todos os objetos
    @staticmethod
    def listar():
        return Objeto.query.all()

    # Buscar objeto pelo ID
    @staticmethod
    def buscar_por_id(id):
        return db.session.get(Objeto, id)

    # Atualizar um objeto
    @staticmethod
    def atualizar(id, nome, descricao):
        objeto = ObjetoDAO.buscar_por_id(id)

        if objeto:
            objeto.nome = nome
            objeto.descricao = descricao

            db.session.commit()
            return objeto

        return None

    # Excluir um objeto
    @staticmethod
    def excluir(id):
        objeto = ObjetoDAO.buscar_por_id(id)

        if objeto:
            db.session.delete(objeto)
            db.session.commit()
            return True

        return False
