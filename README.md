# FSE - Trabalho 2

| Aluno | Matricula |
| --|-- |
| Matheus Gabriel Alves Rodrigues | 180106970 |

## Sobre

O projeto consiste em realizar uma automação predial de um prédio que tem 2 andares,
o sistema será responsável por automatizar o acionamento de um alarme, ligar ou desligar lâmpadas de cada andar,
realizar a contagem de pessoas pelo prédio, etc.

![gif de funcionamento](./static/apresentacao.gif)

### Observações:

* Recomenda-se executar o **Terreo** primeiro que o **1º Andar**.
* Caso queira executar modificando a porta do central ou o ip, se faz necessário atualizar os arquivos **json** tanto na pasta `central` quanto na pasta `distribuido`.
* Executar o **Central** em uma janela do terminal grande (se possivel em tela cheia) pois o layout montado depende disso.
* Devido a biblioteca **pynput** se faz necessário que o projeto seja executado utilizando tunalamento via ssh, usando o comando abaixo:

    ```
    ssh -R 10048:localhost:10048 <usuario e path da rasp42>
    ```

## Como executar

Na execução desse projeto deve-se executar primeiro o servidor central e depois os distribuidos.

#### Central

O Servidor central foi feito usando a linguagem **python** e para executar o projeto deve instalar alguns pacotes simples 
que estão no arquivo **requirements.txt**.

```
pip install -r requirements.txt
```
Se quiser antes da etapa acima voce pode utilizar um ambiente virtual do python, criado assim:

```
python -m venv .venv
source .venv/bin/activate
```

Executar o servidor central:

```
cd central
python server.py
```
Não executar de fora da pasta `central` pois o arquivo `alarme.mp3` se encontra dentro da mesma.

#### Distribuidos

Para executar os sistemas distribuidos foi disponibilizado um arquivo **Makefile** na pasta **Distribuidos**,
os comandos disponiveis são:

* `make all` - Builda a aplicação
* `make clean` - Limpa o os arquivos buildados
* `make terreo` - Executa o distribuido usando o json de configurações do terreo
* `make 1andar` - Executa o distribuido usando o json de configurações do 1º andar


## Comandos

Quando os serviços estiverem em execução as seguintes teclas serão responsáveis por realizar as seguintes tarefas:

* **F1** : Ligar lampada T01
* **F2** : Ligar lampada T02
* **F3** : Ligar lampada corredor terreo
* **F4** : Ligar ar-condicionado terreo
* **F5** : Ligar aspersor
* **F6** : Ligar lampada 101
* **F7** : Ligar lampada 102
* **F8** : Ligar lampada corredor 1º andar
* **F9** : Ligar lampada ar-condicionado 1º andar
* **F10** : Ligar Alarme
