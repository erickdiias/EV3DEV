Instruções
=======

## Necessário para todo programa EV3

~~~python
#!/usr/bin/env/ python3
~~~

A anotação diz o caminho para o interpretador do Python3, é necessária para que o sistema não tente executar o arquivo como binário (o que seria o padrão), mas sim que o execute com o interpretador informado.

## Copiando arquivos para o robô - SCP

~~~bash
scp robot@ev3dev.local:~
# Ou
scp seu_arquivo.py robot@ip_do_robo:~
~~~

Execute o comando no terminal do computador. Após sua execução o arquivo 'seu_arquivo.py' estará copiado no diretório '~'(home) do robô.

## Entrando no robô - SSH

~~~bash
ssh robot@ev3dev.local
# Ou
ssh robot@ip_do_robo
~~~

Execute o comando em um terminal, com o EV3 conectado no computador e com a conexão já configurada. A senha será 'maker'. A partir da execução desse comando você estará 'dentro' do robô, tendo acesso assim ao seu sistema de arquivos e podendo executar comandos no terminal linux.

## Tornando um arquivo executável - CHMOD

~~~bash
chmod +x seu_arquivo.py
~~~

Execute o comando no terminal do robô. Esse comando dará permissão de execução para o arquivo, sendo assim, poderemos executá-lo pelo Brick do EV3.


## Documentação

https://python-ev3dev.readthedocs.io/en/ev3dev-stretch/index.html
