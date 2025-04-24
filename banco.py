import mysql.connector
from matheuseduardodb_sa import *

class Usuarios(object):
    def __init__(self, id_usuario=0, nome="", senha="",tipo=""):
        self.info = {}
        self.idusuario = id_usuario
        self.nome = nome
        self.tipo = tipo
        self.senha = senha

    def insertUser(self):
        banco = matheuseduardodb_sa()
        try:
            c = banco.conexao.cursor()
            c.execute("INSERT INTO usuario (nome, tipo, senha) VALUES (%s, %s, %s)",
                      (self.nome, self.tipo, self.senha))
            banco.conexao.commit()
            c.close()
            return "Usuário cadastrado com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro na inserção do usuário: {e}"

    def updateUser(self):
        banco = matheuseduardodb_sa()
        try:
            c = banco.conexao.cursor()
            c.execute("UPDATE usuario SET nome=%s, usuario=%s, senha=%s WHERE id_usuario=%s",
                      (self.nome, self.usuario, self.senha, self.id_usuario))
            banco.conexao.commit()
            c.close()
            return "Usuário atualizado com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro na alteração do usuário: {e}"

    def deleteUser(self):
        banco = matheuseduardodb_sa()
        try:
            c = banco.conexao.cursor()
            c.execute("DELETE FROM usuario WHERE id_usuario=%s", (self.id_usuario,))
            banco.conexao.commit()
            c.close()
            return "Usuário excluído com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro na exclusão do usuário: {e}"

    def selectUser(self, id_usuario):
        banco = matheuseduardodb_sa()
        try:
            c = banco.conexao.cursor()
            c.execute("SELECT * FROM usuario WHERE idUsuario=%s", (id_usuario,))
            usuario = c.fetchone()
            if usuario:
                self.id_usuario, self.nome, self.telefone, self.email, self.usuario, self.senha = usuario
            c.close()
            return "Busca feita com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro na busca do usuário: {e}"
