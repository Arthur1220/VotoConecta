# VotoConecta
O VotoConecta é um software distribuído que tem como propósito principal permitir a realização de uma eleição ou votação de maneira remota, onde os usuários (votantes) podem registrar seus votos em diferentes chapas a partir de clientes conectados ao servidor.

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

## Protocolo de transporte
O protocolo de transporte do VotoConecta é o TCP.
O protocolo de transporte TCP foi escolhido para o VotoConecta porque ele garante a entrega confiável das mensagens. Isso é importante para um software de comunicação em tempo real, pois as mensagens devem ser entregues ao destinatário sem perdas ou erros, o que garante que o servico de votacao seja confiavel e preciso com as suas informacoes.

**Considerações adicionais:**

O protocolo poderia ser aprimorado para suportar recursos adicionais, como:
* Criptografia para proteger a privacidade das mensagens
* Autenticação para verificar a identidade dos usuários
* Histórico de mensagens para permitir que os usuários visualizem as mensagens que já foram trocadas

## Eventos
O protocolo da camada de aplicação do VotoConecta possui 5 eventos principais e 1 de tratamento de erros e excessoes:


`Registro de Chapa`: `REGISTRAR_CHAPA`
* Mensagem enviada pelo cliente: `REGISTRAR_CHAPA${nome_chapa}${valor_chapa}`
* Mensagem resposta enviada pelo servidor: `CHAPA_REGISTRADA`
* Descrição: Esse evento ocorre quando os administradores ou responsáveis pela votação registram uma nova chapa no sistema, atribuindo-lhe um nome e, possivelmente, um número identificador.
* Funcionamento: O servidor recebe os detalhes da nova chapa, valida os dados e a adiciona à lista de chapas disponíveis. Isso pode envolver a atualização de estruturas de dados no servidor que mantêm as informações sobre as chapas.


`Registro de Voto`: `VOTAR`
* Mensagem enviada pelo cliente: `VOTAR${numero_chapa}${nome_votante}`
* Mensagem resposta enviada pelo servidor: `VOTO_REGISTRADO`
* Descrição: Esse evento ocorre quando um votante envia seu voto para o servidor, indicando a chapa escolhida.
* Funcionamento: O cliente do votante transmite os detalhes do voto para o servidor por meio de uma conexão de socket. O servidor valida o voto e registra as informações associadas, atualizando os totais de votos para a chapa correspondente.


`Consulta de Votantes`: `VOTANTES`
* Mensagem enviada pelo cliente: `VOTANTES`
* Mensagem resposta enviada pelo servidor: lista de votantes com a seguinte configuracao: `{votante}$`
* Descrição: Esse evento ocorre quando um usuário deseja consultar a lista de votantes registrados no sistema.
* Funcionamento: O cliente envia uma solicitação ao servidor, que responde fornecendo a lista de votantes. Essa lista é geralmente mantida pelo servidor e pode ser atualizada conforme novos votantes se registram.


`Consulta de Resultados Parciais`: `RESULTADOS`
* Mensagem enviada pelo cliente: `RESULTADOS`
* Mensagem resposta enviada pelo servidor: lista com resultados parciais com a seguinte configuracao: `{nome_chapa} ({valor_chapa}): {votos_chapa} votos $`
* Descrição: Esse evento ocorre quando os usuários desejam verificar os resultados parciais da votação antes de seu término.
* Funcionamento: O cliente envia uma solicitação ao servidor, que responde fornecendo os resultados parciais. Os resultados podem incluir o número de votos para cada chapa até o momento. Esses dados podem ser atualizados em tempo real ou periodicamente, dependendo da implementação.


`Finalização da Votação`: `SAIDA`
* Mensagem enviada pelo cliente: `SAIDA`
* Mensagem resposta enviada pelo servidor: lista com resultados com a seguinte configuracao: `{nome_chapa} ({valor_chapa}): {votos_chapa} votos $`
* Descrição: Esse evento ocorre quando os administradores ou responsáveis pela votação decidem encerrar o processo de votação.
* Funcionamento: O servidor realiza os cálculos finais, determina os resultados finais da votação e pode fechar a votação para novos votos. Os resultados finais podem ser exibidos para os usuários interessados.


`Mensagens de Erro e Tratamento de Exceções`:
* Mensagem enviada pelo cliente: mensagens incorretas ou fora do padrao esperado
* Mensagem resposta enviada pelo servidor: `DUPLICATA_NOME`, `DUPLICATA_VALOR`, `NOME_INVALIDO` e `CHAPA_INVALIDA`
* Descrição: Esses eventos ocorrem quando ocorrem erros durante o processo, como tentativas de votar em uma chapa inexistente ou duplicada.
* Funcionamento: O servidor trata essas mensagens, fornecendo feedback aos clientes sobre o erro. Pode haver uma lógica específica para lidar com diferentes tipos de erros, garantindo a integridade e a validade do processo de votação.

## Estados
O protocolo da camada de aplicação do VotoConecta tem dois estados:
* `CONECTADO`
* `DESCONECTADO`
O estado `CONECTADO` indica que o cliente está conectado ao servidor. O estado `DESCONECTADO` indica que o cliente não está conectado ao servidor.

## Mensagens
O protocolo da camada de aplicação do VotoConecta usa as seguintes mensagens:
* `MENSAGEM`
A mensagem `MENSAGEM` é composta por um texto e um nome de usuário.

## Diagrama de comunicação
Cliente->>Servidor: CONECTAR
Servidor-->>Cliente: CONECTADO

Cliente->>Servidor: ENVIAR_MENSAGEM(texto, nome_usuario)
Servidor-->>Clientes: MENSAGEM(texto, nome_usuario)

Cliente->>Servidor: DESCONECTAR
Servidor-->>Cliente: DESCONECTADO

## Requisitos mínimos de funcionamento:
O cliente deve ser capaz de se conectar ao servidor e enviar e receber mensagens de acordo com o protocolo definido.
O servidor deve ser capaz de gerenciar as conexões dos usuários e distribuir as mensagens entre eles.