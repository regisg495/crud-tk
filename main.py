from tkinter import ttk
from tkinter import *

import sqlite3


class Pecas:
    # Conexão
    db_name = 'base.db'

    def __init__(self, window):
        # Inicialização
        self.wind = window
        self.wind.title('CRUD de Peças')

        # Botões de mostrar peças
        ttk.Button(text='MOSTRAR TODAS AS PEÇAS', command=self.findAll).grid(row=0, column=0, sticky=W + N + E)
        ttk.Button(text='PEÇA DE MAIOR QUANTIDADE', command=self.showHighesAmount).grid(row=0, column=1,
                                                                                        sticky=W + N + E)
        ttk.Button(text='PEÇA MAIS CARA', command=self.showMoreExpensive).grid(row=1, column=0, sticky=W + N + E)
        ttk.Button(text='PEÇA MAIS BARATA', command=self.showMoreEconomic).grid(row=1, column=1, sticky=W + N + E)

        # Cria Frame
        frame = LabelFrame(self.wind, text='Registrar nova peça')
        frame.grid(row=1, column=0, columnspan=3, pady=60)

        # Input Nome
        Label(frame, text='Nome: ').grid(row=1, column=0)
        self.nome = Entry(frame)
        self.nome.focus()
        self.nome.grid(row=1, column=1)

        # Input Quantidade
        Label(frame, text='Quantidade: ').grid(row=2, column=0)
        self.quantidade = Entry(frame)
        self.quantidade.grid(row=2, column=1)

        # Input Preço
        Label(frame, text='Preço: ').grid(row=3, column=0)
        self.preco = Entry(frame)
        self.preco.grid(row=3, column=1)

        # Botão add Produto
        ttk.Button(frame, text='Salvar Peça', command=self.add_product).grid(row=4, columnspan=2, sticky=W + E)

        # Mensagens para o Usuário
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabela com a Lista que será preenchida
        self.tree = ttk.Treeview(height=10, columns=['#1', '#2'])
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Nome', anchor=CENTER)
        self.tree.heading('#1', text='Quantidade', anchor=CENTER)
        self.tree.heading('#2', text='Preco', anchor=CENTER)

        # Botões Editar ou Deletar
        ttk.Button(text='DELETAR', command=self.deletePeca).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text='EDITAR', command=self.editPeca).grid(row=5, column=1, sticky=W + E)

        # Preenchimento da Lista com os itens do BD
        self.findAll()

    # Função para executar query do BD
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # select * from tabela
    def findAll(self):
        # limpando
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # sql
        sql = 'SELECT * FROM pecas ORDER BY nome DESC'
        db_rows = self.run_query(sql)
        # preenchendo
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[0]))

    # mostra peça de maior quantidade
    def showHighesAmount(self):
        # limpando
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)
        # SQL
        sql = 'SELECT * FROM pecas WHERE quantidade = (SELECT MAX(quantidade) FROM pecas);'
        db_rows = self.run_query(sql)
        # preenchendo
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[0]))

    def showMoreExpensive(self):
        # limpando
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)
        # SQL
        sql = 'SELECT * FROM pecas WHERE preco = (SELECT MAX(preco) FROM pecas);'
        db_rows = self.run_query(sql)
        # preenchendo
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[0]))

    def showMoreEconomic(self):
        # limpando
        records = self.tree.get_children()

        for element in records:
            self.tree.delete(element)
        # sql
        query = 'SELECT * FROM pecas WHERE preco = (SELECT MIN(preco) FROM pecas);'
        db_rows = self.run_query(query)
        # preenchendo
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3], row[0]))

    # Validação se foi inserido algo nos inputs
    def validation(self):
        return len(self.nome.get()) != 0 and len(self.preco.get()) != 0 and len(self.quantidade.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO pecas (nome, quantidade, preco) VALUES(?, ?, ?)'
            parameters = (self.nome.get(), self.quantidade.get(), self.preco.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Peça {} adicionada com sucesso'.format(self.nome.get())
            self.nome.delete(0, END)
            self.quantidade.delete(0, END)
            self.preco.delete(0, END)
        else:
            self.message['text'] = 'Os atributos devem estar preenchidos e com valores não negativos'
        self.findAll()

    def deletePeca(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][2]
        except IndexError as e:
            self.message['text'] = 'Por favor, escolha uma peça para deletar'
            return
        self.message['text'] = ''
        id = self.tree.item(self.tree.selection())['values'][2]
        nome = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM pecas WHERE id = ?'
        self.run_query(query, (id,))
        self.message['text'] = '{} deletado com sucesso'.format(nome)
        self.findAll()

    def editPeca(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][2]
        except IndexError as e:
            self.message['text'] = 'Por favor, escolha uma peça para editar'
            return
        nomeAtual = self.tree.item(self.tree.selection())['text']
        quantidadeAtual = self.tree.item(self.tree.selection())['values'][0]
        precoAtual = self.tree.item(self.tree.selection())['values'][1]
        id = self.tree.item(self.tree.selection())['values'][2]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Produto'
        # Nome
        Label(self.edit_wind, text='Nome Atual:').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=nomeAtual), state='readonly').grid(row=0,
                                                                                                              column=2)
        # Novo nome
        Label(self.edit_wind, text='Novo Nome:').grid(row=1, column=1)
        novoNome = Entry(self.edit_wind)
        novoNome.grid(row=1, column=2)

        # Quantidade Atual
        Label(self.edit_wind, text='Quantidade Atual:').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=quantidadeAtual), state='readonly').grid(
            row=2, column=2)

        # Nova Quantidade
        Label(self.edit_wind, text='Nova Quantidade:').grid(row=3, column=1)
        novaQuantidade = Entry(self.edit_wind)
        novaQuantidade.grid(row=3, column=2)

        # Preço Atual
        Label(self.edit_wind, text='Preço Atual:').grid(row=4, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=precoAtual), state='readonly').grid(row=4,
                                                                                                               column=2)

        # Nova Quantidade
        Label(self.edit_wind, text='Novo Preço:').grid(row=5, column=1)
        novoPreco = Entry(self.edit_wind)
        novoPreco.grid(row=5, column=2)

        Button(self.edit_wind, text='Editar',
               command=lambda: self.edit_records(nomeAtual, id, novoNome.get(), novaQuantidade.get(),
                                                 novoPreco.get())).grid(row=6, column=2, sticky=W)

        self.edit_wind.mainloop()

    def edit_records(self, nomeAtual, id, novoNome, novaQuantidade, novoPreco):
        query = 'UPDATE pecas SET nome = ?, quantidade = ?, preco = ? WHERE id = ?'
        parameters = (novoNome, novaQuantidade, novoPreco, id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Peça {} atualizada com sucesso'.format(nomeAtual)
        self.findAll()


if __name__ == '__main__':
    window = Tk()
    application = Pecas(window)
    window.mainloop()
