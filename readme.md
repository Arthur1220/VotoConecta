# VotoConecta
O VotoConecta é um software distribuído que permite .

## Funcionamento
O VotoConecta é composto por dois componentes: um cliente e um servidor.

O cliente é responsável por:
* Conectar-se ao servidor
* Enviar mensagens para outros usuários
* Receber mensagens de outros usuários

O servidor é responsável por:
* Gerenciar as conexões dos usuários
* Distribuir as mensagens entre os usuários

## Protocolo de transporte
O protocolo de transporte do VotoConecta é o <protocolo de transporte escolhido> .
O protocolo de transporte <TCP> foi escolhido para o VotoConecta porque ele garante a entrega confiável das mensagens. Isso é importante para um software de comunicação em tempo real, pois as mensagens devem ser entregues ao destinatário sem perdas ou erros.
* Considerações adicionais:
    O protocolo poderia ser aprimorado para suportar recursos adicionais, como:
    Criptografia para proteger a privacidade das mensagens
    Autenticação para verificar a identidade dos usuários
    Histórico de mensagens para permitir que os usuários visualizem as mensagens que já foram trocadas

## Eventos
O protocolo da camada de aplicação do VotoConecta tem <numero de eventos> eventos:
* `ENVIAR_MENSAGEM`
* `RECEBER_MENSAGEM`
O evento `ENVIAR_MENSAGEM` é usado pelo cliente para enviar uma mensagem para outro usuário. A mensagem é composta por um texto e um nome de usuário.
O evento `RECEBER_MENSAGEM` é usado pelo cliente para receber uma mensagem de outro usuário. A mensagem é composta por um texto e um nome de usuário.

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