# FuncsForSPO - Funcoes para Selenium; Python; Openpyxl; SQLite3

## pip install FuncsForSPO | NECESSÁRIO PYTHON 3.10

Aqui voce achara funcoes produzidas para ter maior agilidade nos desenvolvimentos nas tecnologias abaixo:

* Selenium
  * Existem diversas funcoes em pt-br que vao te ajudar a desenvolver os seus projetos mais rapidamente em selenium
* Openpyxl (ainda em desenvolvimento para mais funcoes)
  * Algumas funcoes que minimizarao o trabalho pesado de mexer com openpyxl
* Python
  * Funcoes criadas para o Python, como excluir varios arquivos, criar, verificar se um programa / executavel esta aberto, entre outras funcionalidades

## Instalacao

pip install FuncsForSPO em seu ambiente virtual e pronto!

Powered By [https://github.com/gabriellopesdesouza2002](https://github.com/gabriellopesdesouza2002)

# Current Version -> 6.7.0

version==4.33.1 -> Melhoria e criação de diversas funções desde a versão 4.24

version==4.24.0 -> Melhoria nas documentações das funções, e melhoria na função de esperar elemento

 version==4.23.6 -> Melhoria nas documentações das funções, e adicionada uma função para ver dias a frente ou dias a atrás

version==4.22.6 -> Melhorias na função do faz_log agora com formatacao Rich, melhoria nas amostras de output dos códigos

version==4.18.1 -> Melhorias nas funcoes do selenium

version==4.17.1 -> correcao

version==0.0.4.17 -> Funcao para converter imagens em um pdf

version==0.0.4.16 -> Funcoes para criar ambiente de desenvolvimento em um novo projeto python, basta criar seu arquivo main.py, dar pip install FuncsForSPO no ambiente global e executar essa função (cria_diretorios_para_novo_projeto_python)

version==0.0.4.15 -> Correcoes

version==0.0.4.14 -> Criada API para comprimir PDF, organizacao dos pacotes

version==0.0.4.13 -> Melhoria na API de OCR, criada uma exception para a API

version==0.0.4.12 -> funcao que converte para real (BRL)

version==0.0.4.9.9 -> Adicao de função que pode recuperar o texto de todo o site, usando bs4 e requests

version==0.0.4.9.8 -> Adicao de varias funcoes

version==0.0.4.9.7 -> melhorias nas funcoes de popup

version==0.0.4.9.6 -> + Funções, para envio de e-mails, Outlook (melhorada) e Gmail. agora e possivel chamar as funcoes via from FuncsForSPO.femails.femails import * por exemplo

version==0.0.4.9.5 -> + Funções, vide commits

version==0.0.4.9.4 -> Funcao que remove acentos usando unidecode, outra que retorna o valor do arquivo, espera um arquivo terminar o download, threading

version==0.0.4.9.3 -> Funcao que faz backup do banco de dados e funcao que retorna o cursor e a connection SQLite3

version==0.0.4.9.2 -> correcao

version==0.0.4.9.1 -> correcao

version==0.0.4.9 -> Adicionada funcoes no modulo functions_for_py.py

version==0.0.4.8 -> funcao que faz download de arquivo compartilhado no sharepoint, com selenium

version==0.0.4.7 -> funcoes que mostram todos os dados de um arquivo, conversao de bytes, K, M, G, T, P; funcoes que mostram notificacoes usando winotify

version==0.0.4.6 -> funcoes para tempo, retorna o valor da function time() e outra funcao que retorna o valor do (fim - inicio) / 60  para saber o tempo de execucao

version==0.0.4.5 -> funcao que le um arquivo json e retorna um dict, e outra que recebe um dict e envia para o arquivo json

version==0.0.4.4 -> funcao regex que pode recuperar datas nos formatos: 9.9.9999 | 99.99.9999 | 9.9.99 | 99.99.99 | 99/99/9999 | 9/9/9999 | 99/99/99 | 9/9/99

version==0.0.4.3 -> removida funcoes que utilizam psutil, pois ocorreram muitos erros em varios com

version==0.0.4.2 -> adicionada funcao que faz ocr, recupera o config.ini como dict, novas dependencias, funcao que executa no terminal pelo os.system(), funcao que seta o zoom da pagina web, funcao que pega os numeros via regex que retorna o numero, download via wget

version==0.0.4.0 -> foi adicionado pacotes para melhor organizar cada modulo, adicionada tambem uma funcao que pode deletar um diretorio, com ou sem arquivos

version==0.0.3.19 -> funcao que verifica por meio de ping se esta conectado com o ip, pode ser utilizado para verificar se esta conectado na vpn

version==0.0.3.18 -> adicionada 3 funcoes para trabalhar com conexao ftp, download de arquivo, upload de arquivo e alternancia de permissoes dos arquivos

version==0.0.3.17 -> adicionada algumas funções úteis, como remover números de uma string, baixar pdf com o base64 entre outras...

version==0.0.3.16 -> Adicao de 2 funcoes selenium uma que espera o elemento ficar visivel e outra que espera ele ficar ativo, clicavel e visivel

version==0.0.3.15 -> melhoria em funcao que recupera lista de elementos, agora e possivel enviar argumentos, como, recuperar com tudo upper

version==0.0.3.14 -> adicionada 1 funcao que espera webelement estar visivel

version==0.0.3.13 -> adicionada 2 funcoes que retornam data e hora dias a frente e uma que envia send_keys e da um esc. Foi adicionada também 2 funcoes do PySimpleGUI que mostra uma mensagem de erro e outra de finalizado

version==0.0.3.12 -> adicao de funcao para enviar e-mails pelo outlook; melhoria da funcao regex extrair email com base no padrão RFC2822

version==0.0.3.11 -> melhoria na Licenca. Adicionada funcao que executa o garbage_collector, melhorias na documentacao, melhoria na funcao que pega data e hora atual via formatacao strftime, adiciona data no caminho de qualquer arquivo, que pode ter inclusive sufixo em caso de arquivos repetidos, melhoria da funcao de baixar arquivo via link. adicionada um modulo com varias funcoes regex. melhoria na recuperacao de dados de coluna que ao achar um datetime, convertera para uma data normal

version==0.0.3.10 -> removida funcao que retorna uma tupla ao reverso, e adicionada a funcao (reverse_iter) que retorna ao reverso qualquer iteravel | adicionada a funcao que retorna os valores absolutos de qualquer arquivo e/ou diretorio de um caminho relativo de um diretorio (arquivos_com_caminho_absoluto_do_arquivo); adicionada tambem uma funcao que faz download de arquivos na internet (download_file); melhorias nas DocStrings

version==0.0.3.9 -> criada uma funcao que retorna somente numeros utilizando re

version==0.0.3.8 -> adicionada 2 funcoes 1-> retorna os valores absolutos de qualquer arquivo 2-> remove qualquer arquivo que contenha (1), (2), (3) (etc) em qualquer pasta

version==0.0.3.7 -> criada uma funcao que retorna um user-agent do tipo random

version==0.0.3.6 -> melhoria na funcao pega_id

version==0.0.3.5 -> adicionada uma funcao para retornar uma tupla ao reverso, (1,2,3,4,5,6,7,8,9,0), -> (0,9,8,7,6,5,4,3,2,1); adicionada execao do wget, correcoes: 1- correcao ao fazer log, ao enviar um objeto, automaticamente ele e convertido para string removido os print na funcao de pegar colunas no openpyxl

version==0.0.3.4 -> webdriver-manager e instalado automaticamente como dependencia

version==0.0.3.3 -> Adicao de varias funcoes do openpyxl* necessita TDD's

version==0.0.3.2 -> Adicao de 2 funcoes no functions_for_py (pega_caminho_atual; pega_caminho_atual_e_concatena_novo_dir)

version==0.0.3.1 -> Adicao de excecao para erro de login no Gmail; adicao de funcao para pegar codigo fonte de um WebElement Selenium

version==0.0.3.0 -> Adicao de funcoes para SQLite

version==0.0.2.8 ->Melhoria nos imports das execoes em Selenium

version==0.0.2.7 -> Corrigido erro ao enviar as funcoes de openpyxl

version==0.0.2.6 -> Corrigido erro ao utilizar a funcao "faz_log()
