# Importacao das bibliotecas de rede
import socket
import threading

# Importacao de bibliotecas extras
import os 
from datetime import datetime

# Classe do funcionamento do Servidor
class ServidorVotacaoOnline:

    # Definicao das configuaracoes de rede
    def __init__(self, host, port):
        # Definicao das configuaracoes de rede
        self.HOST = host
        self.PORT = port

        # Inicia a conexao
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        # Dicionários para armazenar as chapas e votantes
        self.chapas = {}
        self.votantes = {}

        # Lista para armazenar operações no formato de dicionário
        self.log_entries = []

        # Limpa o terminal
        if os.name == 'posix':  # Linux e macOS
            os.system('clear')
        elif os.name == 'nt':  # Windows
            os.system('cls')
        
        print("Servidor de Votação Online.\n    -Status: online")

    # Funcao para inicializar o thread
    def iniciar(self):
        while True:
            # Aguarda uma conexão
            client_socket, addr = self.server_socket.accept()

            # Cria um novo thread para lidar com a conexão
            thread = threading.Thread(target=self.function, args=(client_socket, addr))
            thread.start()

            print(f"    -Conexão recebida - ({addr})")

    # Executa a criacao do log e printa no terminal
    def registrar_log(self, operacao, detalhes, resposta):
        print('\n')

        # Obtém a hora atual
        hora_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cria um dicionário para o log
        log_entry = {
            'Hora de execucao': hora_execucao,
            'Operacao': operacao,
            'Detalhes': detalhes,
            'Resposta': resposta
        }

        # Adiciona o log à lista
        self.log_entries.append(log_entry)

        # Imprimir o log formatado
        for tipo, conteudo in log_entry.items():
            print(f'{tipo} : {conteudo}')

    # Funcao para ler o tipo de operacao 
    def processar_operacao(self, partes):
        # Extrai o comando da lista de partes
        comando = partes[0]

        # Verifica o tipo de comando e chama a função correspondente
        if comando == "REGISTRAR_CHAPA":
            return self.processar_registro_chapa(partes[1], partes[2])
        elif comando == "VOTAR":
            return self.processar_voto(partes[1], partes[2])
        elif comando == "VOTANTES":
            return self.processar_consulta_votantes()
        elif comando == "RESULTADOS":
            return self.processar_consulta_resultados()
        elif comando == "SAIDA":
            return self.processar_saida()
        else:
            return "ERROR"

    # Funcao para processar o registro de chapa
    def processar_registro_chapa(self, nome_chapa, valor_chapa):
        """
        Registra uma nova chapa com seu valor associado.

        Args:
            nome_chapa (str): Nome da chapa a ser registrada.
            valor_chapa (float): Valor associado à chapa.

        Returns:
            str: Uma string indicando o status da operação ("CHAPA_REGISTRADA").
        """

        # Verifica se já existe uma chapa com o mesmo nome
        if nome_chapa in self.chapas:
            return "DUPLICATA_NOME"  # Nome da chapa já existe

        # Verifica se já existe uma chapa com o mesmo valor
        if any(valor == valor_chapa for valor in self.chapas.values()):
            return "DUPLICATA_VALOR"  # Valor da chapa já existe

        # Adiciona a nova chapa ao dicionário de chapas
        self.chapas[nome_chapa] = valor_chapa

        # Cria uma string com os detalhes da operação para registro de log
        detalhes = f"Nome: {nome_chapa}, Valor: {valor_chapa}"
        # Registra a operação no log
        self.registrar_log("Registrar Chapa", detalhes, "CHAPA_REGISTRADA")

        return "CHAPA_REGISTRADA"

    # Funcao para processar o registro de voto
    def processar_voto(self, numero_chapa, nome_votante):
        """
        Registra o voto de um votante para uma chapa específica.

        Args:
            numero_chapa (str): Número da chapa para a qual o votante está votando.
            nome_votante (str): Nome do votante que está votando.
            chapas (dict): Dicionário contendo as chapas disponíveis.
            votantes (dict): Dicionário contendo os votantes e suas respectivas escolhas.

        Returns:
            str: Uma string indicando o status da operação ("VOTO_REGISTRADO" ou "CHAPA_INVALIDA").
        """

        # Verifica se o número da chapa está presente entre os valores do dicionário de chapas
        if numero_chapa in self.chapas.values():
            # Registra o voto associando o nome do votante ao número da chapa
            self.votantes[nome_votante] = numero_chapa

            # Cria uma string com os detalhes da operação para registro de log
            detalhes = f"Número da Chapa: {numero_chapa}, Nome do Votante: {nome_votante}"
             # Registra a operação no log
            self.registrar_log("Votar", detalhes, "VOTO_REGISTRADO")

             # Retorna um indicador de que o voto foi registrado com sucesso
            return "VOTO_REGISTRADO"
        else:
            # Se o número da chapa não é válido, registra essa informação no log
            detalhes = f"Número da Chapa: {numero_chapa}, Nome do Votante: {nome_votante}"
            self.registrar_log("Votar - Chapa Inválida", detalhes, "CHAPA_INVALIDA")

             # Retorna um indicador de chapa inválida
            return "CHAPA_INVALIDA"

    # Funcao para processar a consulta de votantes
    def processar_consulta_votantes(self):
        """
        Retorna uma string formatada para consulta de votantes, registrando a operação no log.

        Args:
            votantes (dict): Dicionário contendo os votantes e suas respectivas escolhas.

        Returns:
            str: Uma string formatada para consulta de votantes no formato "  $Votante1$Votante2$...$"
        """

        # Verifica se o dicionário de votantes está vazio e faz o registro no log
        if not self.votantes:
            # Cria uma string com os detalhes da operação para registro de log
            detalhes = "Tentativa falha consulta de Votantes"
            # Registra a operação no log
            self.registrar_log("Tentativa de consultar Votantes", detalhes, "    -Nenhum votante registrado.")

            # Retorna a resposta completa
            return " "

        # Inicializa a resposta
        resposta = ""
        # Adiciona cada votante à resposta
        for votante, voto in self.votantes.items():
            resposta += f"{votante}$"

        # Cria uma string com os detalhes da operação para registro de log
        detalhes = "Consulta de Votantes"
        # Registra a operação no log
        self.registrar_log("Consultar Votantes", detalhes, resposta)

        return resposta

    # Funcao para processar a consulta de resultados
    def processar_consulta_resultados(self):
        """
        Retorna uma string formatada para consulta de resultados da eleição, registrando a operação no log.

        Args:
            chapas (dict): Dicionário contendo as chapas e seus respectivos valores.
            votantes (dict): Dicionário contendo os votantes e suas respectivas escolhas.

        Returns:
            str: Uma string formatada para consulta de resultados no formato "NomeChapa (ValorChapa): Votos votos $..."
                 ou uma mensagem indicando que não há resultados se não houver votos registrados.
        """
        # Verifica se o dicionário de votantes está vazio e faz o registro no log
        if not self.votantes:
            # Cria uma string com os detalhes da operação para registro de log
            detalhes = "Tentativa falha consulta de Resultados"
            # Registra a operação no log
            self.registrar_log("Tentativa de consultar Resultados", detalhes, "    -Nenhum voto registrado. Não há resultados.")

            # Retorna a resposta completa
            return " "

        # Inicializa a resposta
        resposta = ""

        # Itera sobre as chapas para calcular e adicionar os resultados à resposta
        for nome_chapa, valor_chapa in self.chapas.items():
            # Conta quantos votos a chapa recebeu
            votos_chapa = sum(1 for numero in self.votantes.values() if numero == valor_chapa)
            # Adiciona os resultados à resposta
            resposta += f"{nome_chapa} ({valor_chapa}): {votos_chapa} votos $"

        # Cria uma string com os detalhes da operação para registro de log
        detalhes = "Consulta de Resultados"
        # Registra a operação no log
        self.registrar_log("Consultar Resultados", detalhes, resposta)

        # Retorna a resposta completa
        return resposta

    def processar_saida(self):
        """
        Finaliza a conexão entre o servidor e o cliente, registrando a operação no log e retornando os resultados.

        Returns:
            str: Uma string formatada para consulta de resultados no formato "NomeChapa (ValorChapa): Votos votos $..."
                 ou uma mensagem indicando que não há resultados se não houver votos registrados.
        """

        # Cria uma string com os detalhes da operação para registro de log
        detalhes = "Sair - Finalizacao da conexao entre servidor e Cliente"
        # Registra a operação no log
        self.registrar_log("Sair", detalhes, "Conexao desligada e resultados mostrados!")

        # Verifica se o dicionário de votantes está vazio
        if not self.votantes:
            # Retorna a resposta
            return " "
        
        # Inicializa a resposta
        resposta = ""

        # Itera sobre as chapas para calcular e adicionar os resultados à resposta
        for nome_chapa, valor_chapa in self.chapas.items():
            # Conta quantos votos a chapa recebeu
            votos_chapa = sum(1 for numero in self.votantes.values() if numero == valor_chapa)
            # Adiciona os resultados à resposta
            resposta += f"{nome_chapa} ({valor_chapa}): {votos_chapa} votos $"

        # Retorna a resposta completa
        return resposta

    def function(self, client_socket, addr):
        """
        Função principal que processa as solicitações do cliente.

        Args:
            client_socket (socket.socket): Socket conectado ao cliente.
            addr (tuple): Tupla contendo o endereço IP e número da porta do cliente.

        Returns:
            None
        """

        # Status de permanência do cliente
        status = True

        while status:
            # Receba a solicitação do cliente
            try:
                request = client_socket.recv(1024).decode()
            except ConnectionResetError:
                print(f"Erro: A conexão com {addr} foi resetada pelo cliente.")
                break  # Encerra o loop se a conexão foi resetada

            partes = request.split("$")

            # Processa a operação com base nas partes da solicitação
            resposta = self.processar_operacao(partes)

            # Envie a resposta ao cliente
            try:
                client_socket.send(resposta.encode())
            except BrokenPipeError:
                print(f"Erro: A conexão com {addr} foi fechada pelo cliente.")
                status = False

            # Verifica se a operação é de saída
            if partes[0] == "SAIDA":
                status = False

        # Fecha o socket do cliente após o término da comunicação
        client_socket.close()

if __name__ == "__main__":
    # Configurações do servidor
    HOST = '127.0.0.1'
    PORT = 12345

    servidor_votacao = ServidorVotacaoOnline(HOST, PORT)
    servidor_votacao.iniciar()
