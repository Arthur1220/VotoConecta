# VotoConecta
O VotoConecta é um software distribuído que tem como propósito principal permitir a realização de uma eleição ou votação de maneira remota, onde os usuários (votantes) podem registrar seus votos em diferentes chapas a partir de clientes conectados ao servidor. O software foi desenvolvido pela dupla: **Arthur Marques Azevedo** e **Gabriela Zerbone Magno Baptista** 

## Funcionamento
O VotoConecta é composto por dois componentes: um cliente e um servidor, e um arquivo de interface grafica, criado com objetivo de melhor interacao entre servidor e cliente.

**Servidor de Votação Online:**
* O servidor é responsável por gerenciar as conexões com os clientes e processar as operações de votação.
* Ele mantém uma lista de chapas e votantes, registra os votos recebidos e fornece consultas de votantes e resultados.
* Utiliza sockets para a comunicação entre o servidor e os clientes, permitindo a transmissão de dados pela rede.
    
**Cliente de Votação Online:**
* Os clientes são interfaces de usuário que permitem que os votantes interajam com o servidor.
* Eles podem registrar novas chapas, votar em chapas existentes, consultar a lista de votantes registrados e verificar os resultados parciais da votação.
* Cada cliente é conectado ao servidor através de sockets.

**Cliente de Interface Gráfica:**
* Este componente é uma interface gráfica para os clientes de votação. Ele fornece uma experiência de usuário mais amigável e interativa, facilitando a interação dos usuários com o sistema.
* A interface permite registrar novas chapas, votar, consultar votantes e visualizar resultados.

## Como executar o software
Verifique se você tem o Python instalado em sua máquina antes de executar o programa. Você pode baixá-lo em <https://www.python.org/downloads/>.

**Passos gerais:**
**Configuração do Ambiente:**
* Abra um terminal ou prompt de comando.
* Navegue até o diretório onde seus arquivos estão localizados usando cd.

**Execute o Servidor:**
* Execute o script do servidor nomeado como Servidor.py, use o seguinte comando:
        python Servidor.py
* **Certifique-se de que o servidor esteja configurado com o host e a porta corretos.**

**Executar o Cliente:**
* Execute o script da interface cliente, nomeado como Cliente_Interface.py, use o seguinte comando:
        python Cliente_Interface.py
* **Verifique se as configurações de host e porta no cliente correspondem às do servidor.**

## Protocolo de transporte
O protocolo de transporte do VotoConecta é o TCP.
O protocolo de transporte TCP foi escolhido para o VotoConecta porque ele garante a entrega confiável das mensagens. Isso é importante para um software de comunicação em tempo real, pois as mensagens devem ser entregues ao destinatário sem perdas ou erros, o que garante que o servico de votacao seja confiavel e preciso com as suas informacoes.

## Eventos
O protocolo da camada de aplicação do VotoConecta possui 5 eventos principais e 1 de tratamento de erros e excessoes:


1. `Registro de Chapa`: `REGISTRAR_CHAPA`
* Mensagem enviada pelo cliente: `REGISTRAR_CHAPA${nome_chapa}${valor_chapa}`
* Mensagem resposta enviada pelo servidor: `CHAPA_REGISTRADA`
* Descrição: Esse evento ocorre quando os administradores ou responsáveis pela votação registram uma nova chapa no sistema, atribuindo-lhe um nome e, possivelmente, um número identificador.
* Funcionamento: O servidor recebe os detalhes da nova chapa, valida os dados e a adiciona à lista de chapas disponíveis. Isso pode envolver a atualização de estruturas de dados no servidor que mantêm as informações sobre as chapas.


2. `Registro de Voto`: `VOTAR`
* Mensagem enviada pelo cliente: `VOTAR${numero_chapa}${nome_votante}`
* Mensagem resposta enviada pelo servidor: `VOTO_REGISTRADO`
* Descrição: Esse evento ocorre quando um votante envia seu voto para o servidor, indicando a chapa escolhida.
* Funcionamento: O cliente do votante transmite os detalhes do voto para o servidor por meio de uma conexão de socket. O servidor valida o voto e registra as informações associadas, atualizando os totais de votos para a chapa correspondente.


3. `Consulta de Votantes`: `VOTANTES`
* Mensagem enviada pelo cliente: `VOTANTES`
* Mensagem resposta enviada pelo servidor: lista de votantes com a seguinte configuracao: `{votante}$`
* Descrição: Esse evento ocorre quando um usuário deseja consultar a lista de votantes registrados no sistema.
* Funcionamento: O cliente envia uma solicitação ao servidor, que responde fornecendo a lista de votantes. Essa lista é geralmente mantida pelo servidor e pode ser atualizada conforme novos votantes se registram.


4. `Consulta de Resultados Parciais`: `RESULTADOS`
* Mensagem enviada pelo cliente: `RESULTADOS`
* Mensagem resposta enviada pelo servidor: lista com resultados parciais com a seguinte configuracao: `{nome_chapa} ({valor_chapa}): {votos_chapa} votos $`
* Descrição: Esse evento ocorre quando os usuários desejam verificar os resultados parciais da votação antes de seu término.
* Funcionamento: O cliente envia uma solicitação ao servidor, que responde fornecendo os resultados parciais. Os resultados podem incluir o número de votos para cada chapa até o momento. Esses dados podem ser atualizados em tempo real ou periodicamente, dependendo da implementação.


5. `Finalização da Votação`: `SAIDA`
* Mensagem enviada pelo cliente: `SAIDA`
* Mensagem resposta enviada pelo servidor: lista com resultados com a seguinte configuracao: `{nome_chapa} ({valor_chapa}): {votos_chapa} votos $`
* Descrição: Esse evento ocorre quando os administradores ou responsáveis pela votação decidem encerrar o processo de votação.
* Funcionamento: O servidor realiza os cálculos finais, determina os resultados finais da votação e pode fechar a votação para novos votos. Os resultados finais podem ser exibidos para os usuários interessados.


6. `Mensagens de Erro e Tratamento de Exceções`:
* Mensagem enviada pelo cliente: mensagens incorretas ou fora do padrao esperado
* Mensagem resposta enviada pelo servidor: `DUPLICATA_NOME`, `DUPLICATA_VALOR` e `CHAPA_INVALIDA`
* Descrição: Esses eventos ocorrem quando ocorrem erros durante o processo, como tentativas de votar em uma chapa inexistente ou duplicada.
* Funcionamento: O servidor trata essas mensagens, fornecendo feedback aos clientes sobre o erro. Pode haver uma lógica específica para lidar com diferentes tipos de erros, garantindo a integridade e a validade do processo de votação.

## Estados
O protocolo da camada de aplicação do VotoConecta tem dois estados:

**Estado de Inicialização:**
Descrição: O software está em processo de inicialização. Nesse estado, o sistema carrega configurações, estabelece conexões, e realiza outras tarefas necessárias para preparar o ambiente de votação.

**Estado de Registro de Chapas:**
Descrição: Durante esta fase, o software aceita o registro de chapas e as adiciona à lista de opções de voto.

**Estado de Registro de Voto:**
Descrição: Este estado envolve o registro de votantes no sistema. Os votantes fornecem informações necessárias para o voto, como o nome do votante e o valor da chapa que deseja votar.

**Estado de Consulta de Resultados Parciais:**
Descrição: Este estado permite que os usuários consultem os resultados parciais da votação antes de sua conclusão. Essa funcionalidade pode estar disponível para manter os votantes informados sobre o progresso da votação.

**Estado de Consulta de Votantes:**
Descrição: Este estado permite que os usuários consultem os votantes ja cadastrados no sistema, mas sem acesso a seu respectivo voto.

**Estado de Finalização da Votação:**
Descrição: Quando a votação é encerrada, o software entra neste estado. Ele realiza os cálculos finais, determina os resultados e exibe as informações finais da votação.

**Estado de Encerramento:**
Descrição: Após a votação e a apresentação dos resultados, o software pode entrar em um estado de encerramento, onde as atividades principais são encerradas.

**Estado de Erro ou Exceção:**
Descrição: Se ocorrerem erros durante qualquer fase do processo, o software entra em um estado de erro. Ele exibe mensagens de erro apropriadas e oferecer opções para corrigir ou contornar os problemas.

## Mensagens
O protocolo da camada de aplicação do VotoConecta usa mensagens padronizadas e com identificadores para se comunicar entre cliente e servidor.

**Mensagens do Cliente para o Servidor:**
* `REGISTRAR_CHAPA$nome_chapa$valor_chapa`: Solicitação para registrar uma nova chapa com o nome nome_chapa e o valor associado valor_chapa.
* `VOTAR$numero_chapa$nome_votante`: Solicitação para registrar o voto de um nome_votante para a chapa com o número numero_chapa.
* `VOTANTES`: Solicitação para obter a lista de votantes registrados.
* `RESULTADOS`: Solicitação para obter os resultados parciais da votação.
* `SAIDA`: Solicitação para encerrar a votação e obter os resultados finais.


**Mensagens do Servidor para o Cliente:**
* `CHAPA_REGISTRADA`: Confirma que a chapa foi registrada com sucesso.
* `DUPLICATA_NOME`: Indica que já existe uma chapa com o mesmo nome.
* `DUPLICATA_VALOR`: Indica que já existe uma chapa com o mesmo valor.
* `VOTO_REGISTRADO`: Confirma que o voto foi registrado com sucesso.
* `CHAPA_INVALIDA`: Indica que o número da chapa fornecido não é válido.
* Consulta de Votantes: Retorna a lista de votantes no formato `$Votante1$Votante2$...$`.
* Consulta de Resultados: Retorna os resultados no formato `NomeChapa (ValorChapa): Votos votos $...` ou apenas um retono vazio, que o cliente identificao como sem resultados.
* Conexão desligada e resultados mostrados!: Indica que a votação foi encerrada e os retorna os resultados finais.

## Diagrama de comunicação
**Diagrama em desenho**
+---------------------+                                         +------------------------+
|                     |                                         |                        |
|     Servidor        |                                         |       Cliente          |
|                     |                                         |                        |
+---------------------+                                         +------------------------+
           |                                                                 |
           |   1. Conexão estabelecida                                       |
           |---------------------------------------------------------------->|
           |                                                                 |
           |                                                                 |
           |   2. `REGISTRAR_CHAPA$nome_chapa$valor_chapa`                   |
           |<----------------------------------------------------------------|
           |                                                                 |
           |   3. `CHAPA_REGISTRADA` ou `DUPLICATA_NOME` ou `DUPLICATA_VALOR`|
           |---------------------------------------------------------------->|
           |                                                                 |
           |                                                                 |
           |   4. `VOTAR$numero_chapa$nome_votante`                          |
           |<----------------------------------------------------------------|
           |                                                                 |
           |   5. `VOTO_REGISTRADO` ou `CHAPA_INVALIDA`                      |
           |---------------------------------------------------------------->|
           |                                                                 |
           |                                                                 |
           |   6. `VOTANTES`                                                 |
           |<----------------------------------------------------------------|
           |                                                                 |
           |   7. Lista de votantes ou lista vaiza                           |
           |---------------------------------------------------------------->|
           |                                                                 |
           |                                                                 |
           |   8. `RESULTADOS`                                               |
           |<----------------------------------------------------------------|
           |                                                                 |
           |   9. Lista de resultados ou lista vaiza                         |
           |---------------------------------------------------------------->|
           |                                                                 |
           |                                                                 |
           |   10. `SAIDA`                                                   |
           |<----------------------------------------------------------------|
           |                                                                 |
           |   11. Lista de resultados finais ou lista vaiza                 |
           |---------------------------------------------------------------->|
           |                                                                 |
           |   12. Conexão encerrada                                         |
           |---------------------------------------------------------------->|
           |                                                                 |
+---------------------+                                         +------------------------+
|                     |                                         |                        |
|     Servidor        |                                         |       Cliente          |
|                     |                                         |                        |
+---------------------+                                         +------------------------+

**Diagrama em tabela**
| Servidor  |  Operacao |Cliente   |
| :------------: | :------------: | :------------: |
|   |  1. Conexão estabelecida |  -> |
|   |   |   |
| <-  |   2. `REGISTRAR_CHAPA$nome_chapa$valor_chapa` |   |
|   |  3. `CHAPA_REGISTRADA` ou `DUPLICATA_NOME` ou `DUPLICATA_VALOR` |  -> |
|   |   |   |
|  <- | 4. `VOTAR$numero_chapa$nome_votante`  |   |
|   | 5. `VOTO_REGISTRADO` ou `CHAPA_INVALIDA`  |  -> |
|   |   |   |
| <-  |  6. `VOTANTES` |   |
|   |  7. Lista de votantes ou lista vaiza |  -> |
|   |   |   |
|  <- |  8. `RESULTADOS` |   |
|   | 9. Lista de resultados ou lista vaiza  | ->  |
|   |   |   |
|  <- |  10. `SAIDA` |   |
|   | 11. Lista de resultados finais ou lista vaiza  |  -> |
|   | 12. Conexão encerrada  |  -> |

**Legenda:**
1. Estabelecimento da conexão.
2. O cliente envia uma solicitação para registrar uma chapa.
3. O servidor responde indicando se a chapa foi registrada com sucesso ou se houve um problema (duplicata de nome).
4. O cliente envia uma solicitação para votar.
5. O servidor responde indicando se o voto foi registrado com sucesso ou se houve um problema (chapa inválida).
6. O cliente solicita a lista de votantes.
7. O servidor envia a lista de votantes.
8. O cliente solicita a lista de resultados.
9. O servidor envia a lista de resultados.
10. O cliente solicita a finalização da votação.
11. O servidor envia os resultados finais.
12. Encerramento da conexão.
                       
## Requisitos mínimos de funcionamento:
**Python:** 
* O software é escrito em Python, portanto, é necessário ter o interpretador Python instalado no sistema onde o servidor e os clientes serão executados. O código e compatível com Python 3.

**Bibliotecas Padrão do Python:**
* socket: Utilizado para comunicação em rede.
* threading: Utilizado para manipulação de threads.
* tkinter: Utilizado para o funcionamento da interface grafica.
* os: Utilizado para limpar o terminal (compatível com sistemas Linux e Windows).
* datetime: Utilizado para registrar a hora de execução.

**Configurações de Rede:**
* O servidor está configurado para escutar em um endereço IP ('127.0.0.1') e porta (12345). Isso indica que o servidor espera conexões na interface de loopback (localhost) na porta 12345. Certifique-se de que essa porta esteja disponível e não esteja bloqueada por firewalls.

**Requisitos para o Correto Funcionamento:**
**Conexão entre Servidor e Cliente:**
* O servidor e os clientes devem ser capazes de se comunicar pela rede. Certifique-se de que não há bloqueios de firewall ou outros obstáculos impedindo a comunicação entre o servidor e os clientes.

**Manutenção do Formato da Mensagem:**
* O correto funcionamento do software depende do formato das mensagens trocadas entre o servidor e os clientes. Certifique-se de que o formato da mensagem é mantido corretamente ao adicionar novas funcionalidades ou ao modificar o código.

**Execução sem Erros:**
* Certifique-se de que não há erros no código, pois os erros podem levar a comportamentos inesperados.

## Observacoes:
**O código foi desenvolvido na última versão LTS do Ubuntu, visando recursos disponiveis e conhecimentos previos. Contudo, é necessário atentar para possíveis desajustes na interface gráfica devido a mudanças no sistema operacional. Além disso, é crucial verificar e adaptar o código às políticas de segurança e configurações de rede específicas do Sistema Operacional utilizado, garantindo uma implementação harmoniosa e eficiente do software.**