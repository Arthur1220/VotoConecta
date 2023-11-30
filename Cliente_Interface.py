# Importacao da Classe Cliente, com todas as suas variaveis e metodos
from Cliente import ClienteVotacaoOnline

# Importacao da biblioteca Tkinter e etc
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring

# Classe de interface do Cliente
class InterfaceVotacao:
    # Funcao do construtor
    def __init__(self):

        # Definicao do nome do dispositivo
        # Loop ate que o nome seja valido ou entao o usuario cancele
        while True:
            self.nome_cliente = askstring("Nome do Cliente", "Digite seu nome:")
            if self.nome_cliente:
                break
            elif self.nome_cliente is None:
                return
            messagebox.showerror("Erro", "Nome do cliente não pode ser vazio.")
        
        # Definicao das configuaracoes de rede
        HOST = '127.0.0.1'
        PORT = 12345

        # Inicializacao da rede Cliente
        self.cliente_votacao = ClienteVotacaoOnline(HOST, PORT, self.nome_cliente)

        # Inicializacao do menu
        self.Menu()
    
    # Funcao de menu
    def Menu(self):
        self.root = Tk()

        self.root.title(f"Votação Online - Cliente: {self.nome_cliente}")
        self.root.geometry("507x310")
        self.root.resizable(False, False)

        Label(self.root, text="Programa de votacao online,\nescolha como deseja prosseguir:", font=('Calibri', 12)).place(x=125, y=15)

        menubar = Menu(self.root)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Mostrar guia", command=self.MenuOption_Help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

        Button(self.root, text="Votar", command=self.Registrar_voto, padx=88, pady=20, font=('Calibri', 12)).place(x=30, y=80)
        Button(self.root, text="Registrar Chapa", command=self.Registrar_chapa, padx=44, pady=20, font=('Calibri', 12)).place(x=262, y=80)
        Button(self.root, text="Consultar votantes", command=self.Consultar_votantes, padx=35, pady=20, font=('Calibri', 12)).place(x=30, y=150)
        Button(self.root, text="Resultados", command=self.Consultar_resultados, padx=65, pady=20, font=('Calibri', 12)).place(x=262, y=150)
        Button(self.root, text="FINALIZAR", command=self.Finalizar, padx=55, pady=20, font=('Calibri', 12)).place(x=150, y=230)

        self.root.mainloop()

    # Funcao para direcionar caminho do menu de opcoes
    def MenuOption_Help(self):
        help_window = Toplevel(self.root)
        help_window.title("Guia de Votação Online")
        help_window.geometry("400x300")

        Label(help_window, text="Bem-vindo ao Votação Online!", font=('Calibri', 12)).pack(pady=10)

        text = (
            "Este é um programa de votação online onde você pode:\n\n"
            "1. Votar em uma chapa\n"
            "2. Registrar uma nova chapa\n"
            "3. Consultar a lista de votantes\n"
            "4. Verificar os resultados parciais\n"
            "5. Finalizar a votação e visualizar resultados\n\n"
            "Para usar o programa, clique nos botões\ncorrespondentesàs ações desejadas."
        )

        Label(help_window, text=text, font=('Calibri', 10)).pack(padx=20, pady=10)

        help_window.mainloop()

    def atualizar_info(self, tree_resultados, tree_votantes):
        # Substitua o código abaixo pelos seus métodos reais de atualização de resultados e votantes
        # Atualiza os resultados
        resultados_fake = {"Chapa1": 60, "Chapa2": 25, "Chapa3": 15}
        self.atualizar_tree(tree_resultados, resultados_fake)

        # Atualiza os votantes
        votantes_fake = {"Votante1": 1, "Votante2": 2, "Votante3": 3, "Votante4": 4}
        self.atualizar_tree(tree_votantes, votantes_fake)

    # Funcao para registrar uma nova chapa
    def Registrar_chapa(self):

        # Definicao do nome da chapa
        nome_chapa = askstring("Registrar Chapa", "Digite o nome da chapa:")
        if nome_chapa is None:
            return

        # Definicao do valor da chapa
        # Loop ate que o valor seja um inteiro ou entao o usuario cancele
        while True:
            valor_chapa = askstring("Registrar Chapa", "Digite o valor para a chapa:")
            if valor_chapa is None:
                return

            # Verifica se o valor_chapa é um número inteiro
            try:
                int(valor_chapa)
            except ValueError:
                messagebox.showerror("Erro", "O valor da chapa deve ser um número inteiro. Tente novamente")
                continue
            
            break

        # Utiliza a funcao do arquivo cliente para fazer o registro da chapa, e recebe uma resposta do mesmo
        resposta = self.cliente_votacao.registrar_chapa(nome_chapa, valor_chapa)

        # Caso a chapa nao possa ser criada, ira aparecer uma mensagem de erro perguntado se deseja refazer a operacao
        # Um dos motivos para a chapa nao ser criada e ela ja existir
        if resposta != "CHAPA_REGISTRADA":
            reiniciar = messagebox.askyesno("Erro", "A chapa não pode ser criada. Deseja refazer a operação?")
            if reiniciar:
                self.Registrar_chapa()
            else:
                messagebox.showinfo("Resposta do Servidor", "Chapa invalida")
        else:
            messagebox.showinfo("Resposta do Servidor", "Chapa criada com sucesso")

    # Funcao para registrar voto
    def Registrar_voto(self):
        # Definicao do numero da chapa
        # Loop enquanto o valor e um inteiro
        while True:
            NumeroVotante = askstring("Votar", "Digite o número da chapa:")
            if NumeroVotante is None:
                return

            # Tenta converter o número da chapa para um número inteiro
            try:
                int(NumeroVotante)
            except ValueError:
                messagebox.showerror("Erro", "O número da chapa deve ser um valor inteiro. Tente novamente.")
                continue  # Continua o loop se a conversão falhar

            break

        # Definicao do nome do votante
        NomeVotante = askstring("Votar", "Digite seu nome:")
        if NomeVotante is None:
                return

        # Loop de confirmacao de voto, onde o usuario deve confirmar seu voto no askyesno
        while True:
            # Confirmação final
            confirmacao = messagebox.askyesno("Confirmação", f"{NomeVotante}, voce deseja Registrar_voto na chapa {NumeroVotante}?")

            # Caso o usuario confirme
            if confirmacao:

                # Utiliza a funcao do arquivo cliente para fazer o registro de voto, e recebe uma resposta do mesmo
                resposta = self.cliente_votacao.votar(NumeroVotante, NomeVotante)
                
                # Caso o numero da chapa nao exista, ira aparecer uma mensagem de erro perguntado se deseja refazer a operacao
                if resposta == "CHAPA_INVALIDA":
                    reiniciar = messagebox.askyesno("Erro", "Chapa inexistente. Deseja refazer a operação?")
                    if reiniciar:
                        self.Registrar_voto()
                    else:
                        messagebox.showinfo("Resposta do Servidor", "Chapa invalida")
                elif resposta == "NOME_INVALIDO":
                    reiniciar = messagebox.askyesno("Erro", "Nome ja registrado. Deseja refazer a operação?")
                    if reiniciar:
                        self.Registrar_voto()
                    else:
                        messagebox.showinfo("Resposta do Servidor", "Nome invalido")
                # Caso toda a operacao tenha sido um sucesso
                else:
                    messagebox.showinfo("Resposta do Servidor", "Voto registrado com sucesso.")
                break  # Sai do loop se o usuário confirmar

            # Caso o usuario nao confirme
            else:
                break  # Sai do loop se o usuário cancelar a confirmação

    # Funcao para consultar os votantes ja registrados
    def Consultar_votantes(self):

        # Utiliza a funcao do arquivo cliente para fazer o pedido do dicionario com a lista do nome dos votantes
        votantes = self.cliente_votacao.consultar_votantes()
        
        # Verificar se há resultados antes de prosseguir
        if not votantes or votantes == " ":
            messagebox.showinfo("Sem Resultados", "Ainda não há resultados para exibir.")
            return

        # Fecha o root da tela principal, para manter apenas a tela para visualizar votos
        self.root.destroy()

        self.root = Tk()

        self.root.title(f"Votação Online - Cliente: {self.nome_cliente}")
        self.root.geometry("500x310")
        self.root.resizable(False, False)

        Label(self.root, text="Tela de visualizacao dos votantes:", font=('Calibri', 12)).place(x=125, y=15)

        Button(self.root, text="Retornar", command=self.Retornar_menu, padx=55, pady=20, font=('Calibri', 12)).place(x=150, y=230)
        
        # Criacao do frame para armazenar a Tree
        frame = Frame(self.root)
        frame.place(x=50, y=40, height=180, width=400)

        # Criação da Treeview
        # INICIO
        tree = ttk.Treeview(frame, columns=("Nome",))
        tree.heading("#0", text="ID")
        tree.heading("Nome", text="Nome")

        tree.column("#0", width=50)
        tree.column("Nome", width=150)

        # Adiciona a lista dos votantes recebidos do servidor à Treeview
        for index, nome in enumerate(votantes, start=1):
            tree.insert("", index, text=index, values=nome)

        # Adicionar barra de rolagem vertical
        vsb = Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)

        # Empacotar o Treeview
        tree.pack(fill=BOTH, expand=True)
        # FIM

        self.root.mainloop()

    # Funcao para consultar os resultados parciais
    def Consultar_resultados(self):
        
        # Utiliza a funcao do arquivo cliente para fazer o pedido do dicionario com a lista do nome dos votantes
        registro_votos = self.cliente_votacao.exibir_resultados()

        # Verificar se há resultados antes de prosseguir
        if not registro_votos:
            messagebox.showinfo("Sem Resultados", "Ainda não há resultados para exibir.")
            return ""
        
        # Fecha o root da tela principal, para manter apenas a tela para visualizar votos
        self.root.destroy()

        self.root = Tk()

        self.root.title(f"Votação Online - Cliente: {self.nome_cliente}")
        self.root.geometry("500x310")
        self.root.resizable(False, False)

        Label(self.root, text=f"Resultado parcial:", font=('Calibri', 12)).place(x=125, y=15)

        Button(self.root, text="Retornar", command=self.Retornar_menu, padx=55, pady=20, font=('Calibri', 12)).place(x=150, y=230)

        # Criacao da arvore com os resultados das chapas e seus numero de votos
        self.Arvore_Resultados(registro_votos)

        self.root.mainloop()
    
    # Funcao para finalizar o programa, mostrando os resultados finais
    def Finalizar(self):
        
        # Fecha o root da tela principal, para manter apenas a tela para visualizar votos
        self.root.destroy()

        while True:
            # Confirmação final
            confirmacao = messagebox.askyesno("Confirmação", "Voce tem certeza que deseja finalizar a votacao?")

            if confirmacao:
                break  # Sai do loop se o usuário confirmar
            else:
                self.Menu()  # Sai do loop se o usuário cancelar a confirmação

        # Utiliza a funcao do arquivo cliente para fazer o pedido do dicionario com a lista do nome dos votantes
        registro_votos = self.cliente_votacao.sair()

        # Verificar se há resultados antes de prosseguir
        if not registro_votos:
            messagebox.showinfo("Sem Resultados", "Não há resultados para exibir.")
            return
        
        self.root = Tk()

        self.root.title(f"Votação Online - Cliente: {self.nome_cliente}")
        self.root.geometry("500x310")
        self.root.resizable(False, False)

        Label(self.root, text=f"Resultado final:", font=('Calibri', 12)).place(x=125, y=15)
        
        Button(self.root, text="Fechar programa", command=self.Destruir_root, padx=55, pady=20, font=('Calibri', 12)).place(x=130, y=230)

        # Criacao da arvore com os resultados das chapas e seus numero de votos
        self.Arvore_Resultados(registro_votos)
        
        self.root.mainloop()

    # Criacao da arvore com as chapas e seus votos
    def Arvore_Resultados(self, dicionario):
        frame = Frame(self.root)
        frame.place(x=50, y=40, height=180, width=400)

        # Criação da Treeview
        tree = ttk.Treeview(frame, columns=("Voto",))
        tree.heading("#0", text="Chapa")
        tree.heading("Voto", text="Votos")

        tree.column("#0", width=150)
        tree.column("Voto", width=50)

        # Adiciona as chapas e votos à Treeview
        for linha in dicionario:
            tree.insert("", "end", text=linha[0], values=linha[1])

        # Adicionar barra de rolagem vertical
        vsb = Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)

        # Empacotar o Treeview
        tree.pack(fill=BOTH, expand=True)
    
    # Funcao para retornar ao menu
    def Retornar_menu(self):
        self.root.destroy()
        self.Menu()

    # Funcao para destruir o root
    def Destruir_root(self):
        self.root.destroy()


# Funcao de execucao de teste do programa
if __name__ == "__main__":
    app = InterfaceVotacao()
