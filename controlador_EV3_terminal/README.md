Controlando um robô LEGO Mindstorms EV3 através do terminal
=======
Esse código é um script em Python para controlar um robô com motores conectados ao EV3, como os utilizados nos kits LEGO Mindstorms. Ele permite controlar o robô a partir do teclado, onde cada tecla pressionada corresponde a um comando específico de movimento.
Aqui está o que cada parte do código faz:
~~~python
#!/usr/bin/env python3:
~~~
Essa linha é chamada de shebang e indica que o script deve ser executado usando o interpretador Python 3.
Importação de módulos:

termios: Módulo para a manipulação de configurações de terminal.
tty: Módulo para operações relacionadas ao terminal.
sys: Módulo para interação com o interpretador Python.
time: Módulo para operações relacionadas ao tempo.
ev3dev2.motor: Módulo para interagir com os motores EV3.
threading: Módulo para suporte à programação concorrente.

## Configuração dos motores:

Os motores direito e esquerdo são inicializados para controlar o movimento do robô.
Definição de funções para cada comando de movimento:

forward(): Faz o robô mover-se para frente.
~~~bash
back(): Faz o robô mover-se para trás.

left(): Faz o robô virar para a esquerda.

right(): Faz o robô virar para a direita.

stop(): Para o movimento do robô.
~~~
## Definição da função:
getch(): Essa função é usada para ler um caractere único do terminal sem a necessidade de pressionar Enter. Isso permite que o robô responda instantaneamente às teclas pressionadas.

Loop principal while True: O programa entra em um loop infinito, onde a cada iteração, lê uma tecla pressionada pelo usuário e executa a função correspondente ao comando de movimento associado a essa tecla. O loop continuará até que o usuário pressione a tecla 'q', o que levará ao encerramento do programa.

## Mapeamento de teclas para comandos:

Quando o usuário pressiona uma tecla, o caractere é armazenado na variável k.
Cada comando de movimento é mapeado para uma tecla específica:
~~~bash
'w': Move o robô para frente (chamando a função forward()).

's': Move o robô para trás (chamando a função back()).

'a': Faz o robô virar para a esquerda (chamando a função left()).

'd': Faz o robô virar para a direita (chamando a função right()).

' ': Para o movimento do robô (chamando a função stop()).

'q': Encerra o programa (chamando a função exit()).
~~~
Esse código permite controlar o robô remotamente usando o teclado do computador enquanto ele está conectado e em execução. É importante lembrar que o código atualmente não lida com outros aspectos do controle do robô, como evitar obstáculos ou parar em caso de emergência. É apenas uma implementação simples para controlar os motores em diferentes direções.
