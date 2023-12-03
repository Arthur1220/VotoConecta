# Importacao da biblioteca de rede
import socket

# Classe do funcionamento do Cliente
class ClienteVotacaoOnline:
    # Construtor para inicializar a conexao cliente servidor
    def __init__(self, host, port, nomeCliente):
        
        # Definicao das configuaracoes de rede
        self.nomeCliente = nomeCliente
        self.HOST = host
        self.PORT = port

        # Executa a conexao com o servidor
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

    # Funcao para enviar mensagem/receber resposta do servidor
    def enviar_mensagem(self, mensagem):
        self.client_socket.send(mensagem.encode())
        resposta = self.client_socket.recv(1024).decode()

        return resposta

    # Funcao para registrar chapa, onde sera criado a string com as informacoes
    def registrar_chapa(self, nome_chapa, valor_chapa):
        mensagem = f"REGISTRAR_CHAPA${nome_chapa}${valor_chapa}"
        resposta = self.enviar_mensagem(mensagem)

        return resposta

    # Funcao para registrar voto, onde sera criado a string com as informacoes
    def votar(self, numero_chapa, nome_votante):
        mensagem = f"VOTAR${numero_chapa}${nome_votante}"
        resposta = self.enviar_mensagem(mensagem)

        return resposta

    # Funcao executar o pedido da lista com votantes, onde recebera uma string com as informacoes, que devem ser tratadas antes de enviadas para a interface
    def consultar_votantes(self):
        resposta = self.enviar_mensagem("VOTANTES")

        # Separa os nomes dos votantes usando "$" como delimitador
        nomes_votantes = resposta.split("$")

        # Remove possíveis strings vazias resultantes da separação
        nomes_votantes = [nome.strip() for nome in nomes_votantes if nome.strip()]

        # Cria uma lista a partir dos nomes dos votantes
        votantes = []
        for nome in nomes_votantes:
            votantes.append(nome) 

        return votantes
    
    # Funcao executar o pedido da lista com os resultados, onde recebera uma string com as informacoes, que devem ser tratadas antes de enviadas para a interface
    def exibir_resultados(self):
        resposta = self.enviar_mensagem("RESULTADOS")

        resultados = resposta.split("$")
        
        # Remove possíveis strings vazias resultantes da separação
        resultados = [nome.strip() for nome in resultados if nome.strip()]

        # Cria uma lista a partir dos nomes dos votantes
        resultados_final = []
        for texto in resultados:
             string = texto.split(":")
             resultados_final.append([string[0], string[1]])

        resultados_final.sort(key = lambda x: x[1], reverse=True)

        return resultados_final
    
    # Funcao para executar o pedido da lista com votantes, onde recebera uma string com as informacoes, que devem ser tratadas antes de enviadas para a interface, e finalizar a conexao com o servidor
    def sair(self):
        resposta = self.enviar_mensagem("SAIDA")

        resultados = resposta.split("$")
        
        # Remove possíveis strings vazias resultantes da separação
        resultados = [nome.strip() for nome in resultados if nome.strip()]

        # Cria uma lista a partir dos nomes dos votantes
        resultados_final = []
        for texto in resultados:
             string = texto.split(":")
             resultados_final.append([string[0], string[1]])

        resultados_final.sort(key = lambda x: x[1], reverse=True)

        self.client_socket.close()

        return resultados_final

# Funcao de execucao de teste do programa
if __name__ == "__main__":

    # Configurações do cliente
    HOST = '127.0.0.1'
    PORT = 12345
    
    # Definicao do nome do cliente
    nomeCliente = 'default'

    # Inicializa o construtor e a Classe Cliente
    cliente_votacao = ClienteVotacaoOnline(HOST, PORT, nomeCliente)
    
    # Registrar algumas chapas
    resposta_registrar_chapa_1 = cliente_votacao.registrar_chapa("Chapa 01", "1")
    resposta_registrar_chapa_2 = cliente_votacao.registrar_chapa("Chapa 02", "2")

    # Printa os retornos
    print('1: ', resposta_registrar_chapa_1)
    print('2: ', resposta_registrar_chapa_2)

    # Votar em algumas chapas
    resposta_votar_1 = cliente_votacao.votar("1", "Votante 1")
    resposta_votar_2 = cliente_votacao.votar("1", "Votante 2")

    # Printa os retornos
    print('3: ', resposta_votar_1)
    print('4: ', resposta_votar_2)

    # Exibir votantes
    votantes = cliente_votacao.consultar_votantes()
    # Printa o retorno
    print('5: ', votantes)

    """ # Exibir resultados
    resultados = cliente_votacao.exibir_resultados()
    # Printa o retorno
    print('6: ', resultados)

    # Sair/Finalizar conexao
    registro_votos = cliente_votacao.sair()
    # Printa o retorno
    print(f"Registro de Votos: {registro_votos}") """
